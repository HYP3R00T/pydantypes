"""GCP region and zone types."""

from __future__ import annotations

import re
from typing import Any, ClassVar

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError

from pydantypes._internal import StrEnum, _str_type_core_schema


# Source: https://cloud.google.com/compute/docs/regions-zones
class Region(StrEnum):
    """GCP cloud regions."""

    US_CENTRAL1 = "us-central1"
    US_EAST1 = "us-east1"
    US_EAST4 = "us-east4"
    US_EAST5 = "us-east5"
    US_SOUTH1 = "us-south1"
    US_WEST1 = "us-west1"
    US_WEST2 = "us-west2"
    US_WEST3 = "us-west3"
    US_WEST4 = "us-west4"
    NORTHAMERICA_NORTHEAST1 = "northamerica-northeast1"
    NORTHAMERICA_NORTHEAST2 = "northamerica-northeast2"
    SOUTHAMERICA_EAST1 = "southamerica-east1"
    SOUTHAMERICA_WEST1 = "southamerica-west1"
    EUROPE_CENTRAL2 = "europe-central2"
    EUROPE_NORTH1 = "europe-north1"
    EUROPE_SOUTHWEST1 = "europe-southwest1"
    EUROPE_WEST1 = "europe-west1"
    EUROPE_WEST2 = "europe-west2"
    EUROPE_WEST3 = "europe-west3"
    EUROPE_WEST4 = "europe-west4"
    EUROPE_WEST6 = "europe-west6"
    EUROPE_WEST8 = "europe-west8"
    EUROPE_WEST9 = "europe-west9"
    EUROPE_WEST10 = "europe-west10"
    EUROPE_WEST12 = "europe-west12"
    ASIA_EAST1 = "asia-east1"
    ASIA_EAST2 = "asia-east2"
    ASIA_NORTHEAST1 = "asia-northeast1"
    ASIA_NORTHEAST2 = "asia-northeast2"
    ASIA_NORTHEAST3 = "asia-northeast3"
    ASIA_SOUTH1 = "asia-south1"
    ASIA_SOUTH2 = "asia-south2"
    ASIA_SOUTHEAST1 = "asia-southeast1"
    ASIA_SOUTHEAST2 = "asia-southeast2"
    AUSTRALIA_SOUTHEAST1 = "australia-southeast1"
    AUSTRALIA_SOUTHEAST2 = "australia-southeast2"
    ME_CENTRAL1 = "me-central1"
    ME_CENTRAL2 = "me-central2"
    ME_WEST1 = "me-west1"
    AFRICA_SOUTH1 = "africa-south1"


# Source: https://cloud.google.com/compute/docs/regions-zones
class Zone(str):
    """A validated GCP zone (e.g. us-central1-a).

    GCP zones use globally consistent names ({region}-{letter}), unlike AWS and
    Azure where zone names are randomly mapped per account/subscription. This
    makes GCP zones the only cloud provider zones worth validating as a type
    with parsed properties (.region, .zone_letter).

    Source: https://cloud.google.com/compute/docs/regions-zones
    """

    _pattern: ClassVar[re.Pattern[str]] = re.compile(r"^([a-z]+-[a-z]+\d+(?:-[a-z]+\d+)?)-([a-z])$")
    region: str
    zone_letter: str

    def __new__(cls, value: str) -> Zone:
        """Create and validate a new Zone instance."""
        m = cls._pattern.match(value)
        if not m:
            raise PydanticCustomError("gcp_zone", "Invalid GCP Zone: {value}", {"value": value})
        region_str = m.group(1)
        try:
            Region(region_str)
        except ValueError:
            raise PydanticCustomError(
                "gcp_zone",
                "Invalid GCP Zone: unknown region '{region}' in {value}",
                {"region": region_str, "value": value},
            ) from None
        instance = str.__new__(cls, value)
        instance.region = region_str
        instance.zone_letter = m.group(2)
        return instance

    @classmethod
    def _validate(cls, value: str) -> Zone:
        """Validate a string as a GCP Zone."""
        return cls(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Return the Pydantic core schema for Zone."""
        return _str_type_core_schema(cls, source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """Return the JSON schema for Zone."""
        return {
            "type": "string",
            "format": "gcp-zone",
            "pattern": cls._pattern.pattern,
            "description": "A GCP zone (e.g. us-central1-a).",
            "examples": ["us-central1-a"],
            "title": "Zone",
        }
