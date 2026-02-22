"""Tests for AWS S3 storage types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.aws.storage import S3Uri


class S3UriModel(BaseModel):
    uri: S3Uri


@pytest.mark.parametrize(
    ("value", "expected_bucket", "expected_key"),
    [
        ("s3://my-bucket/my-key", "my-bucket", "my-key"),
        ("s3://my-bucket/path/to/file.csv", "my-bucket", "path/to/file.csv"),
        ("s3://my-bucket", "my-bucket", ""),
        ("s3://my-bucket/", "my-bucket", ""),
        ("s3://my.dotted.bucket/key", "my.dotted.bucket", "key"),
        ("s3://a1b2c3d4/key", "a1b2c3d4", "key"),
    ],
)
def test_valid_s3_uri(value: str, expected_bucket: str, expected_key: str) -> None:
    model = S3UriModel(uri=value)
    assert str(model.uri) == value
    assert model.uri.bucket == expected_bucket
    assert model.uri.key == expected_key


@pytest.mark.parametrize(
    "value",
    [
        "s3://",
        "s3:///no-bucket",
        "http://bucket/key",
        "s3://UPPER/key",
        "",
        "s3://-invalid/key",
        "not-an-s3-uri",
    ],
)
def test_invalid_s3_uri(value: str) -> None:
    with pytest.raises(ValidationError):
        S3UriModel(uri=value)


def test_s3_uri_serialization() -> None:
    model = S3UriModel(uri="s3://my-bucket/my-key")
    assert model.model_dump() == {"uri": "s3://my-bucket/my-key"}
    json_str = model.model_dump_json()
    restored = S3UriModel.model_validate_json(json_str)
    assert restored.uri == model.uri
    assert restored.uri.bucket == model.uri.bucket


def test_s3_uri_existing_instance() -> None:
    uri = S3Uri("s3://my-bucket/my-key")
    model = S3UriModel(uri=uri)
    assert model.uri is uri


def test_s3_uri_json_schema() -> None:
    schema = S3UriModel.model_json_schema()
    field_schema = schema["properties"]["uri"]
    assert field_schema["type"] == "string"
    assert field_schema["format"] == "s3-uri"
    assert "pattern" in field_schema
