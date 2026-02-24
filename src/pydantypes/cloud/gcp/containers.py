"""GCP container types."""

from __future__ import annotations

import re
from typing import Any, ClassVar

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError

from pydantypes._internal import _str_type_core_schema


# Source: https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling
class ArtifactRegistryImageUri(str):
    """A validated GCP Artifact Registry image URI."""

    _pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"^([a-z][a-z0-9-]*)-docker\.pkg\.dev"
        r"/([a-z][a-z0-9-]{4,28}[a-z0-9]|\d+)"
        r"/([a-z][a-z0-9._-]*)"
        r"/([a-z0-9][a-z0-9._/-]*)"
        r"(?::([a-zA-Z0-9._-]+))?"
        r"(?:@(sha256:[a-f0-9]{64}))?$"
    )

    location: str
    project_id: str
    repository: str
    image: str
    tag: str
    digest: str

    def __new__(cls, value: str) -> ArtifactRegistryImageUri:
        """Create and validate a new ArtifactRegistryImageUri instance."""
        m = cls._pattern.match(value)
        if not m:
            raise PydanticCustomError(
                "gcp_artifact_registry_image_uri",
                "Invalid GCP Artifact Registry image URI: {value}",
                {"value": value},
            )
        instance = str.__new__(cls, value)
        instance.location = m.group(1)
        instance.project_id = m.group(2)
        instance.repository = m.group(3)
        instance.image = m.group(4)
        instance.tag = m.group(5) or ""
        instance.digest = m.group(6) or ""
        return instance

    @classmethod
    def _validate(cls, value: str) -> ArtifactRegistryImageUri:
        """Validate a string as an Artifact Registry image URI."""
        return cls(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Return the Pydantic core schema for ArtifactRegistryImageUri."""
        return _str_type_core_schema(cls, source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """Return the JSON schema for ArtifactRegistryImageUri."""
        return {
            "type": "string",
            "format": "gcp-artifact-registry-image-uri",
            "pattern": cls._pattern.pattern,
            "description": "A GCP Artifact Registry image URI.",
            "examples": ["us-docker.pkg.dev/my-project/my-repo/my-image:latest"],
            "title": "ArtifactRegistryImageUri",
        }
