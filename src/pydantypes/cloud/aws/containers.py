"""AWS container types."""

from __future__ import annotations

import re
from typing import Any, ClassVar

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError

from pydantypes._internal import _str_type_core_schema


# Source: https://docs.aws.amazon.com/AmazonECR/latest/userguide/Repositories.html
class EcrRepositoryUri(str):
    """An AWS ECR repository URI with parsed components."""

    _pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"^(\d{12})\.dkr\.ecr\.([a-z0-9-]+)\.amazonaws\.com/([a-z0-9][a-z0-9._/-]{0,255})$"
    )

    account_id: str
    region: str
    repository_name: str

    def __new__(cls, value: str) -> EcrRepositoryUri:
        """Create and validate a new EcrRepositoryUri instance."""
        m = cls._pattern.match(value)
        if not m:
            raise PydanticCustomError(
                "ecr_repository_uri",
                "Invalid ECR Repository URI: {value}",
                {"value": value},
            )
        instance = str.__new__(cls, value)
        instance.account_id = m.group(1)
        instance.region = m.group(2)
        instance.repository_name = m.group(3)
        return instance

    @classmethod
    def _validate(cls, value: str) -> EcrRepositoryUri:
        """Validate a string as an ECR Repository URI."""
        return cls(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Return the Pydantic core schema for EcrRepositoryUri."""
        return _str_type_core_schema(cls, source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """Return the JSON schema for EcrRepositoryUri."""
        return {
            "type": "string",
            "format": "aws-ecr-repository-uri",
            "pattern": cls._pattern.pattern,
            "description": "An AWS ECR repository URI",
            "examples": ["123456789012.dkr.ecr.us-east-1.amazonaws.com/my-repo"],
            "title": "EcrRepositoryUri",
        }
