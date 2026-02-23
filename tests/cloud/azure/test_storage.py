"""Tests for Azure storage types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.azure.storage import BlobStorageUri, StorageAccountName


class BlobStorageUriModel(BaseModel):
    field: BlobStorageUri


class StorageAccountNameModel(BaseModel):
    field: StorageAccountName


@pytest.mark.parametrize(
    "value",
    [
        "https://myaccount.blob.core.windows.net/mycontainer/path/to/blob",
        "https://myaccount.blob.core.windows.net/mycontainer",
        "https://abc.blob.core.windows.net/abc",
    ],
)
def test_valid_blob_storage_uri(value: str) -> None:
    m = BlobStorageUriModel(field=value)
    assert str(m.field) == value


@pytest.mark.parametrize(
    "value",
    [
        "http://myaccount.blob.core.windows.net/abc",
        "https://ab.blob.core.windows.net/abc",
        "https://myaccount.blob.core.windows.net",
        "not-a-uri",
        "https://abc.blob.core.windows.net/c",
        "https://abc.blob.core.windows.net/ab",
    ],
)
def test_invalid_blob_storage_uri(value: str) -> None:
    with pytest.raises(ValidationError):
        BlobStorageUriModel(field=value)


def test_blob_storage_uri_properties() -> None:
    m = BlobStorageUriModel(
        field="https://myaccount.blob.core.windows.net/mycontainer/path/to/blob"
    )
    assert m.field.account_name == "myaccount"
    assert m.field.container == "mycontainer"
    assert m.field.blob_path == "path/to/blob"


def test_blob_storage_uri_no_path() -> None:
    m = BlobStorageUriModel(field="https://myaccount.blob.core.windows.net/mycontainer")
    assert m.field.blob_path == ""


def test_blob_storage_uri_serialization() -> None:
    m = BlobStorageUriModel(
        field="https://myaccount.blob.core.windows.net/mycontainer/path/to/blob"
    )
    assert (
        m.model_dump()["field"]
        == "https://myaccount.blob.core.windows.net/mycontainer/path/to/blob"
    )


def test_blob_storage_uri_json_schema() -> None:
    schema = BlobStorageUriModel.model_json_schema()
    props = schema["properties"]["field"]
    assert props["type"] == "string"
    assert props["format"] == "azure-blob-storage-uri"


def test_blob_storage_uri_existing_instance() -> None:
    uri = BlobStorageUri("https://myaccount.blob.core.windows.net/mycontainer/path/to/blob")
    m = BlobStorageUriModel(field=uri)
    assert m.field is uri


@pytest.mark.parametrize("value", ["mystorageaccount", "abc", "a1b"])
def test_valid_storage_account_name(value: str) -> None:
    m = StorageAccountNameModel(field=value)
    assert m.field == value


@pytest.mark.parametrize("value", ["ab", "MyAccount", "my-account", "a" * 25, ""])
def test_invalid_storage_account_name(value: str) -> None:
    with pytest.raises(ValidationError):
        StorageAccountNameModel(field=value)


def test_storage_account_name_serialization() -> None:
    m = StorageAccountNameModel(field="mystorageaccount")
    assert m.model_dump()["field"] == "mystorageaccount"
