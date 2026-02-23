"""Tests for AWS identity types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.aws.identity import AccountId, CognitoUserPoolId, Region


class AccountIdModel(BaseModel):
    account_id: AccountId


class RegionModel(BaseModel):
    region: Region


class CognitoModel(BaseModel):
    pool_id: CognitoUserPoolId


@pytest.mark.parametrize("value", ["123456789012", "000000000000", "999999999999"])
def test_valid_account_id(value: str) -> None:
    model = AccountIdModel(account_id=value)
    assert model.account_id == value


@pytest.mark.parametrize(
    "value",
    ["12345", "abcdefghijkl", "1234567890123", "", "12345678901"],
)
def test_invalid_account_id(value: str) -> None:
    with pytest.raises(ValidationError):
        AccountIdModel(account_id=value)


def test_account_id_serialization() -> None:
    model = AccountIdModel(account_id="123456789012")
    assert model.model_dump() == {"account_id": "123456789012"}
    json_str = model.model_dump_json()
    restored = AccountIdModel.model_validate_json(json_str)
    assert restored.account_id == model.account_id


def test_account_id_json_schema() -> None:
    schema = AccountIdModel.model_json_schema()
    field_schema = schema["properties"]["account_id"]
    assert field_schema["type"] == "string"
    assert "pattern" in field_schema


@pytest.mark.parametrize(
    "value", ["us-east-1", "eu-west-1", "ap-southeast-1", "ap-southeast-5", "mx-central-1"]
)
def test_valid_region(value: str) -> None:
    model = RegionModel(region=value)
    assert model.region == value


@pytest.mark.parametrize("value", ["invalid-region", "US-EAST-1", ""])
def test_invalid_region(value: str) -> None:
    with pytest.raises(ValidationError):
        RegionModel(region=value)


def test_region_serialization() -> None:
    model = RegionModel(region="us-east-1")
    assert model.model_dump() == {"region": "us-east-1"}
    json_str = model.model_dump_json()
    restored = RegionModel.model_validate_json(json_str)
    assert restored.region == model.region


@pytest.mark.parametrize("value", ["us-east-1_AbCdEfGhI", "eu-west-1_abc123"])
def test_valid_cognito_user_pool_id(value: str) -> None:
    model = CognitoModel(pool_id=value)
    assert model.pool_id == value


@pytest.mark.parametrize("value", ["no-underscore", "", "a" * 56])
def test_invalid_cognito_user_pool_id(value: str) -> None:
    with pytest.raises(ValidationError):
        CognitoModel(pool_id=value)


def test_cognito_user_pool_id_serialization() -> None:
    model = CognitoModel(pool_id="us-east-1_AbCdEfGhI")
    assert model.model_dump() == {"pool_id": "us-east-1_AbCdEfGhI"}
