"""Task pools for CodeReviewEnv (easy / medium / hard)."""

from __future__ import annotations

from typing import Any, Dict, List

from tasks.easy_task import EASY_TASKS
from tasks.hard_task import HARD_TASKS
from tasks.medium_task import MEDIUM_TASKS


def _tag(tasks: List[Dict[str, Any]], difficulty: str) -> List[Dict[str, Any]]:
    """Attach difficulty for logging; copies shallowly."""
    out: List[Dict[str, Any]] = []
    for row in tasks:
        entry = {**row, "difficulty": difficulty}
        out.append(entry)
    return out


# Flattened list used by the environment for random / seeded selection.
ALL_TASKS: List[Dict[str, Any]] = (
    _tag(EASY_TASKS, "easy") + _tag(MEDIUM_TASKS, "medium") + _tag(HARD_TASKS, "hard")
)

TASK_BY_ID: Dict[str, Dict[str, Any]] = {t["id"]: t for t in ALL_TASKS}

# Backward-compatible name for scripts that iterate by tier.
TASK_REGISTRY = {
    "easy": _tag(EASY_TASKS, "easy"),
    "medium": _tag(MEDIUM_TASKS, "medium"),
    "hard": _tag(HARD_TASKS, "hard"),
}

__all__ = [
    "ALL_TASKS",
    "TASK_BY_ID",
    "TASK_REGISTRY",
    "EASY_TASKS",
    "MEDIUM_TASKS",
    "HARD_TASKS",
]
