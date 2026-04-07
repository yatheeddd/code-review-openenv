"""
CodeReviewEnv — OpenEnv ``Environment`` implementation wired to ``/reset`` and ``/step``.

Episode flow:
    1. ``reset`` picks one buggy snippet (random but seeded for reproducibility)
       unless ``task_id`` pins a row for tests.
    2. The agent posts a ``CodeReviewAction`` to ``step``.
    3. The grader compares the action to the stored ``issue`` label and sets
       ``reward`` in ``{1.0, 0.5, 0.0}``, ``done=True``, and metadata with
       ``expected_issue``.
"""

from __future__ import annotations

import random
import uuid
from copy import deepcopy
from threading import Lock
from typing import Any, Optional

from openenv.core.env_server import Environment
from openenv.core.env_server.types import EnvironmentMetadata

from env.models import (
    CodeReviewAction,
    CodeReviewObservation,
    CodeReviewState,
)

from graders.grader import grade
from tasks import ALL_TASKS, TASK_BY_ID


class CodeReviewEnvironment(
    Environment[CodeReviewAction, CodeReviewObservation, CodeReviewState]
):
    """
    Code Review Environment for OpenEnv.

    Simulates a real-world code review task where an AI agent must identify
    issues in a code snippet and submit a review.
    """

    SUPPORTS_CONCURRENT_SESSIONS = True
    _shared_lock = Lock()
    _shared_current: Optional[dict[str, Any]] = None
    _shared_state: Optional[CodeReviewState] = None

    def __init__(self) -> None:
        super().__init__()

        self._rng = random.Random()

        self._state = CodeReviewState(
            episode_id=str(uuid.uuid4()),
            step_count=0,
        )

        self._current: Optional[dict[str, Any]] = None
        # HTTP mode may create a fresh env per request; recover last episode snapshot.
        with self._shared_lock:
            if self._shared_current is not None:
                self._current = deepcopy(self._shared_current)
            if self._shared_state is not None:
                self._state = self._shared_state.model_copy(deep=True)

    def _persist_shared(self) -> None:
        """Persist current task/state across short-lived HTTP env instances."""
        with self._shared_lock:
            self.__class__._shared_current = (
                deepcopy(self._current) if self._current is not None else None
            )
            self.__class__._shared_state = self._state.model_copy(deep=True)

    def _fallback_task(self) -> dict[str, Any]:
        """
        Return a deterministic fallback task if no task is loaded.
        This prevents /step from crashing when called before /reset.
        """
        if not ALL_TASKS:
            return {
                "id": "fallback-empty",
                "code": "# No tasks configured.",
                "issue": "unknown_issue",
                "difficulty": "unknown",
            }
        return dict(ALL_TASKS[0])

    # -------------------------------------------------
    # RESET
    # -------------------------------------------------

    def reset(
        self,
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
        **kwargs: Any,
    ) -> CodeReviewObservation:

        """
        Starts a new episode and returns a code snippet to review.
        """

        self._reset_rubric()

        task_id: Optional[str] = kwargs.get("task_id")

        if seed is not None:
            self._rng.seed(seed)

        # Load specific task if provided
        if task_id is not None:
            if task_id not in TASK_BY_ID:
                raise ValueError(f"Unknown task_id: {task_id}")

            self._current = dict(TASK_BY_ID[task_id])

        else:
            # randomly select task
            self._current = dict(self._rng.choice(ALL_TASKS))

        # update state
        self._state.episode_id = episode_id or str(uuid.uuid4())
        self._state.step_count = 0
        self._state.current_code = self._current["code"]
        self._state.expected_issue = self._current["issue"]
        self._persist_shared()

        return CodeReviewObservation(
            code_snippet=self._current["code"],
            language="python",
            reward=0.0,
            done=False,
            metadata={
                "task_id": self._current["id"],
                "difficulty": self._current.get("difficulty", "unknown"),
                "language": "python",
            },
        )

    # -------------------------------------------------
    # STEP
    # -------------------------------------------------

    def step(
        self,
        action: CodeReviewAction,
        timeout_s: Optional[float] = None,
        **kwargs: Any,
    ) -> CodeReviewObservation:

        """
        Receives the agent's review and grades it.
        """

        if self._current is None:
            # Avoid 500s in Swagger/HTTP when session state is not preserved.
            with self._shared_lock:
                if self._shared_current is not None:
                    self._current = deepcopy(self._shared_current)
            if self._current is None:
                self._current = self._fallback_task()
            self._state.current_code = str(self._current.get("code", ""))
            self._state.expected_issue = str(self._current.get("issue", ""))

        self._state.step_count += 1

        expected_issue = str(self._current.get("issue", ""))

        # Safe grading
        try:
            reward = float(grade(action, expected_issue))
        except Exception:
            reward = 0.0

        # ensure reward is always finite and in [0, 1]
        if reward != reward or reward in (float("inf"), float("-inf")):
            reward = 0.0
        reward = max(0.0, min(1.0, reward))

        info = {
            "expected_issue": expected_issue,
            "task_id": str(self._current.get("id", "unknown")),
            "difficulty": self._current.get("difficulty", "unknown"),
        }
        self._persist_shared()

        return CodeReviewObservation(
            code_snippet=str(self._current.get("code", "")),
            language="python",
            reward=reward,
            done=True,
            metadata=info,
        )

    # -------------------------------------------------
    # STATE
    # -------------------------------------------------

    @property
    def state(self) -> CodeReviewState:
        return self._state

    # -------------------------------------------------
    # METADATA
    # -------------------------------------------------

    def get_metadata(self) -> EnvironmentMetadata:  # type: ignore[override]
        return EnvironmentMetadata(
            name="CodeReviewEnv",
            description="OpenEnv environment for evaluating AI code review agents",
            version="1.0",
            author="Meta OpenEnv Challenge",
        )