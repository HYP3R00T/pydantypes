"""Tests for GCP storage types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.gcp.storage import GcsBucketName, GcsUri


class GcsModel(BaseModel):
    uri: GcsUri


class BucketModel(BaseModel):
    bucket: GcsBucketName


class TestGcsUriValid:
    def test_bucket_and_key(self) -> None:
        uri = GcsUri("gs://my-bucket/path/to/file")
        assert uri.bucket == "my-bucket"
        assert uri.key == "path/to/file"

    def test_no_key(self) -> None:
        uri = GcsUri("gs://my-bucket")
        assert uri.bucket == "my-bucket"
        assert uri.key == ""

    def test_dotted_bucket(self) -> None:
        uri = GcsUri("gs://my.dotted.bucket/key")
        assert uri.bucket == "my.dotted.bucket"
        assert uri.key == "key"

    def test_pydantic_model(self) -> None:
        m = GcsModel(uri="gs://my-bucket/path/to/file")
        assert isinstance(m.uri, GcsUri)
        assert m.uri.bucket == "my-bucket"


@pytest.mark.parametrize(
    "value",
    [
        "gs://",
        "gs:///no-bucket",
        "s3://bucket/key",
        "gs://UPPER/key",
        "",
        "gs://my..bucket/key",
        "gs://my-.bucket/key",
        "gs://googbucket/key",
        "gs://my-google-bucket/key",
    ],
)
class TestGcsUriInvalid:
    def test_pydantic_rejects(self, value: str) -> None:
        with pytest.raises(ValidationError):
            GcsModel(uri=value)


def test_gcs_uri_serialization() -> None:
    m = GcsModel(uri="gs://my-bucket/path/to/file")
    assert m.model_dump()["uri"] == "gs://my-bucket/path/to/file"


def test_gcs_uri_json_schema() -> None:
    schema = GcsModel.model_json_schema()
    props = schema["properties"]["uri"]
    assert props["type"] == "string"
    assert props["format"] == "gcs-uri"


def test_gcs_uri_existing_instance() -> None:
    uri = GcsUri("gs://my-bucket/path/to/file")
    m = GcsModel(uri=uri)
    assert m.uri is uri


@pytest.mark.parametrize("value", ["my-bucket", "abc", "my.dotted.bucket"])
def test_valid_gcs_bucket_name(value: str) -> None:
    m = BucketModel(bucket=value)
    assert m.bucket == value


@pytest.mark.parametrize(
    "value",
    [
        "ab",
        "UPPER",
        "my..bucket",
        "my-.bucket",
        "my.-bucket",
        "192.168.1.1",
        "googbucket",
        "my-google-bucket",
        "",
    ],
)
def test_invalid_gcs_bucket_name(value: str) -> None:
    with pytest.raises(ValidationError):
        BucketModel(bucket=value)


def test_gcs_bucket_name_serialization() -> None:
    m = BucketModel(bucket="my-bucket")
    assert m.model_dump()["bucket"] == "my-bucket"
