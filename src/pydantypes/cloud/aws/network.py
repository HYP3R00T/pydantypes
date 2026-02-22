"""AWS network types."""

from __future__ import annotations

import re
from typing import Annotated

from pydantic import AfterValidator, WithJsonSchema
from pydantic_core import PydanticCustomError

_VPC_ID_RE = re.compile(r"^vpc-[0-9a-f]{8,17}$")
_SUBNET_ID_RE = re.compile(r"^subnet-[0-9a-f]{8,17}$")
_SECURITY_GROUP_ID_RE = re.compile(r"^sg-[0-9a-f]{8,17}$")


def _validate_vpc_id(v: str) -> str:
    if not _VPC_ID_RE.match(v):
        raise PydanticCustomError("vpc_id", "Invalid VPC ID: {value}", {"value": v})
    return v


def _validate_subnet_id(v: str) -> str:
    if not _SUBNET_ID_RE.match(v):
        raise PydanticCustomError("subnet_id", "Invalid Subnet ID: {value}", {"value": v})
    return v


def _validate_security_group_id(v: str) -> str:
    if not _SECURITY_GROUP_ID_RE.match(v):
        raise PydanticCustomError(
            "security_group_id", "Invalid Security Group ID: {value}", {"value": v}
        )
    return v


VpcId = Annotated[
    str,
    AfterValidator(_validate_vpc_id),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": r"^vpc-[0-9a-f]{8,17}$",
            "description": "An AWS VPC ID",
            "examples": ["vpc-1234567890abcdef0"],
            "title": "VpcId",
        }
    ),
]

SubnetId = Annotated[
    str,
    AfterValidator(_validate_subnet_id),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": r"^subnet-[0-9a-f]{8,17}$",
            "description": "An AWS Subnet ID",
            "examples": ["subnet-1234567890abcdef0"],
            "title": "SubnetId",
        }
    ),
]

SecurityGroupId = Annotated[
    str,
    AfterValidator(_validate_security_group_id),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": r"^sg-[0-9a-f]{8,17}$",
            "description": "An AWS Security Group ID",
            "examples": ["sg-1234567890abcdef0"],
            "title": "SecurityGroupId",
        }
    ),
]
