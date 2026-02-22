from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.gcp.storage import GcsUri


class GcsModel(BaseModel):
    uri: GcsUri


class TestGcsUriValid:
    def test_bucket_and_path(self) -> None:
        uri = GcsUri("gs://my-bucket/path/to/file")
        assert uri.bucket == "my-bucket"
        assert uri.path == "path/to/file"

    def test_no_path(self) -> None:
        uri = GcsUri("gs://my-bucket")
        assert uri.bucket == "my-bucket"
        assert uri.path == ""

    def test_dotted_bucket(self) -> None:
        uri = GcsUri("gs://my.dotted.bucket/key")
        assert uri.bucket == "my.dotted.bucket"
        assert uri.path == "key"

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
    ],
)
class TestGcsUriInvalid:
    def test_pydantic_rejects(self, value: str) -> None:
        with pytest.raises(ValidationError):
            GcsModel(uri=value)
