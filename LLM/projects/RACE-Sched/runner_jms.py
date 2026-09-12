from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from DynaSchedBench.Agents.LLMScheduler.config import ModelConfig
from DynaSchedBench.Logging import init_logging

from .config import LLMCoderConfig
from .runner import solve_jms_instance
from .runner_utils import apply_config_overrides


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run LLMCoder on a JMS/GEN-Bench JSONL instance using JMSSim backend. "
            "This is a thin CLI wrapper around solve_jms_instance, intended "
            "for reproducible runs over data/jmsbench and data/genbench."
        )
    )

    parser.add_argument(
        "--instance-file",
        type=str,
        required=True,
        help="Path to a JMSBench/GEN-Bench style JSONL instance (static_info + dynamic_events).",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output directory; metrics.json, gantt.json, and llmcoder_trajectory.jsonl will be written here.",
    )
    # LLM connection parameters (mirrors A.run subset).
    parser.add_argument("--llm-provider", type=str, default=None, help="LLM HTTP provider (e.g. chatanywhere, openai).")
    parser.add_argument("--llm-model", type=str, default=None, help="Override LLM model name.")
    parser.add_argument("--llm-base-url", type=str, default=None, help="Override LLM HTTP base URL.")
    parser.add_argument("--llm-temperature", type=float, default=None, help="Sampling temperature for LLM calls.")
    parser.add_argument("--llm-timeout", type=float, default=None, help="Timeout seconds for LLM HTTP requests.")

    # LLMCoder-specific options (subset used by the bash scripts).
    parser.add_argument("--llm-coder-eval-max-steps", type=int, default=None)
    parser.add_argument("--llm-coder-max-steps-between-updates", type=int, default=None)
    parser.add_argument("--llm-coder-min-relative-improvement", type=float, default=None)

    parser.add_argument("--llm-coder-force-sync-interval", type=int, default=0)
    parser.add_argument("--llm-coder-force-sync-timeout", type=float, default=600.0)
    parser.add_argument("--llm-coder-force-sync-min-step", type=int, default=0)

    parser.add_argument("--llm-coder-eval-pool-size", type=int, default=None)

    parser.add_argument("--llm-coder-eval-min-episodes", type=int, default=None)
    parser.add_argument("--llm-coder-eval-max-episodes", type=int, default=None)
    parser.add_argument("--llm-coder-eval-significance-level", type=float, default=None)

    parser.add_argument("--llm-coder-agentic-max-iterations", type=int, default=None)

    parser.add_argument(
        "--llm-coder-use-repository",
        dest="llm_coder_use_repository",
        action="store_true",
        default=True,
        help="Enable the rule repository (warm-start and persistence).",
    )
    parser.add_argument(
        "--no-llm-coder-use-repository",
        dest="llm_coder_use_repository",
        action="store_false",
        help="Disable the rule repository (cold start, no persistence).",
    )
    parser.add_argument(
        "--llm-coder-use-meta-advisor",
        dest="llm_coder_use_meta_advisor",
        action="store_true",
        default=True,
        help="Enable MetaConfigAdvisor for automatic eval parameter tuning.",
    )
    parser.add_argument(
        "--no-llm-coder-use-meta-advisor",
        dest="llm_coder_use_meta_advisor",
        action="store_false",
        help="Disable MetaConfigAdvisor and use raw LLMCoderConfig settings.",
    )
    parser.add_argument(
        "--no-llm-coder-use-performance-trigger",
        dest="llm_coder_use_performance_trigger",
        action="store_false",
        default=True,
        help="Disable performance-based trigger gating for codegen.",
    )

    return parser.parse_args()


def _build_llmcoder_config(args: argparse.Namespace) -> LLMCoderConfig:
    cfg = LLMCoderConfig()

    apply_config_overrides(
        cfg,
        {
            "llm_temperature": (args.llm_temperature, float),
            "eval_max_steps": (args.llm_coder_eval_max_steps, int),
            "max_steps_between_updates": (args.llm_coder_max_steps_between_updates, int),
            "min_relative_improvement": (args.llm_coder_min_relative_improvement, float),
            "eval_pool_size": (args.llm_coder_eval_pool_size, int),
            "eval_min_episodes": (args.llm_coder_eval_min_episodes, int),
            "eval_max_episodes": (args.llm_coder_eval_max_episodes, int),
            "eval_significance_level": (args.llm_coder_eval_significance_level, float),
            "agentic_max_iterations": (args.llm_coder_agentic_max_iterations, int),
            "force_sync_codegen_interval": (args.llm_coder_force_sync_interval, int),
            "force_sync_codegen_timeout": (args.llm_coder_force_sync_timeout, float),
            "force_sync_codegen_min_step": (args.llm_coder_force_sync_min_step, int),
        },
    )
    cfg.use_repository = bool(args.llm_coder_use_repository)
    cfg.use_meta_advisor = bool(args.llm_coder_use_meta_advisor)
    cfg.use_performance_trigger = bool(args.llm_coder_use_performance_trigger)

    return cfg


def _build_model_config(args: argparse.Namespace) -> ModelConfig:
    provider = args.llm_provider or "none"
    model_name = args.llm_model
    base_url = args.llm_base_url
    timeout = float(args.llm_timeout) if args.llm_timeout is not None else 30.0
    return ModelConfig(provider=provider, model_name=model_name, base_url=base_url, request_timeout=timeout)


def main() -> None:
    args = _parse_args()

    instance_path = Path(args.instance_file)
    if not instance_path.is_file():
        raise SystemExit(f"JMS/GEN-Bench JSONL instance not found: {instance_path}")

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Initialize logging so that this script behaves like the Agents CLI:
    # logs/A/run_jms/<timestamp>_A_run_jms[_runid]/{main.log,sandbox_eval.log}
    run_id = instance_path.stem

    init_logging(
        component="A",
        command="run_jms",
        log_level="INFO",
        run_id=run_id,
    )

    cfg = _build_llmcoder_config(args)
    model_cfg = _build_model_config(args)

    metrics_path = out_dir / "metrics.json"
    traj_log_path = out_dir / "llmcoder_trajectory.jsonl"

    result = solve_jms_instance(
        instance_path=instance_path,
        cfg=cfg,
        output_path=metrics_path,
        trajectory_path=traj_log_path,
        model_cfg=model_cfg,
    )

    # Also write gantt.json alongside metrics.json for convenience.
    gantt_path = out_dir / "gantt.json"
    gantt_path.write_text(json.dumps(result.get("gantt", []), indent=2, ensure_ascii=False), encoding="utf-8")

    # Print metrics to stdout for quick inspection / logging pipelines.
    metrics: Any = result.get("metrics", result)
    print(json.dumps(metrics, indent=2, ensure_ascii=False))


if __name__ == "__main__":  # pragma: no cover
    main()
