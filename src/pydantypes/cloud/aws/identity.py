"""AWS identity types."""

from __future__ import annotations

import re
import sys
from typing import Annotated

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from enum import Enum

    class StrEnum(str, Enum):
        pass


from pydantic import AfterValidator, WithJsonSchema
from pydantic_core import PydanticCustomError

_ACCOUNT_ID_RE = re.compile(r"^\d{12}$")


def _validate_account_id(v: str) -> str:
    if not _ACCOUNT_ID_RE.match(v):
        raise PydanticCustomError(
            "aws_account_id",
            "Invalid AWS Account ID: must be a 12-digit string. Got: {value}",
            {"value": v},
        )
    return v


AccountId = Annotated[
    str,
    AfterValidator(_validate_account_id),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": r"^\d{12}$",
            "description": "A 12-digit AWS Account ID",
            "examples": ["123456789012"],
            "title": "AccountId",
            "minLength": 12,
            "maxLength": 12,
        }
    ),
]


class Region(StrEnum):
    US_EAST_1 = "us-east-1"
    US_EAST_2 = "us-east-2"
    US_WEST_1 = "us-west-1"
    US_WEST_2 = "us-west-2"
    AF_SOUTH_1 = "af-south-1"
    AP_EAST_1 = "ap-east-1"
    AP_SOUTH_1 = "ap-south-1"
    AP_SOUTH_2 = "ap-south-2"
    AP_SOUTHEAST_1 = "ap-southeast-1"
    AP_SOUTHEAST_2 = "ap-southeast-2"
    AP_SOUTHEAST_3 = "ap-southeast-3"
    AP_SOUTHEAST_4 = "ap-southeast-4"
    AP_NORTHEAST_1 = "ap-northeast-1"
    AP_NORTHEAST_2 = "ap-northeast-2"
    AP_NORTHEAST_3 = "ap-northeast-3"
    CA_CENTRAL_1 = "ca-central-1"
    CA_WEST_1 = "ca-west-1"
    EU_CENTRAL_1 = "eu-central-1"
    EU_CENTRAL_2 = "eu-central-2"
    EU_WEST_1 = "eu-west-1"
    EU_WEST_2 = "eu-west-2"
    EU_WEST_3 = "eu-west-3"
    EU_SOUTH_1 = "eu-south-1"
    EU_SOUTH_2 = "eu-south-2"
    EU_NORTH_1 = "eu-north-1"
    IL_CENTRAL_1 = "il-central-1"
    ME_SOUTH_1 = "me-south-1"
    ME_CENTRAL_1 = "me-central-1"
    SA_EAST_1 = "sa-east-1"
    US_GOV_EAST_1 = "us-gov-east-1"
    US_GOV_WEST_1 = "us-gov-west-1"
    CN_NORTH_1 = "cn-north-1"
    CN_NORTHWEST_1 = "cn-northwest-1"
