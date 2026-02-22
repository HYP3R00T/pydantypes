from __future__ import annotations

import re
from typing import Any, ClassVar

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError

from pydantypes._internal import _str_type_core_schema


class GcsUri(str):
    """A validated Google Cloud Storage URI (gs://bucket/path)."""

    _pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"^gs://([a-z0-9][a-z0-9._-]{1,61}[a-z0-9])(?:/(.*))?$"
    )
    bucket: str
    path: str

    def __new__(cls, value: str) -> GcsUri:
        m = cls._pattern.match(value)
        if not m:
            raise PydanticCustomError("gcs_uri", "Invalid GCS URI: {value}", {"value": value})
        instance = str.__new__(cls, value)
        instance.bucket = m.group(1)
        instance.path = m.group(2) or ""
        return instance

    @classmethod
    def _validate(cls, value: str) -> GcsUri:
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
            "format": "gcs-uri",
            "pattern": cls._pattern.pattern,
            "description": "A Google Cloud Storage URI (gs://bucket/path).",
            "examples": ["gs://my-bucket/path/to/file.csv"],
            "title": "GcsUri",
        }
