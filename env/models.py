"""
Pydantic wire types for CodeReviewEnv (OpenEnv HTTP / WebSocket API).

Observation emphasizes ``code_snippet`` and ``language`` as in the challenge spec;
``reward`` / ``done`` follow the base OpenEnv observation contract.
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field

from openenv.core.env_server.types import Action, Observation, State


class CodeReviewAction(Action):
    """Structured review produced by the agent for ``POST /step``."""

    review_comment: str = Field(
        ...,
        min_length=1,
        description="Natural-language review; keywords here drive partial credit.",
    )
    issue_type: str = Field(
        ...,
        description="Snake_case label for the primary defect (e.g. sql_injection).",
    )
    severity: Literal["low", "medium", "high"] = Field(
        ...,
        description="Perceived severity of the issue.",
    )


class CodeReviewObservation(Observation):
    """
    What the agent sees after ``/reset`` (and again after ``/step`` for continuity).

    Challenge-facing payload centers on ``code_snippet`` and ``language``.
    """

    code_snippet: str = Field(..., description="Buggy code to review.")
    language: str = Field(default="python", description="Source language tag.")
    reward: float = Field(
        default=0.0,
        description="Grader output from last step; 0 immediately after reset.",
    )
    done: bool = Field(
        default=False,
        description="True once a review has been graded for this episode.",
    )


class CodeReviewState(State):
    """Exposed via ``GET /state`` — current episode snippet and secret label."""

    current_code: str = Field(
        default="",
        description="The active buggy snippet (same text as observation code).",
    )
    expected_issue: str = Field(
        default="",
        description="Ground-truth issue key used by the grader (teachers / evaluators).",
    )
