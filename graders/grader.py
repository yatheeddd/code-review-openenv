"""
Deterministic grading for CodeReviewEnv.

Scores:
    1.0 — issue clearly identified (expected label match or strong keyword hit).
    0.5 — partially correct (related keywords in the review text).
    0.0 — incorrect / unrelated.
"""
from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from env.models import CodeReviewAction


def _normalize_label(label: str | None) -> str:
    if not label:
        return ""
    s = label.strip().lower()
    s = re.sub(r"[\s\-]+", "_", s)
    return s


def _issue_tokens(issue: str) -> list[str]:
    """Substrings that should appear in a good review for this issue label."""
    norm = _normalize_label(issue)
    base = [t for t in norm.split("_") if len(t) > 1]

    aliases = {
        "sql": ["sql", "injection", "query", "concat"],
        "injection": ["injection", "inject", "sanitize", "parameterize", "bind"],
        "command": ["command", "shell", "os.system", "subprocess"],
        "unsafe": ["unsafe", "path", "traversal", "sanitize", "user_path"],
        "broken": ["auth", "token", "hardcoded", "credential", "verify"],
        "authentication": ["auth", "token", "verify", "credential"],
        "indentation": ["indent", "syntax"],
        "missing": ["colon", "def", "syntax"],
        "syntax": ["syntax", "assign", "==", "invalid"],
        "logic": ["logic", "condition", "return", "wrong", "incorrect", "loop"],
    }

    tokens: set[str] = set(base)

    for part in base:
        for a in aliases.get(part, []):
            tokens.add(a)

    return sorted(tokens, key=len, reverse=True)


def grade(action: "CodeReviewAction", expected_issue: str) -> float:
    """
    Compare the agent action to the ground-truth expected_issue.
    """

    try:
        expected = _normalize_label(expected_issue)
        declared = _normalize_label(str(getattr(action, "issue_type", "")))
        review_text = str(getattr(action, "review_comment", ""))
        text = review_text.lower()

        if not expected:
            return 0.0

        # perfect match
        if declared == expected or declared in expected or expected in declared:
            return 1.0

        tokens = _issue_tokens(expected_issue)

        hits = sum(1 for tok in tokens if tok in text)

        strong = {"sql_injection", "command_injection", "unsafe_file_access"}

        if expected in strong and hits >= 2:
            return 1.0

        if expected in strong and hits == 1 and len(tokens) <= 6:
            return 0.5

        if hits >= 2:
            return 1.0

        if hits == 1:
            return 0.5

        return 0.0

    except Exception:
        return 0.0
