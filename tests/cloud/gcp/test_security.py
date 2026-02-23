"""Tests for GCP security types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.gcp.security import (
    KmsKeyName,
    SecretManagerSecretName,
    SecretManagerVersionName,
)


class SecretModel(BaseModel):
    secret: SecretManagerSecretName


class VersionModel(BaseModel):
    version: SecretManagerVersionName


class KmsModel(BaseModel):
    key: KmsKeyName


@pytest.mark.parametrize(
    "value",
    [
        "projects/my-project/secrets/my-secret",
        "projects/123456789012/secrets/my_secret_123",
    ],
)
def test_valid_secret_manager_secret_name(value: str) -> None:
    m = SecretModel(secret=value)
    assert str(m.secret) == value


def test_secret_manager_secret_name_properties() -> None:
    m = SecretModel(secret="projects/my-project/secrets/my-secret")
    assert m.secret.project_id == "my-project"
    assert m.secret.secret_id == "my-secret"


@pytest.mark.parametrize(
    "value",
    [
        "my-project/secrets/my-secret",
        "projects/ab/secrets/my-secret",
        "projects/my-project/secrets/",
        "not-valid",
    ],
)
def test_invalid_secret_manager_secret_name(value: str) -> None:
    with pytest.raises(ValidationError):
        SecretModel(secret=value)


def test_secret_manager_secret_name_serialization() -> None:
    m = SecretModel(secret="projects/my-project/secrets/my-secret")
    assert m.model_dump()["secret"] == "projects/my-project/secrets/my-secret"


def test_secret_manager_secret_name_json_schema() -> None:
    schema = SecretModel.model_json_schema()
    props = schema["properties"]["secret"]
    assert props["type"] == "string"
    assert props["format"] == "gcp-secret-manager-secret-name"


def test_secret_manager_secret_name_existing_instance() -> None:
    s = SecretManagerSecretName("projects/my-project/secrets/my-secret")
    m = SecretModel(secret=s)
    assert m.secret is s


@pytest.mark.parametrize(
    "value",
    [
        "projects/my-project/secrets/my-secret/versions/1",
        "projects/my-project/secrets/my-secret/versions/latest",
        "projects/123456789012/secrets/my-secret/versions/42",
    ],
)
def test_valid_secret_manager_version_name(value: str) -> None:
    m = VersionModel(version=value)
    assert str(m.version) == value


def test_secret_manager_version_name_properties() -> None:
    m = VersionModel(version="projects/my-project/secrets/my-secret/versions/3")
    assert m.version.project_id == "my-project"
    assert m.version.secret_id == "my-secret"
    assert m.version.version == "3"


def test_secret_manager_version_name_latest() -> None:
    m = VersionModel(version="projects/my-project/secrets/my-secret/versions/latest")
    assert m.version.version == "latest"


@pytest.mark.parametrize(
    "value",
    [
        "projects/my-project/secrets/my-secret/versions/",
        "projects/ab/secrets/my-secret/versions/1",
        "projects/my-project/secrets/my-secret",
        "not-valid",
    ],
)
def test_invalid_secret_manager_version_name(value: str) -> None:
    with pytest.raises(ValidationError):
        VersionModel(version=value)


def test_secret_manager_version_name_serialization() -> None:
    m = VersionModel(version="projects/my-project/secrets/my-secret/versions/1")
    assert m.model_dump()["version"] == "projects/my-project/secrets/my-secret/versions/1"


def test_secret_manager_version_name_json_schema() -> None:
    schema = VersionModel.model_json_schema()
    props = schema["properties"]["version"]
    assert props["type"] == "string"
    assert props["format"] == "gcp-secret-manager-version-name"


def test_secret_manager_version_name_existing_instance() -> None:
    v = SecretManagerVersionName("projects/my-project/secrets/my-secret/versions/1")
    m = VersionModel(version=v)
    assert m.version is v


VALID_KMS = "projects/my-project/locations/us-central1/keyRings/my-ring/cryptoKeys/my-key"


@pytest.mark.parametrize(
    "value",
    [
        VALID_KMS,
        "projects/123456789012/locations/global/keyRings/ring-1/cryptoKeys/key_2",
    ],
)
def test_valid_kms_key_name(value: str) -> None:
    m = KmsModel(key=value)
    assert str(m.key) == value


def test_kms_key_name_properties() -> None:
    m = KmsModel(key=VALID_KMS)
    assert m.key.project_id == "my-project"
    assert m.key.location == "us-central1"
    assert m.key.key_ring == "my-ring"
    assert m.key.key_name == "my-key"


@pytest.mark.parametrize(
    "value",
    [
        "projects/ab/locations/us/keyRings/ring/cryptoKeys/key",
        "projects/my-project/keyRings/ring/cryptoKeys/key",
        "not-valid",
    ],
)
def test_invalid_kms_key_name(value: str) -> None:
    with pytest.raises(ValidationError):
        KmsModel(key=value)


def test_kms_key_name_serialization() -> None:
    m = KmsModel(key=VALID_KMS)
    assert m.model_dump()["key"] == VALID_KMS


def test_kms_key_name_json_schema() -> None:
    schema = KmsModel.model_json_schema()
    props = schema["properties"]["key"]
    assert props["type"] == "string"
    assert props["format"] == "gcp-kms-key-name"


def test_kms_key_name_existing_instance() -> None:
    k = KmsKeyName(VALID_KMS)
    m = KmsModel(key=k)
    assert m.key is k
