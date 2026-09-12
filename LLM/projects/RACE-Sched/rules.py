from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any, Dict, List, Optional, Protocol


class PriorityRule(Protocol):
    def __call__(self, obs: Dict[str, Any], action: Dict[str, Any], env: Any) -> float:  # pragma: no cover - protocol
        ...


@dataclass
class RuleWithMeta:
    rule: PriorityRule
    name: str = "rule"
    version: int = 0
    info: Dict[str, Any] = field(default_factory=dict)


class RuleManager:
    """Thread-safe manager for the currently active scheduling rule."""

    def __init__(self, fallback_rule: PriorityRule, name: str = "fallback") -> None:
        self._lock = Lock()
        self._current = RuleWithMeta(rule=fallback_rule, name=name, version=0, info={})
        self._fallback = self._current

    def reset_to_fallback(self) -> None:
        with self._lock:
            self._current = self._fallback

    def get_active_rule(self) -> RuleWithMeta:
        with self._lock:
            return self._current

    def update_rule(self, new_rule: RuleWithMeta) -> None:
        with self._lock:
            ver = self._current.version + 1
            self._current = RuleWithMeta(rule=new_rule.rule, name=new_rule.name, version=ver, info=dict(new_rule.info))


class SPTPriorityRule:
    """Priority rule corresponding to the SPT heuristic.

    Higher scores mean higher priority, so shortest processing time maps to
    `-process_time`.
    """

    def __call__(self, obs: Dict[str, Any], action: Dict[str, Any], env: Any) -> float:
        job_id = str(action.get("job_id"))
        ready_ops: List[Dict[str, Any]] = obs.get("ready_ops", []) or []
        pt = None
        for ro in ready_ops:
            if str(ro.get("job_id")) == job_id:
                try:
                    v = float(ro.get("process_time", 0.0))
                except (TypeError, ValueError):
                    v = 0.0
                pt = v if pt is None or v < pt else pt
        if pt is None:
            pt = 0.0
        return -float(pt)


def choose_action_by_rule(
    rule: PriorityRule,
    obs: Dict[str, Any],
    legal_actions: List[Dict[str, Any]],
    env: Any,
) -> Optional[Dict[str, Any]]:
    if not legal_actions:
        return None

    is_disabled = getattr(rule, "is_disabled", None)
    if callable(is_disabled) and bool(is_disabled()):
        # Disabled generated rules fall back to the simulator-provided first
        # action, preserving the original machine-selection behavior.
        return legal_actions[0]

    # Expand each legal action to job-machine candidates when explicit machine
    # choices are available, allowing generated rules to score concrete
    # machine assignments.
    expanded_pairs: List[tuple[Dict[str, Any], Dict[str, Any]]] = []
    for base in legal_actions:
        machines = list(base.get("machine_candidates") or [])
        if not machines:
            expanded_pairs.append((base, base))
            continue
        base_no_mid = dict(base)
        base_no_mid.pop("machine_id", None)
        for m_id in machines:
            a = dict(base_no_mid)
            a["machine_id"] = m_id
            # Keep the full candidate list available for generated rules.
            a["machine_candidates"] = machines
            expanded_pairs.append((a, base_no_mid))

    if len(expanded_pairs) == 1:
        return expanded_pairs[0][0]

    best_action: Optional[Dict[str, Any]] = None
    best_base_action: Optional[Dict[str, Any]] = None
    best_score = float("-inf")
    base_scores: Dict[tuple[str, str, tuple[Any, ...]], List[float]] = {}

    for a, base_action in expanded_pairs:
        job_id = str(a.get("job_id"))
        mg = str(a.get("machine_group"))
        machines_tuple = tuple(a.get("machine_candidates") or [])
        base_key = (job_id, mg, machines_tuple)
        s = float(rule(obs, a, env))

        base_scores.setdefault(base_key, []).append(float(s))

        if s > best_score:
            best_score = s
            best_action = a
            best_base_action = base_action

    if best_action is None:
        return legal_actions[0]

    job_id = str(best_action.get("job_id"))
    mg = str(best_action.get("machine_group"))
    machines_tuple = tuple(best_action.get("machine_candidates") or [])
    base_key = (job_id, mg, machines_tuple)
    scores_here = base_scores.get(base_key) or []
    if len(scores_here) >= 2:
        s_max = max(scores_here)
        s_min = min(scores_here)
        if abs(s_max - s_min) <= 1e-12 and best_base_action is not None:
            return best_base_action

    return best_action
