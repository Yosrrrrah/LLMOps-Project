"""Versioned system prompt discovery and chat-message construction."""

import re
from pathlib import Path

from llmops.config import settings

_VERSION_PATTERN = re.compile(r"v[0-9]+")


class PromptVersionNotFoundError(ValueError):
    """Raised when a requested prompt version is not available."""


def discover_prompt_versions(prompts_dir: str | Path | None = None) -> tuple[str, ...]:
    """Return available prompt versions in numeric order."""
    directory = Path(prompts_dir) if prompts_dir is not None else settings.prompts_dir
    versions = [
        path.stem
        for path in directory.glob("v*.txt")
        if _VERSION_PATTERN.fullmatch(path.stem) and path.is_file()
    ]
    return tuple(sorted(versions, key=lambda version: int(version[1:])))


def load_prompt(version: str | None = None, prompts_dir: str | Path | None = None) -> str:
    """Load a versioned system prompt or raise a clear error for unknown versions."""
    selected_version = version or settings.default_prompt_version
    directory = Path(prompts_dir) if prompts_dir is not None else settings.prompts_dir
    if not _VERSION_PATTERN.fullmatch(selected_version):
        raise PromptVersionNotFoundError(f"Invalid prompt version: {selected_version!r}")

    prompt_path = directory / f"{selected_version}.txt"
    if not prompt_path.is_file():
        available = ", ".join(discover_prompt_versions(directory)) or "none"
        raise PromptVersionNotFoundError(
            f"Prompt version {selected_version!r} was not found in {directory}. "
            f"Available versions: {available}"
        )

    prompt = prompt_path.read_text(encoding="utf-8").strip()
    if not prompt:
        raise ValueError(f"Prompt file is empty: {prompt_path}")
    return prompt


def build_chat_messages(
    instruction: str,
    version: str | None = None,
    prompts_dir: str | Path | None = None,
) -> list[dict[str, str]]:
    """Combine the selected system prompt and a user instruction."""
    if not instruction.strip():
        raise ValueError("instruction must not be empty")
    return [
        {"role": "system", "content": load_prompt(version, prompts_dir)},
        {"role": "user", "content": instruction.strip()},
    ]
