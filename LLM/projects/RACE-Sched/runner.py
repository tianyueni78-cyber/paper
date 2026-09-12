from __future__ import annotations 

import json
import time
from pathlib import Path
from typing import Any, Dict, Optional, Union

from dotenv import load_dotenv

load_dotenv()

from DynaSchedBench.Env import DynaSchedEnv
from DynaSchedBench.Eval.Metrics import evaluate_trajectory
from DynaSchedBench.Agents.utils import (
    LLMClient,
    NullLLMClient,
    OpenAICompatClient,
    RetryingLLMClient,
    resolve_llm_endpoint,
)
from DynaSchedBench.Agents.LLMScheduler.config import ModelConfig
from DynaSchedBench.Agents.LLMScheduler.sampler import choose_by_env_score

from .agent import AsyncDualStreamAgent
from .config import LLMCoderConfig


def _get_client(model_cfg: Optional[ModelConfig] = None) -> LLMClient:
    """Construct an LLM client using the shared ModelConfig-based builder.

    When no ModelConfig is provided, environment variables fill the provider
    and model fields in the same way as the LLMScheduler runner.
    """
    import os

    cfg = model_cfg or ModelConfig()

    provider = str(cfg.provider or os.getenv("DYNA_SCHEDBENCH_LLM_PROVIDER") or "openai").lower()
    model = cfg.model_name or os.getenv("DYNA_SCHEDBENCH_LLM_MODEL")

    base_url_override = cfg.base_url
    api_key, base_url = resolve_llm_endpoint(provider, base_url_override)

    timeout = float(cfg.request_timeout or 30.0)
    max_tokens = int(cfg.max_tokens or 512)

    if not api_key or not model:
        return NullLLMClient()

    base_client = OpenAICompatClient(
        api_key=api_key,
        model=model,
        base_url=base_url,
        max_tokens=max_tokens,
        timeout=timeout,
    )
    return RetryingLLMClient(base_client)


def _dump_agent_trajectory_jsonl(
    agent_stats: Dict[str, Any],
    trajectory_path: Union[str, Path],
) -> str:
    """Write worker and force-sync trajectory events as JSONL."""

    from DynaSchedBench.Agents.LLMScheduler.logger import TrajectoryLogger

    worker = agent_stats.get("worker") if isinstance(agent_stats, dict) else None
    traj_events = []
    if isinstance(worker, dict):
        val = worker.get("trajectory")
        if isinstance(val, list):
            traj_events = [x for x in val if isinstance(x, dict)]

    force_sync_events = []
    if isinstance(agent_stats, dict):
        val_fs = agent_stats.get("force_sync_trajectory")
        if isinstance(val_fs, list):
            force_sync_events = [x for x in val_fs if isinstance(x, dict)]

    logger_obj = TrajectoryLogger()
    for rec in [*traj_events, *force_sync_events]:
        logger_obj.append(rec)

    path = Path(trajectory_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    logger_obj.dump_jsonl(path)
    return str(path)


def solve_jms_instance(
    instance_path: Union[str, Path],
    cfg: Optional[LLMCoderConfig] = None,
    output_path: Optional[Union[str, Path]] = None,
    trajectory_path: Optional[Union[str, Path]] = None,
    model_cfg: Optional[ModelConfig] = None,
) -> Dict[str, Any]:
    """Run LLMCoder on a JMS/GEN-Bench JSONL instance."""

    cfg = cfg or LLMCoderConfig()

    client = _get_client(model_cfg)

    instance_path = Path(instance_path)
    if not instance_path.is_file():
        raise FileNotFoundError(f"JMS/GEN-Bench JSONL instance not found: {instance_path}")

    env = DynaSchedEnv.from_jms_jsonl(instance_path, track_trajectory=True)

    agent = AsyncDualStreamAgent(llm_client=client, cfg=cfg)
    scenario_info: Dict[str, Any] = {"config_path": str(instance_path)}
    agent.reset(scenario_info=scenario_info)

    obs = env.reset()
    done = env.done()
    steps = 0
    max_steps = env.total_operations() * 4 + 1000

    start_time_wall = time.perf_counter()

    while not done and steps < max_steps:
        legal = env.legal_actions()
        if not legal:
            obs = env.advance_if_idle()
            done = env.done()
            continue
        act = agent.act(obs, legal, env)
        if act is None:
            # Fall back to the environment scorer; if it also cannot choose,
            # advance the simulation clock.
            act = choose_by_env_score(legal, env, rollout_steps=0)
            if act is None:
                obs = env.advance_if_idle()
                done = env.done()
                continue
        obs, _, done, _ = env.step(act)
        steps += 1

    traj = env.get_trajectory()
    end_time_wall = time.perf_counter()
    runtime_seconds = float(end_time_wall - start_time_wall)
    metrics = evaluate_trajectory(traj)
    metrics["runtime_seconds"] = float(runtime_seconds)

    sim = getattr(env, "_sim", None)
    gantt = sim.get_gantt() if sim is not None and hasattr(sim, "get_gantt") else []

    agent_stats = agent.get_stats()

    if agent_stats:
        metrics["agent_stats"] = agent_stats

    result: Dict[str, Any] = {
        "algorithm": "llm-coder-jms",
        "gantt": gantt,
        "metrics": metrics,
        "agent_stats": agent_stats,
        "policy_stats": agent_stats,
    }

    if trajectory_path is not None:
        result["trajectory_log_path"] = _dump_agent_trajectory_jsonl(
            agent_stats,
            trajectory_path,
        )

    if output_path is not None:
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

    return result
