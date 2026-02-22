"""AWS compute types."""

from __future__ import annotations

import re
from typing import Annotated

from pydantic import AfterValidator, WithJsonSchema
from pydantic_core import PydanticCustomError

_EC2_INSTANCE_ID_RE = re.compile(r"^i-[0-9a-f]{8,17}$")
_LAMBDA_FUNCTION_NAME_RE = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")


def _validate_ec2_instance_id(v: str) -> str:
    if not _EC2_INSTANCE_ID_RE.match(v):
        raise PydanticCustomError(
            "ec2_instance_id",
            "Invalid EC2 Instance ID: {value}",
            {"value": v},
        )
    return v


def _validate_lambda_function_name(v: str) -> str:
    if not _LAMBDA_FUNCTION_NAME_RE.match(v):
        raise PydanticCustomError(
            "lambda_function_name",
            "Invalid Lambda function name: {value}",
            {"value": v},
        )
    return v


Ec2InstanceId = Annotated[
    str,
    AfterValidator(_validate_ec2_instance_id),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": r"^i-[0-9a-f]{8,17}$",
            "description": "An AWS EC2 instance ID",
            "examples": ["i-1234567890abcdef0"],
            "title": "Ec2InstanceId",
        }
    ),
]

LambdaFunctionName = Annotated[
    str,
    AfterValidator(_validate_lambda_function_name),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": r"^[a-zA-Z0-9_-]{1,64}$",
            "description": "An AWS Lambda function name",
            "examples": ["my-function"],
            "title": "LambdaFunctionName",
            "maxLength": 64,
        }
    ),
]
