"""Tests for reproducible synthetic data and JSONL contracts."""

import pytest

from llmops.config import Settings
from llmops.data.dataset import (
    SupportExample,
    generate_configured_datasets,
    generate_dataset,
    read_jsonl,
    split_dataset,
    write_jsonl,
)


def test_generation_is_deterministic_for_seed_and_count() -> None:
    assert generate_dataset(sample_count=25, seed=7) == generate_dataset(sample_count=25, seed=7)


def test_generation_covers_topics_and_expected_keywords() -> None:
    examples = generate_dataset(sample_count=25, seed=1)

    assert {example.topic for example in examples} == {
        "account_access",
        "sync_status",
        "file_sharing",
        "storage",
        "billing",
    }
    for example in examples:
        response = example.response.casefold()
        assert all(keyword.casefold() in response for keyword in example.keywords)


def test_split_is_deterministic_disjoint_and_complete() -> None:
    examples = generate_dataset(sample_count=30, seed=10)
    train, validation = split_dataset(examples, validation_fraction=0.2, seed=99)
    repeated_train, repeated_validation = split_dataset(examples, validation_fraction=0.2, seed=99)

    assert train == repeated_train
    assert validation == repeated_validation
    assert {row.id for row in train}.isdisjoint({row.id for row in validation})
    assert {row.id for row in train} | {row.id for row in validation} == {
        row.id for row in examples
    }


def test_split_rejects_duplicate_identifiers() -> None:
    duplicate = SupportExample(
        id="duplicate",
        topic="test",
        instruction="Help",
        response="Here is help",
        keywords=("help",),
    )

    with pytest.raises(ValueError, match="IDs must be unique"):
        split_dataset([duplicate, duplicate])


def test_jsonl_round_trip(tmp_path) -> None:
    examples = generate_dataset(sample_count=5, seed=2)
    output_path = write_jsonl(examples, tmp_path / "nested" / "dataset.jsonl")

    assert read_jsonl(output_path) == examples


def test_configured_pipeline_writes_train_and_validation_files(tmp_path) -> None:
    config = Settings(
        data_dir=tmp_path,
        sample_count=10,
        seed=3,
        validation_fraction=0.2,
    )

    train_path, validation_path = generate_configured_datasets(config)
    train = read_jsonl(train_path)
    validation = read_jsonl(validation_path)

    assert len(train) == 8
    assert len(validation) == 2
    assert {row.id for row in train}.isdisjoint({row.id for row in validation})


def test_jsonl_reports_invalid_row_and_line(tmp_path) -> None:
    input_path = tmp_path / "invalid.jsonl"
    input_path.write_text('{"id": ""}\n', encoding="utf-8")

    with pytest.raises(ValueError, match=r"invalid\.jsonl:1"):
        read_jsonl(input_path)


def test_generation_requires_positive_sample_count() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        generate_dataset(sample_count=0)


def test_split_requires_two_examples() -> None:
    with pytest.raises(ValueError, match="At least two examples"):
        split_dataset(generate_dataset(sample_count=1))
