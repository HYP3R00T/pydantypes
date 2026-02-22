"""Tests for keyvault."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.azure.keyvault import KeyVaultUri


class KeyVaultUriModel(BaseModel):
    field: KeyVaultUri


@pytest.mark.parametrize(
    "value",
    [
        "https://my-vault.vault.azure.net/",
        "https://my-vault.vault.azure.net",
        "https://myvault1.vault.azure.net/",
    ],
)
def test_valid_key_vault_uri(value: str) -> None:
    m = KeyVaultUriModel(field=value)
    assert str(m.field) == value


@pytest.mark.parametrize(
    "value",
    [
        "http://my-vault.vault.azure.net/",
        "https://my-vault.vault.example.com/",
        "https://a.vault.azure.net/",
        "not-a-uri",
    ],
)
def test_invalid_key_vault_uri(value: str) -> None:
    with pytest.raises(ValidationError):
        KeyVaultUriModel(field=value)


def test_key_vault_uri_properties() -> None:
    m = KeyVaultUriModel(field="https://my-vault.vault.azure.net/")
    assert m.field.vault_name == "my-vault"


def test_key_vault_uri_serialization() -> None:
    m = KeyVaultUriModel(field="https://my-vault.vault.azure.net/")
    assert m.model_dump()["field"] == "https://my-vault.vault.azure.net/"


def test_key_vault_uri_json_schema() -> None:
    schema = KeyVaultUriModel.model_json_schema()
    props = schema["properties"]["field"]
    assert props["type"] == "string"
    assert props["format"] == "azure-key-vault-uri"


def test_key_vault_uri_existing_instance() -> None:
    uri = KeyVaultUri("https://my-vault.vault.azure.net/")
    m = KeyVaultUriModel(field=uri)
    assert m.field is uri
