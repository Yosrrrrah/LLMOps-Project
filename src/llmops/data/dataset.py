"""Deterministic synthetic support data generation and JSONL utilities."""

import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict

from llmops.config import Settings, settings


class DatasetRow(TypedDict):
    id: str
    topic: str
    instruction: str
    response: str
    keywords: list[str]


@dataclass(frozen=True, slots=True)
class SupportExample:
    id: str
    topic: str
    instruction: str
    response: str
    keywords: tuple[str, ...]

    def to_dict(self) -> DatasetRow:
        return {
            "id": self.id,
            "topic": self.topic,
            "instruction": self.instruction,
            "response": self.response,
            "keywords": list(self.keywords),
        }


_TOPICS: tuple[tuple[str, tuple[str, ...], tuple[str, ...], str, tuple[str, ...]], ...] = (
    (
        "account_access",
        (
            "I cannot sign in to my AuroraSync account.",
            "I need help resetting access to my account.",
            "My password is not working when I log in.",
        ),
        ("password", "reset", "account"),
        "To reset your password, open Account Settings and select Password Reset. "
        "Confirm your account email before saving the new password.",
        ("account", "password"),
    ),
    (
        "sync_status",
        (
            "My files are not syncing across my devices.",
            "The sync status has been paused for a long time.",
            "Recent changes are missing from my other device.",
        ),
        ("sync", "connection", "restart"),
        "Check your internet connection, then restart AuroraSync. The sync status "
        "should update when the connection is restored.",
        ("sync", "connection"),
    ),
    (
        "file_sharing",
        (
            "How can I share a file with a teammate?",
            "A shared link is not opening for my colleague.",
            "I want to change who can access a shared file.",
        ),
        ("share", "link", "permissions"),
        "To share a file, create a sharing link and review the link permissions "
        "before sending it to your teammate.",
        ("share", "link"),
    ),
    (
        "storage",
        (
            "I am running out of cloud storage.",
            "Where can I see how much storage I have used?",
            "How do I free space in my AuroraSync account?",
        ),
        ("storage", "files", "delete"),
        "Review storage usage in Account Settings, then delete files you no longer "
        "need or move them to another storage location.",
        ("storage", "files"),
    ),
    (
        "billing",
        (
            "Where can I find my latest invoice?",
            "I need help understanding my subscription charge.",
            "How do I review or change my AuroraSync plan?",
        ),
        ("billing", "plan", "invoice"),
        "Open Billing in Account Settings to review your plan and download the "
        "latest invoice. Contact support if a charge still looks incorrect.",
        ("billing", "invoice"),
    ),
)


def generate_dataset(sample_count: int = 100, seed: int = 42) -> list[SupportExample]:
    """Generate reproducible support examples covering each configured topic."""
    if sample_count < 1:
        raise ValueError("sample_count must be at least 1")

    rows: list[SupportExample] = []
    for index in range(sample_count):
        topic, instructions, keywords, response, _ = _TOPICS[index % len(_TOPICS)]
        instruction = instructions[(index // len(_TOPICS)) % len(instructions)]
        cycle = index // (len(_TOPICS) * len(instructions))
        if cycle:
            instruction = f"{instruction} (support case {cycle + 1})"
        rows.append(
            SupportExample(
                id=f"aurora-{index + 1:05d}",
                topic=topic,
                instruction=instruction,
                response=response,
                keywords=keywords,
            )
        )

    random.Random(seed).shuffle(rows)
    return rows


def split_dataset(
    examples: list[SupportExample],
    validation_fraction: float = 0.2,
    seed: int = 42,
) -> tuple[list[SupportExample], list[SupportExample]]:
    """Split unique examples reproducibly while retaining their input order."""
    if len(examples) < 2:
        raise ValueError("At least two examples are required to create a split")
    if not 0.0 < validation_fraction < 1.0:
        raise ValueError("validation_fraction must be between 0 and 1")

    identifiers = [example.id for example in examples]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("Dataset example IDs must be unique before splitting")

    validation_count = min(
        len(examples) - 1,
        max(1, round(len(examples) * validation_fraction)),
    )
    shuffled_indices = list(range(len(examples)))
    random.Random(seed).shuffle(shuffled_indices)
    validation_indices = set(shuffled_indices[:validation_count])

    train = [example for index, example in enumerate(examples) if index not in validation_indices]
    validation = [example for index, example in enumerate(examples) if index in validation_indices]
    return train, validation


def write_jsonl(examples: list[SupportExample], path: str | Path) -> Path:
    """Write examples as one compact JSON object per line."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as output_file:
        for example in examples:
            output_file.write(
                json.dumps(example.to_dict(), ensure_ascii=False, sort_keys=True) + "\n"
            )
    return output_path


def generate_configured_datasets(
    config: Settings | None = None,
) -> tuple[Path, Path]:
    """Generate and write configured train and validation JSONL files."""
    active_config = config or settings
    examples = generate_dataset(active_config.sample_count, active_config.seed)
    train, validation = split_dataset(
        examples,
        validation_fraction=active_config.validation_fraction,
        seed=active_config.seed,
    )
    train_path = write_jsonl(train, active_config.data_dir / "train.jsonl")
    validation_path = write_jsonl(validation, active_config.data_dir / "validation.jsonl")
    return train_path, validation_path


def main() -> None:
    """Generate configured train and validation files from the command line."""
    train_path, validation_path = generate_configured_datasets()
    print(f"Generated training data: {train_path}")
    print(f"Generated validation data: {validation_path}")


def read_jsonl(path: str | Path) -> list[SupportExample]:
    """Read JSONL rows and report malformed content with file and line context."""
    input_path = Path(path)
    examples: list[SupportExample] = []
    with input_path.open(encoding="utf-8") as input_file:
        for line_number, line in enumerate(input_file, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                examples.append(_example_from_row(row))
            except (json.JSONDecodeError, TypeError, ValueError) as exc:
                raise ValueError(
                    f"Invalid dataset row at {input_path}:{line_number}: {exc}"
                ) from exc
    return examples


def _example_from_row(row: object) -> SupportExample:
    if not isinstance(row, dict):
        raise ValueError("row must be a JSON object")

    required_strings = ("id", "topic", "instruction", "response")
    for key in required_strings:
        if not isinstance(row.get(key), str) or not row[key].strip():
            raise ValueError(f"'{key}' must be a non-empty string")

    keywords = row.get("keywords")
    if not isinstance(keywords, list) or not all(
        isinstance(keyword, str) and keyword.strip() for keyword in keywords
    ):
        raise ValueError("'keywords' must be a list of non-empty strings")

    return SupportExample(
        id=row["id"],
        topic=row["topic"],
        instruction=row["instruction"],
        response=row["response"],
        keywords=tuple(keywords),
    )
