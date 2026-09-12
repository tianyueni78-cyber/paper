from __future__ import annotations

import math
from typing import Any, Dict, List, Sequence, TypeVar


T = TypeVar("T")


def even_sample(values: Sequence[T], max_n: int) -> List[T]:
    """Return up to `max_n` values while preserving the original order."""

    if max_n <= 0:
        return []
    if len(values) <= max_n:
        return list(values)

    step = max(1, len(values) // max_n)
    out: List[T] = []
    index = 0
    while index < len(values) and len(out) < max_n:
        out.append(values[index])
        index += step
    return out


def numeric_stats(values: Sequence[float], *, include_sample_n: bool = False) -> Dict[str, Any]:
    """Summarize numeric values with simple descriptive statistics."""

    if not values:
        return {"count": 0}

    vals = sorted(float(v) for v in values)
    mean = sum(vals) / float(len(vals))
    variance = 0.0
    if len(vals) >= 2:
        variance = sum((x - mean) ** 2 for x in vals) / float(len(vals) - 1)

    def quantile(p: float) -> float:
        index = int(round((len(vals) - 1) * p))
        index = max(0, min(index, len(vals) - 1))
        return float(vals[index])

    result: Dict[str, Any] = {
        "count": int(len(values)),
        "min": float(vals[0]),
        "max": float(vals[-1]),
        "mean": float(mean),
        "std": float(math.sqrt(max(variance, 0.0))),
        "p50": quantile(0.5),
        "p90": quantile(0.9),
        "p95": quantile(0.95),
    }
    if include_sample_n:
        result["sample_n"] = int(len(values))
    return result


def finite_float(value: Any) -> float | None:
    """Return a finite float or None when conversion is not meaningful."""

    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(out):
        return None
    return out
