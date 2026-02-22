"""Azure Blob Storage URI type."""

from __future__ import annotations

import re
from typing import Any, ClassVar

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError

from pydantypes._internal import _str_type_core_schema


class BlobStorageUri(str):
    """Azure Blob Storage URI.

    Validates and parses a URI of the form:
    https://{account}.blob.core.windows.net/{container}[/{blob_path}]
    """

    _pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"^https://([a-z0-9]{3,24})\.blob\.core\.windows\.net"
        r"/([a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)(?:/(.+))?$"
    )

    account_name: str
    container: str
    blob_path: str

    def __new__(cls, value: str) -> BlobStorageUri:
        m = cls._pattern.match(value)
        if not m:
            raise PydanticCustomError(
                "azure_blob_storage_uri",
                "Invalid Azure Blob Storage URI: {value}",
                {"value": value},
            )
        instance = str.__new__(cls, value)
        instance.account_name = m.group(1)
        instance.container = m.group(2)
        instance.blob_path = m.group(3) or ""
        return instance

    @classmethod
    def _validate(cls, value: str) -> BlobStorageUri:
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
            "format": "azure-blob-storage-uri",
            "pattern": cls._pattern.pattern,
            "description": "Azure Blob Storage URI.",
            "examples": ["https://myaccount.blob.core.windows.net/mycontainer/path/to/blob"],
            "title": "BlobStorageUri",
        }
