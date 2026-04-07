"""
Easy tasks: syntax, indentation, and other obvious static mistakes.
Each row: ``code`` (buggy snippet), ``issue`` (expected label for grading).
"""

from __future__ import annotations

from typing import Any, Dict, List

EASY_TASKS: List[Dict[str, Any]] = [
    {
        "id": "easy-missing-colon",
        "code": "def add(a, b)\n    return a + b\n",
        "issue": "missing_colon",
    },
    {
        "id": "easy-indentation",
        "code": "def total(items):\n    s = 0\n     for x in items:\n        s += x\n    return s\n",
        "issue": "indentation_error",
    },
    {
        "id": "easy-syntax-assign",
        "code": "if x = 5:\n    print(x)\n",
        "issue": "syntax_error",
    },
    {
        "id": "easy-bare-return",
        "code": "def f():\nreturn 1\n",
        "issue": "indentation_error",
    },
]
