"""Azure Resource ID type."""

from __future__ import annotations

import re
from typing import Any, ClassVar

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError

from pydantypes._internal import _str_type_core_schema


class ResourceId(str):
    """Azure Resource ID.

    Validates and parses a fully-qualified Azure resource identifier of the form:
    /subscriptions/{sub}/resourceGroups/{rg}/providers/{ns}/{type}/{name}
    """

    _pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"^/subscriptions/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"
        r"/resourceGroups/([^/]+)/providers/([^/]+)/([^/]+)/([^/]+)$",
        re.IGNORECASE,
    )

    subscription_id: str
    resource_group: str
    provider_namespace: str
    resource_type: str
    resource_name: str

    def __new__(cls, value: str) -> ResourceId:
        m = cls._pattern.match(value)
        if not m:
            raise PydanticCustomError(
                "azure_resource_id",
                "Invalid Azure Resource ID: {value}",
                {"value": value},
            )
        instance = str.__new__(cls, value)
        instance.subscription_id = m.group(1)
        instance.resource_group = m.group(2)
        instance.provider_namespace = m.group(3)
        instance.resource_type = m.group(4)
        instance.resource_name = m.group(5)
        return instance

    @classmethod
    def _validate(cls, value: str) -> ResourceId:
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
            "format": "azure-resource-id",
            "pattern": cls._pattern.pattern,
            "description": "Azure Resource ID.",
            "examples": [
                "/subscriptions/12345678-1234-1234-1234-123456789012"
                "/resourceGroups/myRG/providers/Microsoft.Compute/virtualMachines/myVM"
            ],
            "title": "ResourceId",
        }
