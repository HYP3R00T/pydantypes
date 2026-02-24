"""GCP security types."""

from __future__ import annotations

import re
from typing import Any, ClassVar

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError

from pydantypes._internal import _str_type_core_schema


# Source: https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets
class SecretManagerSecretName(str):
    """A validated GCP Secret Manager secret name (projects/{project}/secrets/{secret})."""

    _pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"^projects/([a-z][a-z0-9-]{4,28}[a-z0-9]|\d+)/secrets/([a-zA-Z0-9_-]{1,255})$"
    )
    project_id: str
    secret_id: str

    def __new__(cls, value: str) -> SecretManagerSecretName:
        """Create and validate a new SecretManagerSecretName instance."""
        m = cls._pattern.match(value)
        if not m:
            raise PydanticCustomError(
                "gcp_secret_manager_secret_name",
                "Invalid GCP Secret Manager secret name: {value}",
                {"value": value},
            )
        instance = str.__new__(cls, value)
        instance.project_id = m.group(1)
        instance.secret_id = m.group(2)
        return instance

    @classmethod
    def _validate(cls, value: str) -> SecretManagerSecretName:
        """Validate a string as a Secret Manager secret name."""
        return cls(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Return the Pydantic core schema for SecretManagerSecretName."""
        return _str_type_core_schema(cls, source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """Return the JSON schema for SecretManagerSecretName."""
        return {
            "type": "string",
            "format": "gcp-secret-manager-secret-name",
            "pattern": cls._pattern.pattern,
            "description": "A GCP Secret Manager secret name.",
            "examples": ["projects/my-project/secrets/my-secret"],
            "title": "SecretManagerSecretName",
        }


# Source: https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets
class SecretManagerVersionName(str):
    """A validated GCP Secret Manager version name."""

    _pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"^projects/([a-z][a-z0-9-]{4,28}[a-z0-9]|\d+)"
        r"/secrets/([a-zA-Z0-9_-]{1,255})"
        r"/versions/([a-zA-Z0-9_-]+|latest)$"
    )
    project_id: str
    secret_id: str
    version: str

    def __new__(cls, value: str) -> SecretManagerVersionName:
        """Create and validate a new SecretManagerVersionName instance."""
        m = cls._pattern.match(value)
        if not m:
            raise PydanticCustomError(
                "gcp_secret_manager_version_name",
                "Invalid GCP Secret Manager version name: {value}",
                {"value": value},
            )
        instance = str.__new__(cls, value)
        instance.project_id = m.group(1)
        instance.secret_id = m.group(2)
        instance.version = m.group(3)
        return instance

    @classmethod
    def _validate(cls, value: str) -> SecretManagerVersionName:
        """Validate a string as a Secret Manager version name."""
        return cls(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Return the Pydantic core schema for SecretManagerVersionName."""
        return _str_type_core_schema(cls, source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """Return the JSON schema for SecretManagerVersionName."""
        return {
            "type": "string",
            "format": "gcp-secret-manager-version-name",
            "pattern": cls._pattern.pattern,
            "description": "A GCP Secret Manager version name.",
            "examples": ["projects/my-project/secrets/my-secret/versions/1"],
            "title": "SecretManagerVersionName",
        }


# Source: https://cloud.google.com/kms/docs/resource-hierarchy
class KmsKeyName(str):
    """A validated GCP KMS key name."""

    _pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"^projects/([a-z][a-z0-9-]{4,28}[a-z0-9]|\d+)"
        r"/locations/([a-z][a-z0-9-]*)"
        r"/keyRings/([a-zA-Z0-9_-]+)"
        r"/cryptoKeys/([a-zA-Z0-9_-]+)$"
    )
    project_id: str
    location: str
    key_ring: str
    key_name: str

    def __new__(cls, value: str) -> KmsKeyName:
        """Create and validate a new KmsKeyName instance."""
        m = cls._pattern.match(value)
        if not m:
            raise PydanticCustomError(
                "gcp_kms_key_name",
                "Invalid GCP KMS key name: {value}",
                {"value": value},
            )
        instance = str.__new__(cls, value)
        instance.project_id = m.group(1)
        instance.location = m.group(2)
        instance.key_ring = m.group(3)
        instance.key_name = m.group(4)
        return instance

    @classmethod
    def _validate(cls, value: str) -> KmsKeyName:
        """Validate a string as a KMS key name."""
        return cls(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Return the Pydantic core schema for KmsKeyName."""
        return _str_type_core_schema(cls, source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """Return the JSON schema for KmsKeyName."""
        return {
            "type": "string",
            "format": "gcp-kms-key-name",
            "pattern": cls._pattern.pattern,
            "description": "A GCP KMS key name.",
            "examples": [
                "projects/my-project/locations/us-central1/keyRings/my-ring/cryptoKeys/my-key"
            ],
            "title": "KmsKeyName",
        }
