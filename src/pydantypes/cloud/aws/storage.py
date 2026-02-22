"""AWS S3 storage types."""

from __future__ import annotations

import re
from typing import Any, ClassVar

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError

from pydantypes._internal import _str_type_core_schema


class S3Uri(str):
    """An S3 URI like s3://bucket/key with parsed properties."""

    _pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"^s3://([a-z0-9][a-z0-9.\-]{1,61}[a-z0-9])(/(.*))?$"
    )

    bucket: str
    key: str

    def __new__(cls, value: str) -> S3Uri:
        m = cls._pattern.match(value)
        if not m:
            raise PydanticCustomError(
                "s3_uri",
                "Invalid S3 URI: {value}",
                {"value": value},
            )
        instance = str.__new__(cls, value)
        instance.bucket = m.group(1)
        instance.key = m.group(3) or ""
        return instance

    @classmethod
    def _validate(cls, value: str) -> S3Uri:
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
            "format": "s3-uri",
            "pattern": cls._pattern.pattern,
            "description": "An S3 URI in the format s3://bucket/key",
            "examples": ["s3://my-bucket/path/to/file.csv"],
            "title": "S3Uri",
        }
