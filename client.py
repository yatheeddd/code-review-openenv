"""
WebSocket HTTP client for a deployed CodeReviewEnv server.

Do not import ``server`` modules from training code; keep client transport
separate from grading logic per OpenEnv invariants.
"""

from __future__ import annotations

from typing import Any, Dict

from openenv.core.client_types import StepResult
from openenv.core.env_client import EnvClient

from env.models import CodeReviewAction, CodeReviewObservation, CodeReviewState


class CodeReviewEnvClient(
    EnvClient[CodeReviewAction, CodeReviewObservation, CodeReviewState]
):
    """
    Thin :class:`EnvClient` with Pydantic (de)serialization for CodeReviewEnv.
    """

    def _step_payload(self, action: CodeReviewAction) -> dict:
        return action.model_dump()

    def _parse_result(self, data: Dict[str, Any]) -> StepResult[CodeReviewObservation]:
        return StepResult(
            observation=CodeReviewObservation(**data["observation"]),
            reward=data.get("reward"),
            done=data.get("done", False),
            info=data.get("info", {}),
        )

    def _parse_state(self, data: Dict[str, Any]) -> CodeReviewState:
        return CodeReviewState(**data)
