"""Typed application configuration loaded from YAML and environment variables."""

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "config.yaml"


def resolve_project_path(path: str | Path, project_root: str | Path = PROJECT_ROOT) -> Path:
    """Resolve a configured path against the project root unless it is absolute."""
    candidate = Path(path).expanduser()
    if candidate.is_absolute():
        return candidate
    return Path(project_root).resolve() / candidate


def _read_config(path: Path) -> dict[str, object]:
    try:
        with path.open(encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)
    except OSError as exc:
        raise OSError(f"Unable to read configuration file: {path}") from exc
    if config is None:
        return {}
    if not isinstance(config, dict):
        raise ValueError(f"Configuration file must contain a YAML mapping: {path}")
    return config


def _section(config: dict[str, object], name: str) -> dict[str, object]:
    value = config.get(name, {})
    if not isinstance(value, dict):
        raise ValueError(f"Configuration section '{name}' must be a mapping")
    return value


def _integer(value: object, key: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{key} must be an integer")
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{key} must be an integer") from exc


def _float(value: object, key: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{key} must be a number")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{key} must be a number") from exc


def _environment_value(environ: Mapping[str, str], key: str, configured_value: object) -> object:
    return environ.get(key, configured_value)


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str = "LLMOps"
    environment: str = "local"
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "INFO"
    data_dir: Path = PROJECT_ROOT / "data"
    sample_count: int = 100
    seed: int = 42
    validation_fraction: float = 0.2
    prompts_dir: Path = PROJECT_ROOT / "prompts"
    default_prompt_version: str = "v1"

    @classmethod
    def from_environment(
        cls,
        config_path: str | Path | None = None,
        environ: Mapping[str, str] | None = None,
    ) -> "Settings":
        environment = os.environ if environ is None else environ
        selected_config = config_path or environment.get("LLMOPS_CONFIG")
        resolved_config = (
            resolve_project_path(selected_config)
            if selected_config is not None
            else DEFAULT_CONFIG_PATH
        )
        config = _read_config(resolved_config)
        app = _section(config, "app")
        data = _section(config, "data")
        prompts = _section(config, "prompts")
        defaults = cls()

        app_name = str(
            _environment_value(environment, "LLMOPS_APP_NAME", app.get("name", defaults.app_name))
        )
        app_environment = str(
            _environment_value(
                environment, "LLMOPS_ENVIRONMENT", app.get("environment", defaults.environment)
            )
        )
        host = str(_environment_value(environment, "LLMOPS_HOST", app.get("host", defaults.host)))
        port = _integer(
            _environment_value(environment, "LLMOPS_PORT", app.get("port", defaults.port)),
            "LLMOPS_PORT",
        )
        log_level = str(
            _environment_value(
                environment, "LLMOPS_LOG_LEVEL", app.get("log_level", defaults.log_level)
            )
        ).upper()
        data_dir = resolve_project_path(
            str(_environment_value(environment, "LLMOPS_DATA_DIR", data.get("output_dir", "data")))
        )
        sample_count = _integer(
            _environment_value(environment, "LLMOPS_SAMPLE_COUNT", data.get("sample_count", 100)),
            "LLMOPS_SAMPLE_COUNT",
        )
        seed = _integer(
            _environment_value(environment, "LLMOPS_SEED", data.get("seed", 42)),
            "LLMOPS_SEED",
        )
        validation_fraction = _float(
            _environment_value(
                environment,
                "LLMOPS_VALIDATION_FRACTION",
                data.get("validation_fraction", 0.2),
            ),
            "LLMOPS_VALIDATION_FRACTION",
        )
        prompts_dir = resolve_project_path(
            str(
                _environment_value(
                    environment, "LLMOPS_PROMPTS_DIR", prompts.get("directory", "prompts")
                )
            )
        )
        default_prompt_version = str(
            _environment_value(
                environment,
                "LLMOPS_DEFAULT_PROMPT_VERSION",
                prompts.get("default_version", "v1"),
            )
        )

        if not 1 <= port <= 65535:
            raise ValueError("LLMOPS_PORT must be between 1 and 65535")
        if sample_count < 2:
            raise ValueError("LLMOPS_SAMPLE_COUNT must be at least 2")
        if not 0.0 < validation_fraction < 1.0:
            raise ValueError("LLMOPS_VALIDATION_FRACTION must be between 0 and 1")
        if log_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError("LLMOPS_LOG_LEVEL must be a standard logging level")

        return cls(
            app_name=app_name,
            environment=app_environment,
            host=host,
            port=port,
            log_level=log_level,
            data_dir=data_dir,
            sample_count=sample_count,
            seed=seed,
            validation_fraction=validation_fraction,
            prompts_dir=prompts_dir,
            default_prompt_version=default_prompt_version,
        )


settings = Settings.from_environment()
