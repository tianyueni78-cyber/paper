from __future__ import annotations

from typing import Any, Callable, Mapping, Tuple


ConfigOverride = Tuple[Any, Callable[[Any], Any]]


def apply_config_overrides(cfg: Any, overrides: Mapping[str, ConfigOverride]) -> None:
    """Apply optional typed overrides to a config object in place.

    `None` means "leave the existing value unchanged". Invalid values should
    fail at the caller boundary instead of silently changing experiment setup.
    """

    for field_name, (raw_value, converter) in overrides.items():
        if raw_value is None:
            continue
        setattr(cfg, field_name, converter(raw_value))
