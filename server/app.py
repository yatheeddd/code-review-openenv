"""
FastAPI entrypoint for OpenEnv ``CodeReviewEnv``.

Run locally:

    uvicorn server.app:app --host 0.0.0.0 --port 8000

Or via Docker / Hugging Face Spaces (set ``PORT`` if the platform injects it).
"""

from __future__ import annotations

import os

from fastapi.responses import RedirectResponse

from openenv.core.env_server import create_app

from env.environment import CodeReviewEnvironment
from env.models import CodeReviewAction, CodeReviewObservation

app = create_app(
    CodeReviewEnvironment,
    CodeReviewAction,
    CodeReviewObservation,
    env_name="CodeReviewEnv",
)


@app.get("/", include_in_schema=False)
async def _root() -> RedirectResponse:
    """OpenEnv does not register ``GET /``; send humans to Swagger UI."""
    return RedirectResponse(url="/docs")


def main() -> None:
    import uvicorn

    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
