"""Tests for AWS compute types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.aws.compute import Ec2InstanceId, LambdaFunctionName


class Ec2Model(BaseModel):
    instance_id: Ec2InstanceId


class LambdaModel(BaseModel):
    name: LambdaFunctionName


@pytest.mark.parametrize("value", ["i-1234567890abcdef0", "i-12345678", "i-abcdef1234567890a"])
def test_valid_ec2_instance_id(value: str) -> None:
    model = Ec2Model(instance_id=value)
    assert model.instance_id == value


@pytest.mark.parametrize("value", ["i-", "i-UPPER", "ec2-12345678", "i-1234567", ""])
def test_invalid_ec2_instance_id(value: str) -> None:
    with pytest.raises(ValidationError):
        Ec2Model(instance_id=value)


def test_ec2_instance_id_serialization() -> None:
    model = Ec2Model(instance_id="i-1234567890abcdef0")
    assert model.model_dump() == {"instance_id": "i-1234567890abcdef0"}
    json_str = model.model_dump_json()
    restored = Ec2Model.model_validate_json(json_str)
    assert restored.instance_id == model.instance_id


@pytest.mark.parametrize("value", ["my-function", "a", "my_function_123", "A-B-C"])
def test_valid_lambda_function_name(value: str) -> None:
    model = LambdaModel(name=value)
    assert model.name == value


@pytest.mark.parametrize("value", ["", "a" * 65, "my function"])
def test_invalid_lambda_function_name(value: str) -> None:
    with pytest.raises(ValidationError):
        LambdaModel(name=value)


def test_lambda_function_name_serialization() -> None:
    model = LambdaModel(name="my-function")
    assert model.model_dump() == {"name": "my-function"}
    json_str = model.model_dump_json()
    restored = LambdaModel.model_validate_json(json_str)
    assert restored.name == model.name
