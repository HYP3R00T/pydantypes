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

    Supports nested resources (e.g., servers/myserver/databases/mydb).

    Source: https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/resource-name-rules
    """

    _pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"^/subscriptions/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"
        r"/resourceGroups/([^/]+)/providers/([^/]+)((?:/[^/]+){2,})$",
        re.IGNORECASE,
    )

    subscription_id: str
    resource_group: str
    provider_namespace: str
    resource_type: str
    resource_name: str
    resource_path: str

    def __new__(cls, value: str) -> ResourceId:
        """Create and validate a new ResourceId instance."""
        m = cls._pattern.match(value)
        if not m:
            raise PydanticCustomError(
                "azure_resource_id",
                "Invalid Azure Resource ID: {value}",
                {"value": value},
            )
        path = m.group(4)
        segments = path.strip("/").split("/")
        if len(segments) % 2 != 0:
            raise PydanticCustomError(
                "azure_resource_id",
                "Invalid Azure Resource ID: malformed resource path in {value}",
                {"value": value},
            )
        instance = str.__new__(cls, value)
        instance.subscription_id = m.group(1)
        instance.resource_group = m.group(2)
        instance.provider_namespace = m.group(3)
        instance.resource_path = path
        instance.resource_type = segments[-2]
        instance.resource_name = segments[-1]
        return instance

    @classmethod
    def _validate(cls, value: str) -> ResourceId:
        """Validate a string as an Azure Resource ID."""
        return cls(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Return the Pydantic core schema for ResourceId."""
        return _str_type_core_schema(cls, source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """Return the JSON schema for ResourceId."""
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
