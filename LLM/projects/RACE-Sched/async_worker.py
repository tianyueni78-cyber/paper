from __future__ import annotations

import math
import queue
from dataclasses import dataclass
from threading import Thread
from typing import Any, Dict, Optional, List

from loguru import logger

from DynaSchedBench.Agents.utils import LLMClient
from DynaSchedBench.Gen import InputModel
from DynaSchedBench.Agents.LLMScheduler.logger import TrajectoryLogger

from .config import LLMCoderConfig
from .rules import PriorityRule, RuleWithMeta
from .coder import LLMCoder
from .sandbox_eval import evaluate_candidate_rule, EvalEventsPool
from .repository import RuleRepository
from .meta import MetaConfigAdvisor
from .explanation import build_rule_explanation, RefactorAgent
from .agentic import PlannerAgent, CriticAgent, TaskMemory, CandidateRecord


@dataclass
class CoderTask:
    model: InputModel
    baseline_rule: PriorityRule
    model_summary: Dict[str, Any]
    obs_example: Dict[str, Any]
    baseline_name: str
    step: int


class AsyncCoderWorker:
    def __init__(self, llm_client: LLMClient, cfg: LLMCoderConfig) -> None:
        self._cfg = cfg
        self._task_q: "queue.Queue[CoderTask]" = queue.Queue(maxsize=1)
        self._ready_q: "queue.Queue[RuleWithMeta]" = queue.Queue()
        self._coder = LLMCoder(llm_client, cfg)
        self._planner = PlannerAgent(llm_client, cfg)
        self._critic = CriticAgent(llm_client, cfg)
        self._n_tasks_processed = 0
        self._n_candidates_total = 0
        self._n_candidates_valid = 0
        self._n_eval_calls = 0
        self._n_rules_selected = 0
        self._n_rules_repo_added = 0
        self._last_best_eval: Dict[str, Any] = {}
        self._next_candidate_index: int = 0
        self._traj_logger = TrajectoryLogger()
        self._eval_events_pool: Optional[EvalEventsPool] = None
        self._repo = RuleRepository(path=cfg.repository_path) if cfg.use_repository else None
        self._meta = MetaConfigAdvisor() if cfg.use_meta_advisor else None
        # Explanation metadata is generated after acceptance and never changes
        # the executable rule path.
        self._refactor = RefactorAgent(llm_client, cfg)
        self._running = True
        self._thread = Thread(target=self._loop, daemon=True)
        logger.info("LLMCoder worker: starting background thread")
        self._thread.start()

    def reset(self) -> None:
        self._drain_queue(self._task_q)
        self._drain_queue(self._ready_q)
        self._n_tasks_processed = 0
        self._n_candidates_total = 0
        self._n_candidates_valid = 0
        self._n_eval_calls = 0
        self._n_rules_selected = 0
        self._n_rules_repo_added = 0
        self._last_best_eval = {}
        self._next_candidate_index = 0

    @staticmethod
    def _drain_queue(q: "queue.Queue[Any]") -> None:
        while not q.empty():
            q.get_nowait()

    def submit_task(self, task: CoderTask) -> bool:
        try:
            self._task_q.put(task, block=False)
            logger.info(
                f"LLMCoder worker: accepted task at step={task.step} baseline={task.baseline_name}"
            )
            return True
        except queue.Full:
            return False

    def poll_ready_rule(self) -> Optional[RuleWithMeta]:
        try:
            return self._ready_q.get_nowait()
        except queue.Empty:
            return None

    def _loop(self) -> None:
        while self._running:
            try:
                task = self._task_q.get(timeout=0.5)
            except queue.Empty:
                continue
            self._n_tasks_processed += 1
            try:
                logger.debug(
                    "LLMCoder worker: picked up task at step={} baseline='{}'",
                    task.step,
                    task.baseline_name,
                )
                self._handle_task(task)
            except Exception as e:  # pragma: no cover - defensive
                logger.error(f"LLMCoder worker: unexpected error while handling task: {e}")

    def _handle_task(self, task: CoderTask) -> None:
        if self._meta is not None:
            self._meta.tune_inplace(task.model_summary, self._cfg)
        max_iter = int(self._cfg.agentic_max_iterations)
        if max_iter <= 1:
            self._handle_task_single_pass(task)
        else:
            self._handle_task_agentic(task, max_iter)

    def _handle_task_single_pass(self, task: CoderTask) -> None:
        metric_main = str(self._cfg.objective_metric)
        candidates = self._coder.build_candidates(
            model_summary=task.model_summary,
            obs_example=task.obs_example,
            baseline_name=task.baseline_name,
            objective_metric=metric_main,
        )
        num_candidates = len(candidates)
        self._n_candidates_total += num_candidates
        if not candidates:
            logger.warning("LLMCoder worker: no valid candidate rule generated")
            return
        best_rule: Optional[RuleWithMeta] = None
        best_res = None
        best_score = float("-inf")
        events_pool = self._get_or_create_eval_pool(task.model)
        for cand in candidates:
            self._n_eval_calls += 1
            res = evaluate_candidate_rule(
                model=task.model,
                baseline_rule=task.baseline_rule,
                candidate_rule=cand.rule,
                cfg=self._cfg,
                events_pool=events_pool,
                objective_metric=metric_main,
            )
            eval_dict: Dict[str, Any] = {}
            if res is not None:
                eval_dict = {
                    "baseline_value": res.baseline_value,
                    "candidate_value": res.candidate_value,
                    "relative_improvement": res.relative_improvement,
                    "accepted": res.accepted,
                    "episodes_used": res.episodes_used,
                    "effect_size": res.effect_size,
                }
            if res is None or not res.accepted:
                logger.info(
                    "LLMCoder worker: candidate '{}' rejected by sandbox eval",
                    cand.name,
                )
                self._append_log(
                    {
                        "event": "candidate_evaluated",
                        "mode": "single_pass",
                        "step": task.step,
                        "baseline_name": task.baseline_name,
                        "candidate": {
                            "name": cand.name,
                            "eval": eval_dict,
                            "accepted": False,
                        },
                    }
                )
                continue
            self._n_candidates_valid += 1
            info = dict(cand.info)
            complexity_score = self._extract_complexity_score_from_info(info)
            normalized_complexity = math.log1p(max(complexity_score, 0.0))
            score = float(res.relative_improvement) - float(self._cfg.complexity_weight) * normalized_complexity
            logger.info(
                "LLMCoder worker: candidate '{}' accepted by sandbox eval (rel_improve={:.6f}, complexity_score={:.6f}, normalized_complexity={:.6f}, combined_score={:.6f})",
                cand.name,
                res.relative_improvement,
                complexity_score,
                normalized_complexity,
                score,
            )
            self._append_log(
                {
                    "event": "candidate_evaluated",
                    "mode": "single_pass",
                    "step": task.step,
                    "baseline_name": task.baseline_name,
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
                best_rule = RuleWithMeta(rule=cand.rule, name=cand.name, info=info)
        logger.debug(
            "LLMCoder worker: after evaluation loop best_rule={} best_score={:.6f}",
            best_rule.name if best_rule is not None else None,
            best_score,
        )
        if best_rule is None or best_res is None:
            logger.info("LLMCoder worker: all candidate rules rejected by sandbox eval")
            self._append_log(
                {
                    "event": "rule_search_failed",
                    "mode": "single_pass",
                    "step": task.step,
                    "baseline_name": task.baseline_name,
                }
            )
            return
        self._finalize_and_enqueue_best(task, best_rule, best_res, best_score, agentic_summary=None)

    def _handle_task_agentic(self, task: CoderTask, max_iter: int) -> None:
        memory = TaskMemory()
        history: Dict[str, Any] = {}
        best_rule: Optional[RuleWithMeta] = None
        best_res = None
        best_score = float("-inf")
        for it in range(max_iter):
            memory.iteration = it
            metric_main = str(self._cfg.objective_metric)
            try:
                plans = self._planner.plan_strategies(
                    model_summary=task.model_summary,
                    obs_example=task.obs_example,
                    baseline_name=task.baseline_name,
                    history=history,
                    objective_metric=metric_main,
                )
            except Exception as e:
                logger.error(f"LLMCoder worker: PlannerAgent error: {e}")
                plans = []
            logger.debug(
                "LLMCoder worker: [agentic iter=%d] planner produced %d plans: %s",
                it,
                len(plans),
                [p.name for p in plans],
            )
            candidates = self._coder.build_candidates_from_plans(
                model_summary=task.model_summary,
                obs_example=task.obs_example,
                baseline_name=task.baseline_name,
                plans=plans,
                objective_metric=metric_main,
            )
            num_candidates = len(candidates)
            self._n_candidates_total += num_candidates
            logger.debug(
                "LLMCoder worker: [agentic iter=%d] generated %d candidates from plans",
                it,
                num_candidates,
            )
            if not candidates:
                logger.warning("LLMCoder worker: no valid candidate rule generated in agentic iteration %d", it)
                break
            records: List[CandidateRecord] = []
            scores: Dict[int, float] = {}
            candidate_summaries: List[Dict[str, Any]] = []
            accepted_count = 0
            best_rel_improvement_accepted = float("-inf")
            events_pool = self._get_or_create_eval_pool(task.model)
            entries: List[CandidateRecord] = []
            for cand in candidates:
                idx = self._next_candidate_index
                self._next_candidate_index += 1
                rec = CandidateRecord(index=idx, rule=cand, iteration=it)
                entries.append(rec)

            for rec, cand in zip(entries, candidates):
                self._n_eval_calls += 1
                res = evaluate_candidate_rule(
                    model=task.model,
                    baseline_rule=task.baseline_rule,
                    candidate_rule=cand.rule,
                    cfg=self._cfg,
                    events_pool=events_pool,
                    objective_metric=metric_main,
                )
                records.append(rec)
                rec.eval_result = res
                info = dict(cand.info)
                eval_dict: Dict[str, Any] = {}
                if res is not None:
                    eval_dict = {
                        "baseline_value": res.baseline_value,
                        "candidate_value": res.candidate_value,
                        "relative_improvement": res.relative_improvement,
                        "accepted": res.accepted,
                        "episodes_used": res.episodes_used,
                        "effect_size": res.effect_size,
                    }
                complexity_score = self._extract_complexity_score_from_info(info)
                if res is not None and res.accepted:
                    self._n_candidates_valid += 1
                    accepted_count += 1
                    rel_imp = float(res.relative_improvement)
                    if rel_imp > best_rel_improvement_accepted:
                        best_rel_improvement_accepted = rel_imp
                    normalized_complexity = math.log1p(max(complexity_score, 0.0))
                    score = float(res.relative_improvement) - float(self._cfg.complexity_weight) * normalized_complexity
                    scores[rec.index] = score
                    if score > best_score:
                        best_score = score
                        best_res = res
                        best_rule = RuleWithMeta(rule=cand.rule, name=cand.name, info=info)
                    logger.info(
                        "LLMCoder worker: [iter=%d] candidate '%s' accepted by sandbox eval (rel_improve={:.6f}, complexity_score={:.6f}, combined_score={:.6f})",
                        it,
                        cand.name,
                        res.relative_improvement,
                        complexity_score,
                        score,
                    )
                else:
                    logger.info(
                        "LLMCoder worker: [iter=%d] candidate '%s' rejected by sandbox eval",
                        it,
                        cand.name,
                    )
                candidate_summaries.append(
                    {
                        "index": rec.index,
                        "name": cand.name,
                        "plan": info.get("plan"),
                        "complexity": info.get("complexity"),
                        "eval": eval_dict,
                    }
                )
            memory.add_candidates(records)
            logger.debug(
                "LLMCoder worker: [agentic iter=%d] candidate_summaries=%s",
                it,
                candidate_summaries,
            )
            memory.update_best_by_score(scores)
            history = {
                "iteration": it,
                "num_candidates": len(records),
                "best_score": best_score,
                "objective_metric": metric_main,
                "max_iterations": max_iter,
                "remaining_iterations": max(0, max_iter - (it + 1)),
                "agentic_min_relative_improvement": float(self._cfg.agentic_min_relative_improvement),
                "best_relative_improvement": (
                    float(best_rel_improvement_accepted)
                    if best_rel_improvement_accepted > float("-inf")
                    else None
                ),
                "accepted_count": int(accepted_count),
            }
            critic_result = None
            agentic_threshold = float(self._cfg.agentic_min_relative_improvement)
            early_stop_triggered = (
                accepted_count > 0
                and best_rel_improvement_accepted > float("-inf")
                and float(best_rel_improvement_accepted) >= float(agentic_threshold)
            )
            if early_stop_triggered:
                logger.info(
                    "LLMCoder worker: [agentic iter=%d] early-stop triggered (best_rel_improve=%.6f >= threshold=%.6f), skipping critic",
                    it,
                    float(best_rel_improvement_accepted),
                    float(agentic_threshold),
                )
            else:
                try:
                    critic_result = self._critic.analyze(
                        baseline_name=task.baseline_name,
                        model_summary=task.model_summary,
                        candidate_summaries=candidate_summaries,
                        history=history,
                        objective_metric=metric_main,
                    )
                except Exception as e:
                    logger.error(f"LLMCoder worker: CriticAgent error: {e}")
                    critic_result = None

            critic_info: Optional[Dict[str, Any]] = None
            if early_stop_triggered:
                critic_info = {
                    "continue_iterations": False,
                    "feedbacks": [],
                    "early_stop": {
                        "best_rel_improve": float(best_rel_improvement_accepted),
                        "threshold": float(agentic_threshold),
                    },
                }
            if critic_result is not None:
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
                    "continue_iterations": bool(critic_result.continue_iterations),
                    "feedbacks": fb_list,
                }

            logger.debug(
                "LLMCoder worker: [agentic iter=%d] critic_info=%s",
                it,
                critic_info,
            )

            self._append_log(
                {
                    "event": "agentic_iteration",
                    "mode": "agentic",
                    "step": task.step,
                    "iteration": it,
                    "baseline_name": task.baseline_name,
                    "num_candidates": len(records),
                    "best_score_so_far": best_score,
                    "scores": scores,
                    "candidates": candidate_summaries,
                    "critic": critic_info,
                }
            )
            if early_stop_triggered or critic_result is None or not critic_result.continue_iterations:
                break
        if best_rule is None or best_res is None:
            logger.info("LLMCoder worker: no accepted candidate rule after agentic iterations")
            self._append_log(
                {
                    "event": "rule_search_failed",
                    "mode": "agentic",
                    "step": task.step,
                    "baseline_name": task.baseline_name,
                }
            )
            return
        agentic_summary: Dict[str, Any] = {
            "iterations": memory.iteration + 1,
            "num_candidates": len(memory.candidates),
            "best_score": best_score,
        }
        logger.debug(
            "LLMCoder worker: agentic summary at step=%s baseline='%s': %s",
            task.step,
            task.baseline_name,
            agentic_summary,
        )
        self._finalize_and_enqueue_best(task, best_rule, best_res, best_score, agentic_summary=agentic_summary)

    def _extract_complexity_score_from_info(self, info: Dict[str, Any]) -> float:
        complexity = info.get("complexity")
        if not isinstance(complexity, dict):
            return 0.0
        value = complexity.get("complexity_score", 0.0)
        return float(value) if isinstance(value, (int, float)) else 0.0

    def _finalize_and_enqueue_best(
        self,
        task: CoderTask,
        best_rule: RuleWithMeta,
        best_res: Any,
        best_score: float,
        agentic_summary: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._n_rules_selected += 1
        eval_info: Dict[str, Any] = {
            "baseline_value": best_res.baseline_value,
            "candidate_value": best_res.candidate_value,
            "relative_improvement": best_res.relative_improvement,
            "episodes_used": best_res.episodes_used,
            "effect_size": best_res.effect_size,
            "combined_score": best_score,
        }
        self._last_best_eval = dict(eval_info)
        info = dict(best_rule.info)
        info["eval"] = eval_info
        if agentic_summary is not None:
            info["agentic"] = dict(agentic_summary)
        try:
            explanation = self._refactor.explain(best_rule, eval_info=eval_info)
        except Exception:
            explanation = build_rule_explanation(best_rule)
        if isinstance(explanation, dict):
            info["explanation"] = explanation
        best_rule.info = info
        self._append_log(
            {
                "event": "rule_selected",
                "step": task.step,
                "baseline_name": task.baseline_name,
                "rule_name": best_rule.name,
                "eval": eval_info,
                "agentic": agentic_summary,
                "model_summary": task.model_summary,
            }
        )
        if self._repo is not None:
            logger.debug(
                "LLMCoder worker: calling RuleRepository.add_from_rule for '{}'",
                best_rule.name,
            )
            self._repo.add_from_rule(best_rule, task.model_summary)
            self._n_rules_repo_added += 1
            logger.debug(
                "LLMCoder worker: RuleRepository.add_from_rule completed for '{}'",
                best_rule.name,
            )
        logger.info(
            "LLMCoder worker: best candidate '{}' selected (rel_improvement={:.6f}, combined_score={:.6f}), enqueuing for hot-swap",
            best_rule.name,
            best_res.relative_improvement,
            best_score,
        )
        self._ready_q.put(best_rule)

    def _get_or_create_eval_pool(self, model: InputModel) -> EvalEventsPool:
        if self._eval_events_pool is not None:
            return self._eval_events_pool
        base_seed = int(model.meta.seed or 0)
        pool_size = int(self._cfg.eval_pool_size)
        self._eval_events_pool = EvalEventsPool(model, base_seed, pool_size)
        return self._eval_events_pool

    def _append_log(self, record: Dict[str, Any]) -> None:
        self._traj_logger.append(record)

    def get_trajectory(self) -> List[Dict[str, Any]]:
        return self._traj_logger.to_list()

    def get_stats(self) -> Dict[str, Any]:
        return {
            "num_tasks_processed": self._n_tasks_processed,
            "num_candidates_total": self._n_candidates_total,
            "num_candidates_accepted": self._n_candidates_valid,
            "num_eval_calls": self._n_eval_calls,
            "num_rules_selected": self._n_rules_selected,
            "num_rules_repo_added": self._n_rules_repo_added,
            "last_best_eval": self._last_best_eval,
            "trajectory": self.get_trajectory(),
        }
