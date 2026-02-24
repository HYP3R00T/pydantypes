"""Tests for CloudStorageUri base class."""

from __future__ import annotations

import pytest

from pydantypes.cloud._base import CloudStorageUri
from pydantypes.cloud.aws.storage import S3Uri
from pydantypes.cloud.azure.storage import BlobStorageUri
from pydantypes.cloud.gcp.storage import GcsUri

# ---------------------------------------------------------------------------
# Polymorphism
# ---------------------------------------------------------------------------


def test_s3_uri_is_cloud_storage_uri() -> None:
    uri = S3Uri("s3://my-bucket/key")
    assert isinstance(uri, CloudStorageUri)


def test_gcs_uri_is_cloud_storage_uri() -> None:
    uri = GcsUri("gs://my-bucket/key")
    assert isinstance(uri, CloudStorageUri)


def test_blob_storage_uri_is_cloud_storage_uri() -> None:
    uri = BlobStorageUri("https://abc.blob.core.windows.net/mycontainer/key")
    assert isinstance(uri, CloudStorageUri)


# ---------------------------------------------------------------------------
# Core path helpers — parametrized via S3Uri
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("key", "expected_name"),
    [
        ("path/to/file.csv", "file.csv"),
        ("file.csv", "file.csv"),
        ("path/to/", "to"),
        ("", ""),
        ("noext", "noext"),
        (".hidden", ".hidden"),
    ],
)
def test_name(key: str, expected_name: str) -> None:
    uri_str = f"s3://my-bucket/{key}" if key else "s3://my-bucket"
    uri = S3Uri(uri_str)
    assert uri.name == expected_name


@pytest.mark.parametrize(
    ("key", "expected_suffix"),
    [
        ("path/to/file.csv", ".csv"),
        ("file.tar.gz", ".gz"),
        ("noext", ""),
        ("", ""),
        (".hidden", ""),
        ("path/to/", ""),
    ],
)
def test_suffix(key: str, expected_suffix: str) -> None:
    uri_str = f"s3://my-bucket/{key}" if key else "s3://my-bucket"
    uri = S3Uri(uri_str)
    assert uri.suffix == expected_suffix


@pytest.mark.parametrize(
    ("key", "expected_stem"),
    [
        ("path/to/file.csv", "file"),
        ("file.tar.gz", "file.tar"),
        ("noext", "noext"),
        ("", ""),
        (".hidden", ".hidden"),
    ],
)
def test_stem(key: str, expected_stem: str) -> None:
    uri_str = f"s3://my-bucket/{key}" if key else "s3://my-bucket"
    uri = S3Uri(uri_str)
    assert uri.stem == expected_stem


@pytest.mark.parametrize(
    ("key", "expected_parent"),
    [
        ("path/to/file.csv", "path/to"),
        ("file.csv", ""),
        ("a/b/c/d.txt", "a/b/c"),
        ("", ""),
    ],
)
def test_parent_key(key: str, expected_parent: str) -> None:
    uri_str = f"s3://my-bucket/{key}" if key else "s3://my-bucket"
    uri = S3Uri(uri_str)
    assert uri.parent_key == expected_parent


# ---------------------------------------------------------------------------
# Extended path helpers
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("key", "expected_suffixes"),
    [
        ("file.tar.gz", [".tar", ".gz"]),
        ("file.csv", [".csv"]),
        ("noext", []),
        ("", []),
        (".hidden", []),
    ],
)
def test_suffixes(key: str, expected_suffixes: list[str]) -> None:
    uri_str = f"s3://my-bucket/{key}" if key else "s3://my-bucket"
    uri = S3Uri(uri_str)
    assert uri.suffixes == expected_suffixes


@pytest.mark.parametrize(
    ("key", "expected_parts"),
    [
        ("path/to/file.csv", ("path", "to", "file.csv")),
        ("file.csv", ("file.csv",)),
        ("a/b/c", ("a", "b", "c")),
        ("", ()),
    ],
)
def test_parts(key: str, expected_parts: tuple[str, ...]) -> None:
    uri_str = f"s3://my-bucket/{key}" if key else "s3://my-bucket"
    uri = S3Uri(uri_str)
    assert uri.parts == expected_parts


# ---------------------------------------------------------------------------
# Heuristic helpers
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("key", "expected_is_file", "expected_is_folder"),
    [
        ("path/to/file.csv", True, False),
        ("path/to/", False, True),
        ("", False, True),
        ("file", True, False),
        ("prefix/", False, True),
    ],
)
def test_is_file_is_folder(key: str, expected_is_file: bool, expected_is_folder: bool) -> None:
    uri_str = f"s3://my-bucket/{key}" if key else "s3://my-bucket"
    uri = S3Uri(uri_str)
    assert uri.is_file is expected_is_file
    assert uri.is_folder is expected_is_folder


# ---------------------------------------------------------------------------
# Cross-provider: path helpers work on all providers
# ---------------------------------------------------------------------------


def test_gcs_uri_path_helpers() -> None:
    uri = GcsUri("gs://my-bucket/path/to/data.parquet")
    assert uri.name == "data.parquet"
    assert uri.suffix == ".parquet"
    assert uri.stem == "data"
    assert uri.parent_key == "path/to"


def test_blob_storage_uri_path_helpers() -> None:
    uri = BlobStorageUri("https://abc.blob.core.windows.net/mycontainer/path/to/data.parquet")
    assert uri.name == "data.parquet"
    assert uri.suffix == ".parquet"
    assert uri.stem == "data"
    assert uri.parent_key == "path/to"
