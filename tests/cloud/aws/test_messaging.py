"""Tests for AWS messaging types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.aws.messaging import SqsQueueUrl


class SqsModel(BaseModel):
    url: SqsQueueUrl


@pytest.mark.parametrize(
    ("value", "region", "account_id", "queue_name"),
    [
        (
            "https://sqs.us-east-1.amazonaws.com/123456789012/my-queue",
            "us-east-1",
            "123456789012",
            "my-queue",
        ),
        (
            "https://sqs.eu-west-1.amazonaws.com/123456789012/my-queue.fifo",
            "eu-west-1",
            "123456789012",
            "my-queue.fifo",
        ),
    ],
)
def test_valid_sqs_queue_url(value: str, region: str, account_id: str, queue_name: str) -> None:
    model = SqsModel(url=value)
    assert str(model.url) == value
    assert model.url.region == region
    assert model.url.account_id == account_id
    assert model.url.queue_name == queue_name


@pytest.mark.parametrize(
    "value",
    [
        "http://sqs.us-east-1.amazonaws.com/123456789012/my-queue",
        "https://sqs.us-east-1.amazonaws.com/12345/my-queue",
        "https://wrong.domain.com/123456789012/my-queue",
        "",
    ],
)
def test_invalid_sqs_queue_url(value: str) -> None:
    with pytest.raises(ValidationError):
        SqsModel(url=value)


def test_sqs_queue_url_serialization() -> None:
    model = SqsModel(url="https://sqs.us-east-1.amazonaws.com/123456789012/my-queue")
    dumped = model.model_dump()
    assert dumped == {"url": "https://sqs.us-east-1.amazonaws.com/123456789012/my-queue"}
    json_str = model.model_dump_json()
    restored = SqsModel.model_validate_json(json_str)
    assert restored.url == model.url


def test_sqs_queue_url_existing_instance() -> None:
    url = SqsQueueUrl("https://sqs.us-east-1.amazonaws.com/123456789012/my-queue")
    model = SqsModel(url=url)
    assert model.url is url


def test_sqs_queue_url_json_schema() -> None:
    schema = SqsModel.model_json_schema()
    field_schema = schema["properties"]["url"]
    assert field_schema["type"] == "string"
    assert field_schema["format"] == "aws-sqs-queue-url"
