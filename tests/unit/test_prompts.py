"""Tests for versioned prompt discovery and chat message assembly."""

import pytest

from llmops.utils.prompts import (
    PromptVersionNotFoundError,
    build_chat_messages,
    discover_prompt_versions,
    load_prompt,
)


def test_discovery_orders_versions_numerically(tmp_path) -> None:
    (tmp_path / "v10.txt").write_text("Prompt ten", encoding="utf-8")
    (tmp_path / "v2.txt").write_text("Prompt two", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("Not a prompt version", encoding="utf-8")

    assert discover_prompt_versions(tmp_path) == ("v2", "v10")


def test_load_prompt_reads_requested_version(tmp_path) -> None:
    (tmp_path / "v1.txt").write_text("  Be helpful.  \n", encoding="utf-8")

    assert load_prompt("v1", tmp_path) == "Be helpful."


def test_unknown_prompt_version_has_clear_error(tmp_path) -> None:
    (tmp_path / "v1.txt").write_text("Available", encoding="utf-8")

    with pytest.raises(PromptVersionNotFoundError, match="Available versions: v1"):
        load_prompt("v2", tmp_path)


def test_prompt_version_rejects_path_traversal(tmp_path) -> None:
    with pytest.raises(PromptVersionNotFoundError, match="Invalid prompt version"):
        load_prompt("../secret", tmp_path)


def test_build_chat_messages_uses_system_prompt_and_instruction(tmp_path) -> None:
    (tmp_path / "v1.txt").write_text("System rules", encoding="utf-8")

    assert build_chat_messages("  I need help.  ", "v1", tmp_path) == [
        {"role": "system", "content": "System rules"},
        {"role": "user", "content": "I need help."},
    ]


def test_build_chat_messages_rejects_blank_instruction(tmp_path) -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        build_chat_messages("  ", "v1", tmp_path)
