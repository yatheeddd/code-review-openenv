"""
Medium tasks: logical errors — wrong conditions, returns, and control flow.
"""

from __future__ import annotations

from typing import Any, Dict, List

MEDIUM_TASKS: List[Dict[str, Any]] = [
    {
        "id": "medium-is-even",
        "code": "def is_even(n):\n    if n % 2 == 1:\n        return True\n    return False\n",
        "issue": "logic_error",
    },
    {
        "id": "medium-adult-check",
        "code": "def is_adult(age):\n    return age > 18\n",
        "issue": "logic_error",
    },
    {
        "id": "medium-loop-index",
        "code": (
            "def first_positive(nums):\n"
            "    for i in range(len(nums) + 1):\n"
            "        if nums[i] > 0:\n"
            "            return nums[i]\n"
            "    return None\n"
        ),
        "issue": "logic_error",
    },
    {
        "id": "medium-countdown",
        "code": (
            "def countdown(n):\n"
            "    while n > 0:\n"
            "        print(n)\n"
            "    print('done')\n"
        ),
        "issue": "logic_error",
    },
]
