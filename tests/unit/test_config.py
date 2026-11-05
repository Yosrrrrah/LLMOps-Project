"""Unit tests for environment configuration."""

import pytest

from llmops.config import Settings


def test_invalid_port(monkeypatch) -> None:
    monkeypatch.setenv("LLMOPS_PORT", "not-a-number")
    with pytest.raises(ValueError, match="LLMOPS_PORT must be an integer"):
        Settings.from_environment()


def test_valid_environment(monkeypatch) -> None:
    monkeypatch.setenv("LLMOPS_APP_NAME", "TestLLMOps")
    monkeypatch.setenv("LLMOPS_PORT", "9000")
    settings = Settings.from_environment()
    assert settings.app_name == "TestLLMOps"
    assert settings.port == 9000


def test_yaml_values_are_loaded_and_environment_overrides_them(tmp_path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "app:\n  name: FromYaml\n  port: 8100\n"
        "data:\n  output_dir: generated\n  seed: 11\n"
        "prompts:\n  directory: prompt-files\n  default_version: v2\n",
        encoding="utf-8",
    )

    settings = Settings.from_environment(
        config_path=config_path,
        environ={"LLMOPS_APP_NAME": "FromEnvironment"},
    )

    assert settings.app_name == "FromEnvironment"
    assert settings.port == 8100
    assert settings.seed == 11
    assert settings.data_dir.name == "generated"
    assert settings.prompts_dir.name == "prompt-files"
    assert settings.default_prompt_version == "v2"


def test_relative_paths_resolve_from_project_root() -> None:
    settings = Settings.from_environment(environ={})

    assert settings.data_dir.is_absolute()
    assert settings.prompts_dir.is_absolute()
    assert settings.data_dir.name == "data"
    assert settings.prompts_dir.name == "prompts"


def test_invalid_validation_fraction_is_rejected(monkeypatch) -> None:
    monkeypatch.setenv("LLMOPS_VALIDATION_FRACTION", "1")

    with pytest.raises(ValueError, match="between 0 and 1"):
        Settings.from_environment()
