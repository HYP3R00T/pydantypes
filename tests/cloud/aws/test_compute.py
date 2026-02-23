"""Tests for AWS compute types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.aws.compute import (
    AmiId,
    Ec2InstanceId,
    EcsClusterName,
    EksClusterName,
    LambdaFunctionName,
)


class Ec2Model(BaseModel):
    instance_id: Ec2InstanceId


class LambdaModel(BaseModel):
    name: LambdaFunctionName


class AmiModel(BaseModel):
    ami_id: AmiId


class EcsModel(BaseModel):
    cluster: EcsClusterName


class EksModel(BaseModel):
    cluster: EksClusterName


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


@pytest.mark.parametrize(
    "value", ["my-function", "a", "my_function_123", "A-B-C", "my.function.v2"]
)
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


@pytest.mark.parametrize("value", ["ami-1234567890abcdef0", "ami-12345678"])
def test_valid_ami_id(value: str) -> None:
    model = AmiModel(ami_id=value)
    assert model.ami_id == value


@pytest.mark.parametrize("value", ["ami-", "ami-UPPER", "i-12345678", ""])
def test_invalid_ami_id(value: str) -> None:
    with pytest.raises(ValidationError):
        AmiModel(ami_id=value)


def test_ami_id_serialization() -> None:
    model = AmiModel(ami_id="ami-1234567890abcdef0")
    assert model.model_dump() == {"ami_id": "ami-1234567890abcdef0"}


@pytest.mark.parametrize("value", ["my-ecs-cluster", "a", "cluster_123"])
def test_valid_ecs_cluster_name(value: str) -> None:
    model = EcsModel(cluster=value)
    assert model.cluster == value


@pytest.mark.parametrize("value", ["", "a" * 256, "my cluster"])
def test_invalid_ecs_cluster_name(value: str) -> None:
    with pytest.raises(ValidationError):
        EcsModel(cluster=value)


def test_ecs_cluster_name_serialization() -> None:
    model = EcsModel(cluster="my-ecs-cluster")
    assert model.model_dump() == {"cluster": "my-ecs-cluster"}


@pytest.mark.parametrize("value", ["my-eks-cluster", "a", "cluster123"])
def test_valid_eks_cluster_name(value: str) -> None:
    model = EksModel(cluster=value)
    assert model.cluster == value


@pytest.mark.parametrize("value", ["", "-starts", "a" * 101])
def test_invalid_eks_cluster_name(value: str) -> None:
    with pytest.raises(ValidationError):
        EksModel(cluster=value)


def test_eks_cluster_name_serialization() -> None:
    model = EksModel(cluster="my-eks-cluster")
    assert model.model_dump() == {"cluster": "my-eks-cluster"}
