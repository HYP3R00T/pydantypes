"""AWS ARN types."""

from __future__ import annotations

import re
from typing import Any, ClassVar, cast

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError

from pydantypes._internal import _str_type_core_schema


class Arn(str):
    """An AWS ARN with parsed components."""

    _pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"^arn:(aws|aws-cn|aws-us-gov):([a-z0-9-]+):([a-z0-9-]*):(\d{12}|):(.+)$"
    )

    partition: str  # type: ignore[assignment]
    service: str
    region: str
    account_id: str
    resource: str

    def __new__(cls, value: str) -> Arn:
        m = cls._pattern.match(value)
        if not m:
            raise PydanticCustomError(
                "arn",
                "Invalid AWS ARN: {value}",
                {"value": value},
            )
        instance = str.__new__(cls, value)
        instance.partition = m.group(1)
        instance.service = m.group(2)
        instance.region = m.group(3)
        instance.account_id = m.group(4)
        instance.resource = m.group(5)
        return instance

    @classmethod
    def _validate(cls, value: str) -> Arn:
        return cls(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return _str_type_core_schema(cls, source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {
            "type": "string",
            "format": "aws-arn",
            "pattern": cls._pattern.pattern,
            "description": (
                "An AWS ARN in the format arn:partition:service:region:account-id:resource"
            ),
            "examples": ["arn:aws:iam::123456789012:role/MyRole"],
            "title": "Arn",
        }


class IamRoleArn(Arn):
    """An IAM Role ARN with parsed role name."""

    role_name: str

    def __new__(cls, value: str) -> IamRoleArn:
        instance = cast(IamRoleArn, Arn.__new__(cls, value))
        if instance.service != "iam" or not instance.resource.startswith("role/"):
            raise PydanticCustomError(
                "iam_role_arn",
                "Invalid IAM Role ARN: expected service 'iam'"
                " with resource 'role/...'. Got: {value}",
                {"value": value},
            )
        instance.role_name = instance.resource.removeprefix("role/")
        return instance

    @classmethod
    def _validate(cls, value: str) -> IamRoleArn:
        return cls(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return _str_type_core_schema(cls, source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {
            "type": "string",
            "format": "aws-iam-role-arn",
            "pattern": Arn._pattern.pattern,
            "description": "An AWS IAM Role ARN",
            "examples": ["arn:aws:iam::123456789012:role/MyRole"],
            "title": "IamRoleArn",
        }


class SnsTopicArn(Arn):
    """An SNS Topic ARN with parsed topic name."""

    topic_name: str

    def __new__(cls, value: str) -> SnsTopicArn:
        instance = cast(SnsTopicArn, Arn.__new__(cls, value))
        if instance.service != "sns":
            raise PydanticCustomError(
                "sns_topic_arn",
                "Invalid SNS Topic ARN: expected service 'sns'. Got: {value}",
                {"value": value},
            )
        instance.topic_name = instance.resource
        return instance

    @classmethod
    def _validate(cls, value: str) -> SnsTopicArn:
        return cls(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return _str_type_core_schema(cls, source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {
            "type": "string",
            "format": "aws-sns-topic-arn",
            "pattern": Arn._pattern.pattern,
            "description": "An AWS SNS Topic ARN",
            "examples": ["arn:aws:sns:us-east-1:123456789012:my-topic"],
            "title": "SnsTopicArn",
        }
