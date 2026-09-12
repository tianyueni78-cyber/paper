from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMCoderConfig:
    """Configuration for the asynchronous LLM coder.

    These fields control rule update triggers, sandbox evaluation budget,
    the objective metric, and LLM sampling parameters.
    """

    # Trigger and update schedule.
    max_steps_between_updates: int = 500
    force_sync_codegen_interval: int = 0
    force_sync_codegen_timeout: float = 600.0
    force_sync_codegen_min_step: int = 0

    # Minimum expected relative improvement, e.g. 0.05 means 5%.
    min_relative_improvement: float = 0.0

    # Sandbox evaluation budget.
    eval_max_steps: int = 500

    # Primary metric minimized during sandbox evaluation.
    objective_metric: str = "makespan"

    # LLM sampling parameters.
    llm_temperature: float = 0.0
    llm_top_p: float = 1.0
    llm_top_k: int = 0
    llm_timeout: float = 9999.0

    n_candidates: int = 3
    max_code_chars: int = 16000
    eval_min_episodes: int = 3
    eval_max_episodes: int = 20
    eval_pool_size: int = 32
    eval_significance_level: float = 0.05
    eval_min_effect_size: float = 0.0
    state_profile_window_size: int = 200
    complexity_weight: float = 0.1
    perf_trigger_window: int = 100
    perf_trigger_min_relative_change: float = 0.2
    use_performance_trigger: bool = True

    # Enable scenario-aware evaluation parameter tuning.
    use_meta_advisor: bool = True
    # Enable warm-start and persistent rule storage.
    use_repository: bool = True
    # Custom repository path. None uses RuleRepository's default location.
    repository_path: Optional[str] = None

    agentic_max_iterations: int = 2
    agentic_max_plans: int = 2
    agentic_min_relative_improvement: float = 0.02
    planner_temperature: float = 0.3
    critic_temperature: float = 0.0
