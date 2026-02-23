"""Tests for AWS container types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.aws.containers import EcrRepositoryUri


class EcrModel(BaseModel):
    uri: EcrRepositoryUri


@pytest.mark.parametrize(
    ("value", "account_id", "region", "repository_name"),
    [
        (
            "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-repo",
            "123456789012",
            "us-east-1",
            "my-repo",
        ),
        (
            "123456789012.dkr.ecr.eu-west-1.amazonaws.com/org/my-repo",
            "123456789012",
            "eu-west-1",
            "org/my-repo",
        ),
    ],
)
def test_valid_ecr_repository_uri(
    value: str, account_id: str, region: str, repository_name: str
) -> None:
    model = EcrModel(uri=value)
    assert str(model.uri) == value
    assert model.uri.account_id == account_id
    assert model.uri.region == region
    assert model.uri.repository_name == repository_name


@pytest.mark.parametrize(
    "value",
    [
        "not-a-uri",
        "12345.dkr.ecr.us-east-1.amazonaws.com/my-repo",
        "",
    ],
)
def test_invalid_ecr_repository_uri(value: str) -> None:
    with pytest.raises(ValidationError):
        EcrModel(uri=value)


def test_ecr_repository_uri_serialization() -> None:
    model = EcrModel(uri="123456789012.dkr.ecr.us-east-1.amazonaws.com/my-repo")
    dumped = model.model_dump()
    assert dumped == {"uri": "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-repo"}
    json_str = model.model_dump_json()
    restored = EcrModel.model_validate_json(json_str)
    assert restored.uri == model.uri


def test_ecr_repository_uri_existing_instance() -> None:
    uri = EcrRepositoryUri("123456789012.dkr.ecr.us-east-1.amazonaws.com/my-repo")
    model = EcrModel(uri=uri)
    assert model.uri is uri


def test_ecr_repository_uri_json_schema() -> None:
    schema = EcrModel.model_json_schema()
    field_schema = schema["properties"]["uri"]
    assert field_schema["type"] == "string"
    assert field_schema["format"] == "aws-ecr-repository-uri"
