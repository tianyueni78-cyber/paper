# RACE-Sched

RACE-Sched is a DynaSchedBench agent that uses an LLM to synthesize Python
dispatching priority rules for dynamic job-shop scheduling. The active rule is
used online for fast decisions, while candidate rules are generated and
evaluated in a slower search path before they are allowed to replace the
current policy.

## Core Idea

At each decision point, DynaSchedBench provides an observation, legal actions,
and simulator state. RACE-Sched represents a scheduling policy as:

```python
def optimized_priority(obs, action, env) -> float:
    ...
```

Every legal action is scored by this function, and the highest score is chosen.
The default rule is SPT. When an LLM is configured, RACE-Sched periodically asks
the model to propose new `optimized_priority` implementations, evaluates them
against the current baseline in sandbox rollouts, and hot-swaps an accepted
candidate into the online agent.

## Files

- `config.py`: configuration for generation triggers, evaluation budget, LLM
  sampling, repository usage, and agentic search.
- `rules.py`: priority-rule protocol, SPT baseline, active-rule manager, and
  action selection.
- `agent.py`: `AsyncDualStreamAgent`, which owns the online scheduling loop,
  force-sync generation path, async worker, repository warm-start, and stats.
- `async_worker.py`: background rule generation and evaluation worker used by
  the performance-triggered path.
- `coder.py`: prompt construction, LLM output parsing, generated-code
  compilation, and simple code-complexity analysis.
- `compile.py`: restricted compilation environment for generated priority
  functions.
- `agentic.py`: planner and critic agents for multi-iteration rule refinement.
- `sandbox_eval.py`: paired baseline/candidate sandbox evaluation for both
  InputModel-backed and JMSSim-backed environments.
- `repository.py`: persistent storage, retrieval, and ensemble warm-start for
  accepted generated rules.
- `meta.py`: scenario-aware tuning of evaluation budgets and candidate counts.
- `explanation.py`: AST-based rule explanation and optional LLM-assisted
  refactoring metadata.
- `runner.py`: shared execution helper for running RACE-Sched on one JMS/GEN-Bench
  JSONL instance and writing metrics.
- `runner_jms.py`: command-line wrapper around `runner.solve_jms_instance`.
- `runner_utils.py`: small CLI/config helper utilities.
- `stats_utils.py`: numeric summary helpers used in agent statistics and prompt
  payloads.

## Generated Rule Execution

Generated code is compiled by `compile_optimized_priority`. The execution
environment intentionally exposes only a small set of safe Python builtins and
the `math` module. File system, network, process, randomness, and import-heavy
modules are blocked.

Generated rules are expected to be imperfect. Runtime errors inside generated
priority functions are counted, logged, and eventually disable that rule so the
main scheduler can fall back to a safe action path.

## Evaluation

Each accepted candidate must pass paired sandbox evaluation against the current
baseline rule. The evaluator:

1. Acquires a pool of deterministic evaluation instances.
2. Runs the baseline and candidate on matching episodes.
3. Computes relative makespan improvement, effect size, and an approximate
   t-statistic.
4. Accepts only candidates that satisfy the configured improvement,
   effect-size, and significance thresholds.
5. Rejects early after the minimum number of episodes if the candidate is not
   improving.

Accepted rules are scored with a small complexity penalty before selection.

## Outputs

Each run writes:

- `metrics.json`: aggregate metrics, agent stats, policy stats, and Gantt data.
- `gantt.json`: extracted Gantt data for quick inspection.
- `llmcoder_trajectory.jsonl`: force-sync and worker events useful for debugging
  candidate generation and selection.
