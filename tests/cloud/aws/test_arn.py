"""Tests for AWS ARN types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.aws.arn import Arn, IamRoleArn, SnsTopicArn


class ArnModel(BaseModel):
    arn: Arn


class IamRoleArnModel(BaseModel):
    arn: IamRoleArn


class SnsTopicArnModel(BaseModel):
    arn: SnsTopicArn


@pytest.mark.parametrize(
    ("value", "partition", "service", "region", "account_id", "resource"),
    [
        (
            "arn:aws:iam::123456789012:role/MyRole",
            "aws",
            "iam",
            "",
            "123456789012",
            "role/MyRole",
        ),
        (
            "arn:aws:s3:::my-bucket",
            "aws",
            "s3",
            "",
            "",
            "my-bucket",
        ),
        (
            "arn:aws-cn:ec2:cn-north-1:123456789012:instance/i-1234",
            "aws-cn",
            "ec2",
            "cn-north-1",
            "123456789012",
            "instance/i-1234",
        ),
        (
            "arn:aws:sns:us-east-1:123456789012:my-topic",
            "aws",
            "sns",
            "us-east-1",
            "123456789012",
            "my-topic",
        ),
    ],
)
def test_valid_arn(
    value: str,
    partition: str,
    service: str,
    region: str,
    account_id: str,
    resource: str,
) -> None:
    model = ArnModel(arn=value)
    assert str(model.arn) == value
    assert model.arn.partition == partition
    assert model.arn.service == service
    assert model.arn.region == region
    assert model.arn.account_id == account_id
    assert model.arn.resource == resource


@pytest.mark.parametrize(
    "value",
    [
        "not-an-arn",
        "arn:invalid:s3:::bucket",
        "",
        "arn:aws:",
    ],
)
def test_invalid_arn(value: str) -> None:
    with pytest.raises(ValidationError):
        ArnModel(arn=value)


def test_arn_serialization() -> None:
    model = ArnModel(arn="arn:aws:s3:::my-bucket")
    assert model.model_dump() == {"arn": "arn:aws:s3:::my-bucket"}
    json_str = model.model_dump_json()
    restored = ArnModel.model_validate_json(json_str)
    assert restored.arn == model.arn


def test_arn_existing_instance() -> None:
    arn = Arn("arn:aws:s3:::my-bucket")
    model = ArnModel(arn=arn)
    assert model.arn is arn


def test_arn_json_schema() -> None:
    schema = ArnModel.model_json_schema()
    field_schema = schema["properties"]["arn"]
    assert field_schema["type"] == "string"
    assert field_schema["format"] == "aws-arn"


@pytest.mark.parametrize(
    ("value", "role_name"),
    [
        ("arn:aws:iam::123456789012:role/MyRole", "MyRole"),
        ("arn:aws:iam::123456789012:role/path/to/role", "path/to/role"),
    ],
)
def test_valid_iam_role_arn(value: str, role_name: str) -> None:
    model = IamRoleArnModel(arn=value)
    assert model.arn.role_name == role_name
    assert model.arn.service == "iam"


@pytest.mark.parametrize(
    "value",
    [
        "arn:aws:s3:::my-bucket",
        "arn:aws:iam::123456789012:user/MyUser",
    ],
)
def test_invalid_iam_role_arn(value: str) -> None:
    with pytest.raises(ValidationError):
        IamRoleArnModel(arn=value)


def test_iam_role_arn_existing_instance() -> None:
    arn = IamRoleArn("arn:aws:iam::123456789012:role/MyRole")
    model = IamRoleArnModel(arn=arn)
    assert model.arn is arn


@pytest.mark.parametrize(
    ("value", "topic_name"),
    [
        ("arn:aws:sns:us-east-1:123456789012:my-topic", "my-topic"),
    ],
)
def test_valid_sns_topic_arn(value: str, topic_name: str) -> None:
    model = SnsTopicArnModel(arn=value)
    assert model.arn.topic_name == topic_name
    assert model.arn.service == "sns"


@pytest.mark.parametrize(
    "value",
    [
        "arn:aws:sqs:us-east-1:123456789012:my-queue",
    ],
)
def test_invalid_sns_topic_arn(value: str) -> None:
    with pytest.raises(ValidationError):
        SnsTopicArnModel(arn=value)


def test_sns_topic_arn_existing_instance() -> None:
    arn = SnsTopicArn("arn:aws:sns:us-east-1:123456789012:my-topic")
    model = SnsTopicArnModel(arn=arn)
    assert model.arn is arn
