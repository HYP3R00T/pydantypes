"""Tests for AWS security types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.aws.security import KmsKeyId, SecretsManagerSecretName, SsmParameterName


class KmsModel(BaseModel):
    key_id: KmsKeyId


class SecretsModel(BaseModel):
    secret_name: SecretsManagerSecretName


class SsmModel(BaseModel):
    param_name: SsmParameterName


@pytest.mark.parametrize(
    "value",
    [
        "12345678-1234-1234-1234-123456789012",
        "mrk-1234567890abcdef1234567890abcdef",
    ],
)
def test_valid_kms_key_id(value: str) -> None:
    model = KmsModel(key_id=value)
    assert model.key_id == value


@pytest.mark.parametrize("value", ["not-a-uuid", "mrk-short", ""])
def test_invalid_kms_key_id(value: str) -> None:
    with pytest.raises(ValidationError):
        KmsModel(key_id=value)


def test_kms_key_id_serialization() -> None:
    model = KmsModel(key_id="12345678-1234-1234-1234-123456789012")
    assert model.model_dump() == {"key_id": "12345678-1234-1234-1234-123456789012"}


@pytest.mark.parametrize("value", ["prod/my-app/db-password", "MySecret", "a"])
def test_valid_secrets_manager_secret_name(value: str) -> None:
    model = SecretsModel(secret_name=value)
    assert model.secret_name == value


@pytest.mark.parametrize("value", ["", "my secret!", "a" * 513])
def test_invalid_secrets_manager_secret_name(value: str) -> None:
    with pytest.raises(ValidationError):
        SecretsModel(secret_name=value)


def test_secrets_manager_secret_name_serialization() -> None:
    model = SecretsModel(secret_name="prod/my-app/db-password")
    assert model.model_dump() == {"secret_name": "prod/my-app/db-password"}


@pytest.mark.parametrize("value", ["/my-app/config/database-url", "MyParam", "param.name"])
def test_valid_ssm_parameter_name(value: str) -> None:
    model = SsmModel(param_name=value)
    assert model.param_name == value


@pytest.mark.parametrize("value", ["", "aws-reserved", "ssm-reserved", "a" * 1012])
def test_invalid_ssm_parameter_name(value: str) -> None:
    with pytest.raises(ValidationError):
        SsmModel(param_name=value)


def test_ssm_parameter_name_hierarchy_limit() -> None:
    deep_path = "/".join(["level"] * 17)
    with pytest.raises(ValidationError):
        SsmModel(param_name=deep_path)


def test_ssm_parameter_name_serialization() -> None:
    model = SsmModel(param_name="/my-app/config/database-url")
    assert model.model_dump() == {"param_name": "/my-app/config/database-url"}
