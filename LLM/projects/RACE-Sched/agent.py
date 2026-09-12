from __future__ import annotations

from collections import deque
import math
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger

from DynaSchedBench.Agents.utils import (
    LLMClient,
    NullLLMClient,
    PerformanceTrigger,
    StepTrigger,
)
from DynaSchedBench.Agents.LLMScheduler.logger import TrajectoryLogger
from DynaSchedBench.Gen import InputModel
from DynaSchedBench.Env import DynaSchedEnv

from ..Base import BaseAgent
from .config import LLMCoderConfig
from .rules import RuleManager, SPTPriorityRule, choose_action_by_rule
from .async_worker import AsyncCoderWorker, CoderTask
from .repository import RuleRepository
from .coder import LLMCoder
from .sandbox_eval import (
    evaluate_candidate_rule,
    evaluate_candidate_rule_jms,
    EvalEventsPool,
    JMSEvalPool,
)
from .agentic import PlannerAgent, CriticAgent
from .stats_utils import even_sample, finite_float, numeric_stats


def _eval_result_dict(res: Any, *, combined_score: Optional[float] = None) -> Dict[str, Any]:
    """Serialize an EvalResult-like object for logs."""

    out: Dict[str, Any] = {
        "baseline_value": res.baseline_value,
        "candidate_value": res.candidate_value,
        "relative_improvement": res.relative_improvement,
        "accepted": res.accepted,
        "episodes_used": res.episodes_used,
        "effect_size": res.effect_size,
    }
    if combined_score is not None:
        out["combined_score"] = combined_score
    return out


