"""Azure Key Vault URI type."""

from __future__ import annotations

import re
from typing import Any, ClassVar

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError

from pydantypes._internal import _str_type_core_schema


class KeyVaultUri(str):
    """Azure Key Vault URI.

    Validates and parses a URI of the form:
    https://{vault_name}.vault.azure.net/
    """

    _pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"^https://([a-zA-Z][a-zA-Z0-9-]{1,22}[a-zA-Z0-9])\.vault\.azure\.net/?$"
    )

    vault_name: str

    def __new__(cls, value: str) -> KeyVaultUri:
        m = cls._pattern.match(value)
        if not m:
            raise PydanticCustomError(
                "azure_key_vault_uri",
                "Invalid Azure Key Vault URI: {value}",
                {"value": value},
            )
        instance = str.__new__(cls, value)
        instance.vault_name = m.group(1)
        return instance

    @classmethod
    def _validate(cls, value: str) -> KeyVaultUri:
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
            "format": "azure-key-vault-uri",
            "pattern": cls._pattern.pattern,
            "description": "Azure Key Vault URI.",
            "examples": ["https://my-vault.vault.azure.net/"],
            "title": "KeyVaultUri",
        }
