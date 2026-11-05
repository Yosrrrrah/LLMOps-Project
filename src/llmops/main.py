"""Application entry point."""

import uvicorn

from llmops.config import settings


def main() -> None:
    uvicorn.run(
        "llmops.api.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "local",
    )


if __name__ == "__main__":
    main()