class AsyncDualStreamAgent(BaseAgent):
    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        cfg: Optional[LLMCoderConfig] = None,
    ) -> None:
        self.cfg = cfg or LLMCoderConfig()
        self._llm_client: LLMClient = llm_client or NullLLMClient()
        self._fallback_rule = SPTPriorityRule()
        self._rules = RuleManager(self._fallback_rule, name="SPT")
        self._trigger = StepTrigger(self.cfg.max_steps_between_updates)
        if self.cfg.use_performance_trigger:
            self._perf_trigger: Optional[PerformanceTrigger] = PerformanceTrigger(
                self.cfg.perf_trigger_window,
                self.cfg.perf_trigger_min_relative_change,
            )
        else:
            self._perf_trigger = None
        self._repo = RuleRepository(path=self.cfg.repository_path) if self.cfg.use_repository else None
        if isinstance(self._llm_client, NullLLMClient) or self.cfg.force_sync_codegen_interval > 0:
            self._worker: Optional[AsyncCoderWorker] = None
        else:
            self._worker = AsyncCoderWorker(self._llm_client, self.cfg)
        self._sync_coder: Optional[LLMCoder] = None
        self._traj_logger = TrajectoryLogger()
        self._global_step = 0
        self._scenario_info: Optional[Dict[str, Any]] = None
        self._repo_warm_started = False
        self._n_codegen_triggers = 0
        self._n_codegen_submitted = 0
        self._n_rule_switches = 0
        self._n_force_sync_calls = 0
        self._n_force_sync_success = 0
        self._force_sync_fail_streak = 0
        self._force_sync_next_allowed_step = 0
        self._force_sync_last_outcome = ""
        self._eval_events_pool: Optional[EvalEventsPool] = None
        self._jms_eval_pool: Optional[JMSEvalPool] = None
        self._planner: Optional[PlannerAgent] = None
        self._critic: Optional[CriticAgent] = None
        window_size = max(1, int(self.cfg.state_profile_window_size))
        self._state_profile_window = deque(maxlen=window_size)
        self._fast_decision_lat_ms = []
        self._force_sync_success_lat_s = []

    def reset(self, scenario_info: Dict[str, Any] | None = None) -> None:  # noqa: D401
        self._global_step = 0
        self._scenario_info = dict(scenario_info) if isinstance(scenario_info, dict) else None
        self._rules.reset_to_fallback()
        self._trigger.reset()
        if self._perf_trigger is not None:
            self._perf_trigger.reset()
        if self._worker is not None:
            self._worker.reset()
        self._n_codegen_triggers = 0
        self._n_codegen_submitted = 0
        self._n_rule_switches = 0
        self._n_force_sync_calls = 0
        self._n_force_sync_success = 0
        self._force_sync_fail_streak = 0
        self._force_sync_next_allowed_step = 0
        self._force_sync_last_outcome = ""
        self._fast_decision_lat_ms = []
        self._force_sync_success_lat_s = []
        logger.info(
            "AsyncDualStreamAgent: reset called (has_worker={}, scenario_info_keys={})",
            bool(self._worker),
            list(self._scenario_info.keys()) if isinstance(self._scenario_info, dict) else [],
        )

    def act(
        self,
        obs: Dict[str, Any],
        legal_actions: List[Dict[str, Any]],
        env: Any,
    ) -> Optional[Dict[str, Any]]:
        if not legal_actions:
            return None
        use_fast_path = False
        if len(legal_actions) == 1:
            # Use the fast path only when there is no job-level or
            # machine-level choice left for the rule to make.
            mc = legal_actions[0].get("machine_candidates")
            num_mc = len(mc) if isinstance(mc, (list, tuple, set)) else 0
            if num_mc <= 1:
                use_fast_path = True
        if use_fast_path:
            current = self._rules.get_active_rule()
            logger.info(
                "AsyncDualStreamAgent: step={} using rule='{}' fast-path single legal action",
                self._global_step + 1,
                current.name,
            )
            self._global_step += 1
            self._update_state_profile_window(obs, env)
            self._update_performance_signal(env, obs)
            self._maybe_warm_start_from_repository(env)
            self._maybe_apply_new_rule()
            self._maybe_force_sync_codegen(env, obs, legal_actions)
            self._maybe_submit_task(env, obs, legal_actions)
            return legal_actions[0]
        self._global_step += 1
        self._update_state_profile_window(obs, env)
        self._update_performance_signal(env, obs)
        self._maybe_warm_start_from_repository(env)
        self._maybe_apply_new_rule()
        self._maybe_force_sync_codegen(env, obs, legal_actions)
        self._maybe_submit_task(env, obs, legal_actions)
        current = self._rules.get_active_rule()
        logger.debug(
            "AsyncDualStreamAgent: step={} using rule='{}' with {} legal actions",
            self._global_step,
            current.name,
            len(legal_actions),
        )
        t0 = time.perf_counter()
        try:
            action = choose_action_by_rule(
                current.rule,
                obs,
                legal_actions,
                env,
            )
        finally:
            dt_ms = (time.perf_counter() - t0) * 1000.0
            self._fast_decision_lat_ms.append(float(dt_ms))
        return action

    def _maybe_submit_task(
        self,
        env: Any,
        obs: Dict[str, Any],
        legal_actions: List[Dict[str, Any]],
    ) -> None:
        if self._worker is None:
            return
        if not self._trigger.should_trigger(self._global_step):
            return
        if self._perf_trigger is not None and self.cfg.use_performance_trigger:
            if not self._perf_trigger.should_trigger(self._global_step):
                return
        if not isinstance(env, DynaSchedEnv):
            return
        self._n_codegen_triggers += 1
        model: InputModel = env.model
        model_summary = self._build_model_summary(model)
        baseline = self._rules.get_active_rule()
        obs_payload = self._build_obs_payload(
            obs=obs,
            legal_actions=legal_actions,
            env=env,
            baseline_rule=baseline.rule,
        )
        logger.info(
            "AsyncDualStreamAgent: submitting LLMCoder task at step={} with baseline='{}'",
            self._global_step,
            baseline.name,
        )
        task = CoderTask(
            model=model,
            baseline_rule=baseline.rule,
            model_summary=model_summary,
            obs_example=obs_payload,
            baseline_name=baseline.name,
            step=self._global_step,
        )
        ok = self._worker.submit_task(task)
        if ok:
            self._n_codegen_submitted += 1

    def _maybe_apply_new_rule(self) -> None:
        if self._worker is None:
            return
        new_rule = self._worker.poll_ready_rule()
        if new_rule is None:
            return
        self._rules.update_rule(new_rule)
        self._n_rule_switches += 1
        logger.info(f"AsyncDualStreamAgent: switched active rule to {new_rule.name}")

    def _maybe_force_sync_codegen(
        self,
        env: Any,
        obs: Dict[str, Any],
        legal_actions: List[Dict[str, Any]],
    ) -> None:
        interval = int(self.cfg.force_sync_codegen_interval)
        if interval <= 0:
            return
        if not isinstance(env, DynaSchedEnv):
            return
        # Count only environment decision steps.
        if self._global_step < int(self.cfg.force_sync_codegen_min_step):
            return
        if self._global_step % interval != 0:
            return

        next_allowed = self._force_sync_next_allowed_step
        if self._global_step < next_allowed:
            logger.info(
                "AsyncDualStreamAgent: skipping force-sync codegen at step={} due to backoff (next_allowed_step={}, fail_streak={}, last_outcome='{}')",
                self._global_step,
                next_allowed,
                self._force_sync_fail_streak,
                self._force_sync_last_outcome,
            )
            self._append_force_sync_log(
                {
                    "event": "force_sync_skipped_backoff",
                    "step": self._global_step,
                    "next_allowed_step": next_allowed,
                    "fail_streak": self._force_sync_fail_streak,
                    "last_outcome": self._force_sync_last_outcome,
                }
            )
            return

        if isinstance(self._llm_client, NullLLMClient):
            return

        self._n_force_sync_calls += 1

        model: InputModel = env.model  # type: ignore[assignment]
        model_summary = self._build_model_summary(model)
        baseline = self._rules.get_active_rule()
        obs_payload = self._build_obs_payload(
            obs=obs,
            legal_actions=legal_actions,
            env=env,
            baseline_rule=baseline.rule,
        )

        self._append_force_sync_log(
            {
                "event": "force_sync_invoked",
                "step": self._global_step,
                "baseline_name": baseline.name,
            }
        )

        logger.info(
            "AsyncDualStreamAgent: force-sync codegen at step={} with baseline='{}'",
            self._global_step,
            baseline.name,
        )

        new_rule = self._run_sync_codegen_task(
            env,
            model,
            model_summary,
            obs_payload,
            baseline.rule,
            baseline.name,
        )
        if new_rule is None:
            self._force_sync_fail_streak += 1
            exp = min(max(self._force_sync_fail_streak - 1, 0), 3)
            multiplier = 2**exp
            if self._force_sync_last_outcome == "timeout":
                multiplier = min(multiplier * 2, 8)
            backoff_steps = int(max(1, interval) * multiplier)
            self._force_sync_next_allowed_step = self._global_step + backoff_steps
            logger.info(
                "AsyncDualStreamAgent: force-sync codegen at step={} produced no accepted rule (outcome='{}'); backing off for {} steps until step={}",
                self._global_step,
                self._force_sync_last_outcome,
                backoff_steps,
                self._force_sync_next_allowed_step,
            )
            self._append_force_sync_log(
                {
                    "event": "force_sync_backoff_scheduled",
                    "step": self._global_step,
                    "baseline_name": baseline.name,
                    "outcome": self._force_sync_last_outcome,
                    "fail_streak": self._force_sync_fail_streak,
                    "backoff_steps": backoff_steps,
                    "next_allowed_step": self._force_sync_next_allowed_step,
                }
            )
            return

        self._rules.update_rule(new_rule)
        self._n_rule_switches += 1
        self._n_force_sync_success += 1
        self._force_sync_fail_streak = 0
        cooldown_steps = int(max(1, interval) * 2)
        self._force_sync_next_allowed_step = self._global_step + cooldown_steps
        self._append_force_sync_log(
            {
                "event": "force_sync_rule_applied",
                "step": self._global_step,
                "baseline_name": baseline.name,
                "rule_name": new_rule.name,
            }
        )
        self._append_force_sync_log(
            {
                "event": "force_sync_cooldown_scheduled",
                "step": self._global_step,
                "cooldown_steps": cooldown_steps,
                "next_allowed_step": self._force_sync_next_allowed_step,
            }
        )
        logger.info(
            "AsyncDualStreamAgent: force-sync switched active rule to {} at step={}",
            new_rule.name,
            self._global_step,
        )

    def _run_sync_codegen_task(
        self,
        env: Any,
        model: InputModel,
        model_summary: Dict[str, Any],
        obs_example: Dict[str, Any],
        baseline_rule: Any,
        baseline_name: str,
    ) -> Optional[Any]:
        self._force_sync_last_outcome = ""
        if self._sync_coder is None:
            self._sync_coder = LLMCoder(self._llm_client, self.cfg)

        start_time = time.perf_counter()

        # Use the synchronous agentic path when the experiment asks for
        # multi-iteration search.
        max_iter = max(1, int(self.cfg.agentic_max_iterations))
        if max_iter > 1:
            return self._run_sync_agentic_task(
                env=env,
                model=model,
                model_summary=model_summary,
                obs_example=obs_example,
                baseline_rule=baseline_rule,
                baseline_name=baseline_name,
                start_time=start_time,
                max_iter=max_iter,
            )

        metric_main = str(self.cfg.objective_metric)

        candidates = self._sync_coder.build_candidates(
            model_summary=model_summary,
            obs_example=obs_example,
            baseline_name=baseline_name,
            objective_metric=metric_main,
        )

        num_candidates = len(candidates)
        if num_candidates == 0:
            self._force_sync_last_outcome = "no_candidates"
            logger.warning(
                "AsyncDualStreamAgent: force-sync codegen produced no valid candidate rule at step={}",
                self._global_step,
            )
            self._append_force_sync_log(
                {
                    "event": "force_sync_no_candidates",
                    "step": self._global_step,
                    "baseline_name": baseline_name,
                }
            )
            return None

        self._append_force_sync_log(
            {
                "event": "force_sync_candidates_generated",
                "step": self._global_step,
                "baseline_name": baseline_name,
                "num_candidates": num_candidates,
            }
        )

        best_rule = None
        best_res = None
        best_score = float("-inf")

        timed_out = False

        timeout = float(self.cfg.force_sync_codegen_timeout)

        events_pool, jms_pool, is_jms_backend = self._select_eval_backend(env, model)
        for cand in candidates:
            if timeout > 0.0:
                elapsed_now = time.perf_counter() - start_time
                if elapsed_now > timeout:
                    timed_out = True
                    logger.info(
                        "AsyncDualStreamAgent: force-sync codegen timeout after {:.3f} seconds at step={}",
                        elapsed_now,
                        self._global_step,
                    )
                    self._append_force_sync_log(
                        {
                            "event": "force_sync_timeout",
                            "step": self._global_step,
                            "baseline_name": baseline_name,
                            "elapsed_seconds": elapsed_now,
                        }
                    )
                    break
            if is_jms_backend and jms_pool is not None:
                res = evaluate_candidate_rule_jms(
                    baseline_rule=baseline_rule,
                    candidate_rule=cand.rule,
                    cfg=self.cfg,
                    events_pool=jms_pool,
                    objective_metric=metric_main,
                )
            else:
                res = evaluate_candidate_rule(
                    model=model,
                    baseline_rule=baseline_rule,
                    candidate_rule=cand.rule,
                    cfg=self.cfg,
                    events_pool=events_pool,
                    objective_metric=metric_main,
                )
            if res is None or not res.accepted:
                logger.info(
                    "AsyncDualStreamAgent: force-sync candidate '{}' rejected by sandbox eval at step={}",
                    cand.name,
                    self._global_step,
                )
                eval_dict: Dict[str, Any] = {}
                if res is not None:
                    eval_dict = _eval_result_dict(res)
                self._append_force_sync_log(
                    {
                        "event": "force_sync_candidate_evaluated",
                        "step": self._global_step,
                        "baseline_name": baseline_name,
                        "candidate": {
                            "name": cand.name,
                            "eval": eval_dict,
                            "accepted": False,
                        },
                    }
                )
                continue

            info = dict(cand.info or {})
            complexity_score = self._extract_complexity_score_from_info_local(info)
            normalized_complexity = math.log1p(max(complexity_score, 0.0))
            score = float(res.relative_improvement) - float(self.cfg.complexity_weight) * normalized_complexity

            logger.info(
                "AsyncDualStreamAgent: force-sync candidate '{}' accepted (rel_improve={:.6f}, complexity_score={:.6f}, combined_score={:.6f})",
                cand.name,
                res.relative_improvement,
                complexity_score,
                score,
            )

            eval_dict = _eval_result_dict(res)

            self._append_force_sync_log(
                {
                    "event": "force_sync_candidate_evaluated",
                    "step": self._global_step,
                    "baseline_name": baseline_name,
                    "candidate": {
                        "name": cand.name,
                        "eval": eval_dict,
                        "accepted": True,
                        "complexity_score": complexity_score,
                        "normalized_complexity": normalized_complexity,
                        "combined_score": score,
                    },
                }
            )

            if score > best_score:
                best_score = score
                best_res = res
                best_rule = cand

        if best_rule is None or best_res is None:
            self._force_sync_last_outcome = "timeout" if timed_out else "no_accepted"
            logger.info(
                "AsyncDualStreamAgent: force-sync codegen at step={} had all candidates rejected by sandbox eval",
                self._global_step,
            )
            self._append_force_sync_log(
                {
                    "event": "force_sync_rule_search_failed",
                    "step": self._global_step,
                    "baseline_name": baseline_name,
                }
            )
            return None

        elapsed = time.perf_counter() - start_time
        self._force_sync_last_outcome = "selected"
        logger.info(
            "AsyncDualStreamAgent: force-sync agentic best candidate '{}' selected (rel_improvement={:.6f}, combined_score={:.6f}) in {:.3f} seconds",
            best_rule.name,
            best_res.relative_improvement,
            best_score,
            elapsed,
        )
        self._append_force_sync_log(
            {
                "event": "force_sync_rule_selected",
                "step": self._global_step,
                "baseline_name": baseline_name,
                "rule_name": best_rule.name,
                "eval": _eval_result_dict(best_res, combined_score=best_score),
                "elapsed_seconds": elapsed,
            }
        )
        self._force_sync_success_lat_s.append(float(elapsed))
        eval_info = _eval_result_dict(best_res, combined_score=best_score)
        if self._repo is not None:
            info = dict(best_rule.info or {})
            info["eval"] = eval_info
            best_rule.info = info
            self._repo.add_from_rule(best_rule, model_summary)
        return best_rule

    def _run_sync_agentic_task(
        self,
        env: Any,
        model: InputModel,
        model_summary: Dict[str, Any],
        obs_example: Dict[str, Any],
        baseline_rule: Any,
        baseline_name: str,
        start_time: float,
        max_iter: int,
    ) -> Optional[Any]:
        if self._planner is None:
            self._planner = PlannerAgent(self._llm_client, self.cfg)
        if self._critic is None:
            self._critic = CriticAgent(self._llm_client, self.cfg)

        best_rule: Optional[Any] = None
        best_res: Optional[Any] = None
        best_score = float("-inf")
        total_candidates = 0
        timeout = float(self.cfg.force_sync_codegen_timeout)

        events_pool, jms_pool, is_jms_backend = self._select_eval_backend(env, model)

        timed_out = False
        had_no_candidates = False

        history: Dict[str, Any] = {}
        used_iterations = 0

        for it in range(max_iter):
            # Global timeout covers planning, generation, and evaluation.
            if timeout > 0.0:
                elapsed_now = time.perf_counter() - start_time
                if elapsed_now > timeout:
                    timed_out = True
                    logger.info(
                        "AsyncDualStreamAgent: force-sync agentic codegen timeout after {:.3f} seconds at step={} (iter={})",
                        elapsed_now,
                        self._global_step,
                        it,
                    )
                    self._append_force_sync_log(
                        {
                            "event": "force_sync_agentic_timeout",
                            "step": self._global_step,
                            "baseline_name": baseline_name,
                            "iteration": it,
                            "elapsed_seconds": elapsed_now,
                        }
                    )
                    break

            metric_main = str(self.cfg.objective_metric)

            try:
                plans = self._planner.plan_strategies(
                    model_summary=model_summary,
                    obs_example=obs_example,
                    baseline_name=baseline_name,
                    history=history,
                    objective_metric=metric_main,
                )
            except Exception as e:
                logger.error(
                    "AsyncDualStreamAgent: PlannerAgent error in force-sync agentic mode: {}",
                    e,
                )
                plans = []

            logger.debug(
                "AsyncDualStreamAgent: [force-sync agentic iter={}] planner produced {} plans: {}",
                it,
                len(plans),
                [p.name for p in plans],
            )

            candidates = self._sync_coder.build_candidates_from_plans(
                model_summary=model_summary,
                obs_example=obs_example,
                baseline_name=baseline_name,
                plans=plans,
                objective_metric=metric_main,
            )
            num_candidates = len(candidates)
            total_candidates += num_candidates
            logger.debug(
                "AsyncDualStreamAgent: [force-sync agentic iter={}] generated {} candidates from plans",
                it,
                num_candidates,
            )
            if not candidates:
                had_no_candidates = True
                logger.warning(
                    "AsyncDualStreamAgent: force-sync agentic iteration {} produced no valid candidate rule at step={}",
                    it,
                    self._global_step,
                )
                self._append_force_sync_log(
                    {
                        "event": "force_sync_agentic_no_candidates",
                        "step": self._global_step,
                        "baseline_name": baseline_name,
                        "iteration": it,
                    }
                )
                break

            scores: Dict[int, float] = {}
            candidate_summaries: List[Dict[str, Any]] = []
            eval_results: List[Optional[Any]] = []

            # Evaluate candidates sequentially, matching the single-pass path.
            for idx, cand in enumerate(candidates):
                if timeout > 0.0:
                    elapsed_now = time.perf_counter() - start_time
                    if elapsed_now > timeout:
                        timed_out = True
                        logger.info(
                            "AsyncDualStreamAgent: force-sync agentic codegen timeout after {:.3f} seconds at step={} (iter={}, cand_idx={})",
                            elapsed_now,
                            self._global_step,
                            it,
                            idx,
                        )
                        self._append_force_sync_log(
                            {
                                "event": "force_sync_agentic_timeout",
                                "step": self._global_step,
                                "baseline_name": baseline_name,
                                "iteration": it,
                                "candidate_index": idx,
                                "elapsed_seconds": elapsed_now,
                            }
                        )
                        break
                if is_jms_backend and jms_pool is not None:
                    res = evaluate_candidate_rule_jms(
                        baseline_rule=baseline_rule,
                        candidate_rule=cand.rule,
                        cfg=self.cfg,
                        events_pool=jms_pool,
                        objective_metric=metric_main,
                    )
                else:
                    res = evaluate_candidate_rule(
                        model=model,
                        baseline_rule=baseline_rule,
                        candidate_rule=cand.rule,
                        cfg=self.cfg,
                        events_pool=events_pool,
                        objective_metric=metric_main,
                    )
                eval_results.append(res)

            if timeout > 0.0:
                elapsed_now = time.perf_counter() - start_time
                if elapsed_now > timeout:
                    timed_out = True
                    break

            accepted_count = 0
            best_rel_improvement_accepted = float("-inf")
            for idx, cand in enumerate(candidates):
                res = eval_results[idx] if idx < len(eval_results) else None
                eval_dict: Dict[str, Any] = {}
                if res is not None:
                    eval_dict = _eval_result_dict(res)
                info = dict(cand.info or {})
                complexity_score = self._extract_complexity_score_from_info_local(info)
                if res is not None and res.accepted:
                    accepted_count += 1
                    rel_imp = float(res.relative_improvement)
                    if rel_imp > best_rel_improvement_accepted:
                        best_rel_improvement_accepted = rel_imp
                    normalized_complexity = math.log1p(max(complexity_score, 0.0))
                    score = float(res.relative_improvement) - float(self.cfg.complexity_weight) * normalized_complexity
                    scores[idx] = score
                    if score > best_score:
                        best_score = score
                        best_res = res
                        best_rule = cand
                    logger.info(
                        "AsyncDualStreamAgent: [force-sync agentic iter={}] candidate '{}' accepted by sandbox eval (rel_improve={:.6f}, complexity_score={:.6f}, combined_score={:.6f})",
                        it,
                        cand.name,
                        res.relative_improvement,
                        complexity_score,
                        score,
                    )
                else:
                    logger.info(
                        "AsyncDualStreamAgent: [force-sync agentic iter={}] candidate '{}' rejected by sandbox eval",
                        it,
                        cand.name,
                    )
                candidate_summaries.append(
                    {
                        "index": idx,
                        "name": cand.name,
                        "plan": info.get("plan"),
                        "complexity": info.get("complexity"),
                        "eval": eval_dict,
                    }
                )

            logger.debug(
                "AsyncDualStreamAgent: [force-sync agentic iter={}] candidate_summaries={}",
                it,
                candidate_summaries,
            )

            logger.info(
                "AsyncDualStreamAgent: [force-sync agentic iter={}] evaluated {} candidates (accepted={}, best_score_so_far={:.6f})",
                it,
                len(candidate_summaries),
                accepted_count,
                best_score,
            )

            history = {
                "iteration": it,
                "objective_metric": metric_main,
                "num_candidates": len(candidate_summaries),
                "best_score": best_score,
                "max_iterations": max_iter,
                "remaining_iterations": max(0, max_iter - (it + 1)),
                "agentic_min_relative_improvement": float(self.cfg.agentic_min_relative_improvement),
                "best_relative_improvement": (
                    float(best_rel_improvement_accepted)
                    if accepted_count > 0 and best_rel_improvement_accepted > float("-inf")
                    else None
                ),
                "accepted_count": int(accepted_count),
            }

            critic_info: Optional[Dict[str, Any]] = None
            continue_iterations = False
            critic_result = None
            agentic_threshold = float(self.cfg.agentic_min_relative_improvement)
            early_stop_triggered = (
                accepted_count > 0
                and best_rel_improvement_accepted > float("-inf")
                and float(best_rel_improvement_accepted) >= float(agentic_threshold)
            )
            if early_stop_triggered:
                logger.info(
                    "AsyncDualStreamAgent: [force-sync agentic iter={}] early-stop triggered (best_rel_improve={:.6f} >= threshold={:.6f}), skipping critic",
                    it,
                    float(best_rel_improvement_accepted),
                    float(agentic_threshold),
                )
                critic_info = {
                    "continue_iterations": False,
                    "feedbacks": [],
                    "early_stop": {
                        "best_rel_improve": float(best_rel_improvement_accepted),
                        "threshold": float(agentic_threshold),
                    },
                }
                continue_iterations = False
            else:
                try:
                    critic_result = self._critic.analyze(
                        baseline_name=baseline_name,
                        model_summary=model_summary,
                        candidate_summaries=candidate_summaries,
                        history=history,
                        objective_metric=metric_main,
                    )
                except Exception as e:
                    logger.error(
                        "AsyncDualStreamAgent: CriticAgent error in force-sync agentic mode: {}",
                        e,
                    )
                    critic_result = None

            if critic_result is not None:
                continue_iterations = bool(critic_result.continue_iterations)
                fb_list = [
                    {
                        "candidate_index": fb.candidate_index,
                        "candidate_name": fb.candidate_name,
                        "verdict": fb.verdict,
                        "reason": fb.reason,
                        "suggested_changes": dict(fb.suggested_changes),
                    }
                    for fb in critic_result.feedbacks
                ]
                critic_info = {
                    "continue_iterations": continue_iterations,
                    "feedbacks": fb_list,
                }

            logger.debug(
                "AsyncDualStreamAgent: [force-sync agentic iter={}] critic_info={}",
                it,
                critic_info,
            )

            logger.info(
                "AsyncDualStreamAgent: [force-sync agentic iter={}] critic continue_iterations={} ",
                it,
                continue_iterations,
            )

            self._append_force_sync_log(
                {
                    "event": "force_sync_agentic_iteration",
                    "mode": "agentic",
                    "step": self._global_step,
                    "iteration": it,
                    "baseline_name": baseline_name,
                    "num_candidates": len(candidate_summaries),
                    "num_accepted": accepted_count,
                    "best_score_so_far": best_score,
                    "scores": scores,
                    "candidates": candidate_summaries,
                    "critic": critic_info,
                }
            )

            used_iterations = it + 1
            if critic_result is None or not continue_iterations:
                break

        if best_rule is None or best_res is None:
            if timed_out:
                self._force_sync_last_outcome = "timeout"
            elif had_no_candidates:
                self._force_sync_last_outcome = "no_candidates"
            else:
                self._force_sync_last_outcome = "no_accepted"
            logger.info(
                "AsyncDualStreamAgent: force-sync agentic codegen at step={} produced no accepted rule",
                self._global_step,
            )
            self._append_force_sync_log(
                {
                    "event": "force_sync_agentic_rule_search_failed",
                    "step": self._global_step,
                    "baseline_name": baseline_name,
                }
            )
            return None

        elapsed = time.perf_counter() - start_time
        self._force_sync_last_outcome = "selected"
        agentic_summary: Dict[str, Any] = {
            "iterations": used_iterations,
            "num_candidates": total_candidates,
            "best_score": best_score,
        }
        logger.debug(
            "AsyncDualStreamAgent: force-sync agentic summary at step={} baseline='{}': {}",
            self._global_step,
            baseline_name,
            agentic_summary,
        )
        logger.info(
            "AsyncDualStreamAgent: force-sync agentic best candidate '{}' selected (rel_improvement={:.6f}, combined_score={:.6f}) in {:.3f} seconds",
            best_rule.name,
            best_res.relative_improvement,
            best_score,
            elapsed,
        )
        self._append_force_sync_log(
            {
                "event": "force_sync_agentic_rule_selected",
                "step": self._global_step,
                "baseline_name": baseline_name,
                "rule_name": best_rule.name,
                "eval": _eval_result_dict(best_res, combined_score=best_score),
                "agentic": agentic_summary,
                "elapsed_seconds": elapsed,
            }
        )
        self._force_sync_success_lat_s.append(float(elapsed))
        eval_info = _eval_result_dict(best_res, combined_score=best_score)
        if self._repo is not None:
            info = dict(best_rule.info or {})
            info["eval"] = eval_info
            info["agentic"] = dict(agentic_summary)
            best_rule.info = info
            self._repo.add_from_rule(best_rule, model_summary)
        return best_rule

    def _get_or_create_eval_pool(self, model: InputModel) -> EvalEventsPool:
        if self._eval_events_pool is not None:
            return self._eval_events_pool
        base_seed = int(model.meta.seed or 0)
        pool_size = int(self.cfg.eval_pool_size)
        self._eval_events_pool = EvalEventsPool(model, base_seed, pool_size)
        return self._eval_events_pool

    def _select_eval_backend(self, env: Any, model: InputModel) -> tuple[Optional[EvalEventsPool], Optional[JMSEvalPool], bool]:
        """Select the eval pool that matches the active simulator backend."""

        if isinstance(env, DynaSchedEnv) and getattr(env, "model", None) is None:
            jms_pool = self._get_or_create_jms_eval_pool(env)
            if jms_pool is None:
                logger.warning(
                    "AsyncDualStreamAgent: JMSSim backend detected but failed to create JMSEvalPool; sandbox eval disabled.",
                )
            return None, jms_pool, True
        return self._get_or_create_eval_pool(model), None, False

    def _get_or_create_jms_eval_pool(self, env: Any) -> Optional[JMSEvalPool]:
        """Create or reuse JMSEvalPool for JMSSim-backed environments.

        Non-JMS backends return None and continue through the InputModel-based
        EvalEventsPool path.
        """

        if self._jms_eval_pool is not None:
            return self._jms_eval_pool

        if not isinstance(env, DynaSchedEnv):
            return None

        try:
            from DynaSchedBench.Sim.JMSSnapshotAdapter import JMSSimBackend  # type: ignore[import]
        except Exception:
            return None

        sim_backend = getattr(env, "_sim", None)
        if not isinstance(sim_backend, JMSSimBackend):
            return None

        jms_sim = getattr(sim_backend, "_sim", None)
        static_info = getattr(jms_sim, "_static_info", None)
        if not isinstance(static_info, dict):
            return None

        suite = "jms"
        base_seed = 0

        payload = getattr(jms_sim, "_payload", None)
        if isinstance(payload, dict):
            meta = payload.get("meta")
            if isinstance(meta, dict):
                val_suite = meta.get("suite")
                if val_suite:
                    suite = str(val_suite)
                try:
                    if "seed" in meta and meta["seed"] is not None:
                        base_seed = int(meta["seed"])
                except Exception:
                    base_seed = 0

        # If payload metadata lacks a suite, infer it from the scenario path.
        if (not suite or suite == "jms") and isinstance(self._scenario_info, dict):
            cfg_path = self._scenario_info.get("config_path")
            if isinstance(cfg_path, str):
                parent_name = Path(cfg_path).parent.name
                if parent_name:
                    suite = parent_name

        pool_size = int(self.cfg.eval_pool_size)
        self._jms_eval_pool = JMSEvalPool(static_info, base_seed, pool_size, suite=suite)
        logger.info(
            "AsyncDualStreamAgent: created JMSEvalPool for suite='{}' (pool_size={}, base_seed={})",
            suite,
            pool_size,
            base_seed,
        )
        return self._jms_eval_pool

    @staticmethod
    def _extract_complexity_score_from_info_local(info: Dict[str, Any]) -> float:
        complexity = info.get("complexity")
        if not isinstance(complexity, dict):
            return 0.0
        value = complexity.get("complexity_score", 0.0)
        return float(value) if isinstance(value, (int, float)) else 0.0

    def _append_force_sync_log(self, record: Dict[str, Any]) -> None:
        self._traj_logger.append(record)

    def _get_force_sync_trajectory(self) -> List[Dict[str, Any]]:
        return self._traj_logger.to_list()

    def _update_performance_signal(self, env: Any, obs: Dict[str, Any]) -> None:
        if self._perf_trigger is None:
            return
        if not isinstance(env, DynaSchedEnv):
            return
        try:
            snap = env.get_snapshot()
        except Exception:
            return
        try:
            jobs = list(getattr(snap, "jobs", []) or [])
            completed = 0
            for j in jobs:
                status = getattr(j, "status", None)
                if status in ("completed", "cancelled"):
                    completed += 1
            t = float(getattr(snap, "time", 0.0) or 0.0)
            denom = t if abs(t) > 1e-6 else 1.0
            metric = completed / denom
        except Exception:
            return
        self._perf_trigger.update(metric)

    def _maybe_warm_start_from_repository(self, env: Any) -> None:
        if self._repo is None:
            return
        if self._repo_warm_started:
            return
        if not isinstance(env, DynaSchedEnv):
            self._repo_warm_started = True
            return
        try:
            model: InputModel = env.model
        except Exception:
            self._repo_warm_started = True
            return
        summary = self._build_model_summary(model)
        rule = self._repo.build_ensemble_for(summary)
        if rule is None:
            rule = self._repo.find_best_for(summary)
        self._repo_warm_started = True
        if rule is None:
            return
        self._rules.update_rule(rule)
        logger.info(
            "AsyncDualStreamAgent: warm-started active rule from repository as '{}'",
            rule.name,
        )

    def _build_model_summary(self, model: InputModel) -> Dict[str, Any]:
        meta = model.meta
        summary: Dict[str, Any] = {
            "num_jobs": len(model.jobs),
            "num_machines": len(model.machines),
            "run_name": meta.run_name,
            "seed": meta.seed,
            "horizon": meta.horizon,
        }
        if self._scenario_info and "config_path" in self._scenario_info:
            summary["config_path"] = self._scenario_info["config_path"]
        return summary

    def _build_obs_payload(
        self,
        *,
        obs: Dict[str, Any],
        legal_actions: List[Dict[str, Any]],
        env: Any,
        baseline_rule: Any,
    ) -> Dict[str, Any]:
        t_now = float(obs.get("time", 0.0))
        profile = self._build_state_profile(obs, env)
        action_sample = self._build_action_sample(
            obs=obs,
            legal_actions=legal_actions,
            env=env,
            baseline_rule=baseline_rule,
            top_k=30,
        )
        window_payload = self._build_state_profile_window_payload()
        return {
            "time": t_now,
            "state_profile": profile,
            "state_profile_window": window_payload,
            "action_sample": action_sample,
        }

    def _update_state_profile_window(self, obs: Dict[str, Any], env: Any) -> None:
        t_now = float(obs.get("time", 0.0))
        profile = self._build_state_profile(obs, env)

        def _get_scalar(p: Dict[str, Any], *keys: str) -> Optional[float]:
            cur: Any = p
            for k in keys:
                if not isinstance(cur, dict):
                    return None
                cur = cur.get(k)
            return finite_float(cur)

        scalars: Dict[str, float] = {}
        v = _get_scalar(profile, "num_ready_ops")
        if v is not None:
            scalars["num_ready_ops"] = v
        v = _get_scalar(profile, "dynamic_counts", "down_machines")
        if v is not None:
            scalars["down_machines"] = v
        v = _get_scalar(profile, "dynamic_counts", "emergency_jobs")
        if v is not None:
            scalars["emergency_jobs"] = v
        v = _get_scalar(profile, "ready_ops_stats", "process_time", "mean")
        if v is not None:
            scalars["ready_ops_process_time_mean"] = v
        v = _get_scalar(profile, "ready_ops_stats", "remaining_work", "mean")
        if v is not None:
            scalars["ready_ops_remaining_work_mean"] = v
        v = _get_scalar(profile, "machines_available_from", "mean")
        if v is not None:
            scalars["machines_available_from_mean"] = v

        self._state_profile_window.append(
            {
                "time": float(t_now),
                "state_profile": profile,
                "scalars": scalars,
            }
        )

    def _build_state_profile_window_payload(self) -> Dict[str, Any]:
        items = list(self._state_profile_window)
        n = len(items)
        if n <= 0:
            return {"window_size": 0, "sampled": [], "scalar_stats": {}}

        scalar_vals: Dict[str, List[float]] = {}
        for it in items:
            sc = it.get("scalars") if isinstance(it, dict) else None
            if not isinstance(sc, dict):
                continue
            for k, v in sc.items():
                fv = finite_float(v)
                if fv is None:
                    continue
                scalar_vals.setdefault(str(k), []).append(float(fv))

        scalar_stats = {k: numeric_stats(vs) for k, vs in scalar_vals.items()}
        sampled = even_sample(items, 12)
        sampled_compact: List[Dict[str, Any]] = []
        for it in sampled:
            if not isinstance(it, dict):
                continue
            sampled_compact.append(
                {
                    "time": it.get("time"),
                    "scalars": it.get("scalars") if isinstance(it.get("scalars"), dict) else {},
                }
            )
        return {
            "window_size": int(n),
            "sampled": sampled_compact,
            "scalar_stats": scalar_stats,
        }

    def _build_state_profile(self, obs: Dict[str, Any], env: Any) -> Dict[str, Any]:
        ready_ops = obs.get("ready_ops") if isinstance(obs, dict) else None
        if not isinstance(ready_ops, list):
            ready_ops = []
        machines = obs.get("machines") if isinstance(obs, dict) else None
        if not isinstance(machines, dict):
            machines = {}

        dyn = obs.get("dynamic_summary") if isinstance(obs, dict) else None
        if not isinstance(dyn, dict):
            dyn = {}
        down_machines = dyn.get("down_machines") if isinstance(dyn, dict) else None
        emergency_jobs = dyn.get("emergency_jobs") if isinstance(dyn, dict) else None
        events_info = dyn.get("events") if isinstance(dyn, dict) else None
        if not isinstance(down_machines, list):
            down_machines = []
        if not isinstance(emergency_jobs, list):
            emergency_jobs = []
        if not isinstance(events_info, dict):
            events_info = {}

        def _stats(vals: List[float]) -> Dict[str, Any]:
            if not vals:
                return {"count": 0}
            sample = even_sample(vals, 256)
            stats = numeric_stats(sample, include_sample_n=True)
            stats["count"] = int(len(vals))
            return stats

        proc_times: List[float] = []
        remaining_work: List[float] = []
        remaining_ops: List[float] = []
        flex: List[float] = []
        priorities: List[float] = []
        for ro in ready_ops:
            if not isinstance(ro, dict):
                continue
            for key, bucket in (
                ("process_time", proc_times),
                ("remaining_work", remaining_work),
                ("remaining_ops", remaining_ops),
                ("flexibility", flex),
                ("priority", priorities),
            ):
                value = finite_float(ro.get(key))
                if value is not None:
                    bucket.append(value)

        avail_times: List[float] = []
        for v in machines.values():
            value = finite_float(v)
            if value is not None:
                avail_times.append(value)

        events_top: Dict[str, int] = {}
        event_items = [(str(k), int(v)) for k, v in events_info.items() if isinstance(v, (int, float))]
        event_items.sort(key=lambda x: x[1], reverse=True)
        for k, v in event_items[:10]:
            events_top[k] = int(v)

        return {
            "num_ready_ops": int(len(ready_ops)),
            "num_machines": int(len(machines)),
            "ready_ops_stats": {
                "process_time": _stats(proc_times),
                "remaining_work": _stats(remaining_work),
                "remaining_ops": _stats(remaining_ops),
                "flexibility": _stats(flex),
                "priority": _stats(priorities),
            },
            "machines_available_from": _stats(avail_times),
            "dynamic_counts": {
                "down_machines": int(len(down_machines)),
                "emergency_jobs": int(len(emergency_jobs)),
            },
            "event_counters_top": events_top,
        }

    def _build_action_sample(
        self,
        *,
        obs: Dict[str, Any],
        legal_actions: List[Dict[str, Any]],
        env: Any,
        baseline_rule: Any,
        top_k: int,
    ) -> Dict[str, Any]:
        k = int(top_k)
        if k <= 0:
            k = 30
        n_actions = len(legal_actions)

        def _find_ready_op(job_id: str, machine_group: str) -> Dict[str, Any]:
            ready_ops: List[Dict[str, Any]] = obs.get("ready_ops", []) or []
            fallback: Optional[Dict[str, Any]] = None
            for ro in ready_ops:
                if str(ro.get("job_id")) != job_id:
                    continue
                if fallback is None:
                    fallback = ro
                if machine_group and str(ro.get("machine_group")) == machine_group:
                    return ro
            return fallback or {}

        def _summarize_action(a: Dict[str, Any], *, score: Optional[float]) -> Dict[str, Any]:
            jid = str(a.get("job_id"))
            mg = str(a.get("machine_group"))
            ro = _find_ready_op(jid, mg)
            cands = a.get("machine_candidates") or []
            if not isinstance(cands, list):
                cands = list(cands) if isinstance(cands, (tuple, set)) else []
            cands_total = len(cands)
            cands_preview = cands[:10]
            out: Dict[str, Any] = {
                "job_id": a.get("job_id"),
                "machine_group": a.get("machine_group"),
                "machine_candidates_total": int(cands_total),
                "machine_candidates": cands_preview,
                "process_time": ro.get("process_time"),
                "remaining_work": ro.get("remaining_work"),
                "remaining_ops": ro.get("remaining_ops"),
                "flexibility": ro.get("flexibility"),
                "priority": ro.get("priority"),
            }
            if score is not None:
                out["baseline_score"] = float(score)
            return out

        if n_actions <= k:
            return {
                "top_k": int(k),
                "num_legal_actions": int(n_actions),
                "scored": False,
                "actions": [_summarize_action(a, score=None) for a in legal_actions],
            }

        scored_items: List[tuple[float, Dict[str, Any]]] = []
        for base in legal_actions:
            cands = base.get("machine_candidates") or []
            if not isinstance(cands, list):
                cands = list(cands) if isinstance(cands, (tuple, set)) else []
            best = float("-inf")
            if not cands:
                try:
                    best = float(baseline_rule(obs, base, env))
                except Exception:
                    best = float("-inf")
            else:
                base_no_mid = dict(base)
                base_no_mid.pop("machine_id", None)
                for mid in cands:
                    a = dict(base_no_mid)
                    a["machine_id"] = mid
                    a["machine_candidates"] = cands
                    try:
                        s = float(baseline_rule(obs, a, env))
                    except Exception:
                        continue
                    if s > best:
                        best = s
            scored_items.append((best, base))

        scored_items.sort(key=lambda x: x[0], reverse=True)
        top = scored_items[:k]
        return {
            "top_k": int(k),
            "num_legal_actions": int(n_actions),
            "scored": True,
            "actions": [_summarize_action(a, score=s) for s, a in top],
        }

    def get_stats(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "num_steps": self._global_step,
            "num_codegen_triggers": self._n_codegen_triggers,
            "num_codegen_submitted": self._n_codegen_submitted,
            "num_rule_switches": self._n_rule_switches,
            "num_force_sync_calls": self._n_force_sync_calls,
            "num_force_sync_success": self._n_force_sync_success,
            "force_sync_fail_streak": self._force_sync_fail_streak,
            "force_sync_next_allowed_step": self._force_sync_next_allowed_step,
            "force_sync_last_outcome": self._force_sync_last_outcome,
        }
        # Summarize token counters exposed by the configured LLM client.
        llm_usage: Dict[str, Any] = {}
        client = self._llm_client
        for key in ("total_input_tokens", "total_output_tokens"):
            val = getattr(client, key, None)
            if val is not None:
                llm_usage[key] = int(val)
        base = getattr(client, "_base", None)
        if base is not None:
            for key in ("total_input_tokens", "total_output_tokens"):
                val = getattr(base, key, None)
                if val is not None:
                    llm_usage[key] = int(val)
        if llm_usage:
            data["llm_usage"] = llm_usage
        if self._fast_decision_lat_ms:
            fast_stats = numeric_stats(self._fast_decision_lat_ms)
            fast_stats["unit"] = "ms"
            data["fast_stream"] = fast_stats
        if self._force_sync_success_lat_s:
            slow_stats = numeric_stats(self._force_sync_success_lat_s)
            slow_stats["unit"] = "s"
            data["slow_stream"] = slow_stats
        traj = self._get_force_sync_trajectory()
        if traj:
            data["force_sync_trajectory"] = traj
        if self._worker is not None:
            data["worker"] = self._worker.get_stats()
        return data
