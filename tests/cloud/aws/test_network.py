"""Tests for AWS network types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.aws.network import SecurityGroupId, SubnetId, VpcId


class VpcModel(BaseModel):
    vpc_id: VpcId


class SubnetModel(BaseModel):
    subnet_id: SubnetId


class SgModel(BaseModel):
    sg_id: SecurityGroupId


@pytest.mark.parametrize("value", ["vpc-1234567890abcdef0", "vpc-12345678"])
def test_valid_vpc_id(value: str) -> None:
    model = VpcModel(vpc_id=value)
    assert model.vpc_id == value


@pytest.mark.parametrize("value", ["vpc-", "vpc-UPPER", "ec2-12345678", ""])
def test_invalid_vpc_id(value: str) -> None:
    with pytest.raises(ValidationError):
        VpcModel(vpc_id=value)


@pytest.mark.parametrize("value", ["subnet-1234567890abcdef0", "subnet-12345678"])
def test_valid_subnet_id(value: str) -> None:
    model = SubnetModel(subnet_id=value)
    assert model.subnet_id == value


@pytest.mark.parametrize("value", ["subnet-", "subnet-UPPER", ""])
def test_invalid_subnet_id(value: str) -> None:
    with pytest.raises(ValidationError):
        SubnetModel(subnet_id=value)


@pytest.mark.parametrize("value", ["sg-1234567890abcdef0", "sg-12345678"])
def test_valid_security_group_id(value: str) -> None:
    model = SgModel(sg_id=value)
    assert model.sg_id == value


@pytest.mark.parametrize("value", ["sg-", "sg-UPPER", ""])
def test_invalid_security_group_id(value: str) -> None:
    with pytest.raises(ValidationError):
        SgModel(sg_id=value)


def test_vpc_id_serialization() -> None:
    model = VpcModel(vpc_id="vpc-1234567890abcdef0")
    assert model.model_dump() == {"vpc_id": "vpc-1234567890abcdef0"}
    json_str = model.model_dump_json()
    restored = VpcModel.model_validate_json(json_str)
    assert restored.vpc_id == model.vpc_id
