"""GCP identity types."""

from __future__ import annotations

import re
import sys
from typing import Annotated, Any, ClassVar

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from enum import Enum

    class StrEnum(str, Enum):
        pass


from pydantic import AfterValidator, GetCoreSchemaHandler, GetJsonSchemaHandler, WithJsonSchema
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError

from pydantypes._internal import _str_type_core_schema

_PROJECT_ID_RE = re.compile(r"^[a-z][a-z0-9-]{4,28}[a-z0-9]$")
_PROJECT_NUMBER_RE = re.compile(r"^[1-9]\d+$")
_BILLING_ACCOUNT_ID_RE = re.compile(r"^[A-Z0-9]{6}-[A-Z0-9]{6}-[A-Z0-9]{6}$")
_ORGANIZATION_ID_RE = re.compile(r"^[1-9]\d*$")

_RESERVED_PROJECT_IDS = frozenset({"google", "undefined", "null", "ssl"})


def _validate_project_id(v: str) -> str:
    """Validate a GCP project ID format."""
    if not _PROJECT_ID_RE.match(v):
        raise PydanticCustomError(
            "gcp_project_id",
            "Invalid GCP project ID: {value}",
            {"value": v},
        )
    if v in _RESERVED_PROJECT_IDS:
        raise PydanticCustomError(
            "gcp_project_id",
            "Invalid GCP project ID: '{value}' is a reserved word",
            {"value": v},
        )
    return v


def _validate_project_number(v: str) -> str:
    """Validate a GCP project number format."""
    if not _PROJECT_NUMBER_RE.match(v):
        raise PydanticCustomError(
            "gcp_project_number",
            "Invalid GCP project number: {value}",
            {"value": v},
        )
    return v


def _validate_billing_account_id(v: str) -> str:
    """Validate a GCP billing account ID format."""
    if not _BILLING_ACCOUNT_ID_RE.match(v):
        raise PydanticCustomError(
            "gcp_billing_account_id",
            "Invalid GCP billing account ID: {value}",
            {"value": v},
        )
    return v


def _validate_organization_id(v: str) -> str:
    """Validate a GCP organization ID format."""
    if not _ORGANIZATION_ID_RE.match(v):
        raise PydanticCustomError(
            "gcp_organization_id",
            "Invalid GCP organization ID: {value}",
            {"value": v},
        )
    return v


# Source: https://cloud.google.com/resource-manager/docs/creating-managing-projects
ProjectId = Annotated[
    str,
    AfterValidator(_validate_project_id),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": _PROJECT_ID_RE.pattern,
            "description": "A GCP project ID (6-30 lowercase chars).",
            "examples": ["my-project-123"],
            "title": "ProjectId",
        }
    ),
]

# Source: https://cloud.google.com/resource-manager/docs/creating-managing-projects
ProjectNumber = Annotated[
    str,
    AfterValidator(_validate_project_number),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": _PROJECT_NUMBER_RE.pattern,
            "description": "A GCP project number.",
            "examples": ["123456789012"],
            "title": "ProjectNumber",
        }
    ),
]

# Source: https://cloud.google.com/billing/docs/how-to/find-billing-account-id
BillingAccountId = Annotated[
    str,
    AfterValidator(_validate_billing_account_id),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": _BILLING_ACCOUNT_ID_RE.pattern,
            "description": "A GCP billing account ID.",
            "examples": ["01A2B3-C4D5E6-F7G8H9"],
            "title": "BillingAccountId",
        }
    ),
]

# Source: https://cloud.google.com/resource-manager/docs/creating-managing-organization
OrganizationId = Annotated[
    str,
    AfterValidator(_validate_organization_id),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": _ORGANIZATION_ID_RE.pattern,
            "description": "A GCP organization ID.",
            "examples": ["123456789012"],
            "title": "OrganizationId",
        }
    ),
]


class ServiceAccountEmail(str):
    """A validated GCP service account email.

    Source: https://cloud.google.com/iam/docs/service-accounts-create
    """

    _pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"^([a-z][a-z0-9-]{4,28}[a-z0-9])@([a-z][a-z0-9-]{4,28}[a-z0-9])\.iam\.gserviceaccount\.com$"
    )
    name: str
    project_id: str

    def __new__(cls, value: str) -> ServiceAccountEmail:
        """Create and validate a new ServiceAccountEmail instance."""
        m = cls._pattern.match(value)
        if not m:
            raise PydanticCustomError(
                "gcp_service_account_email",
                "Invalid GCP service account email: {value}",
                {"value": value},
            )
        instance = str.__new__(cls, value)
        instance.name = m.group(1)
        instance.project_id = m.group(2)
        return instance

    @classmethod
    def _validate(cls, value: str) -> ServiceAccountEmail:
        """Validate a string as a service account email."""
        return cls(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Return the Pydantic core schema for ServiceAccountEmail."""
        return _str_type_core_schema(cls, source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """Return the JSON schema for ServiceAccountEmail."""
        return {
            "type": "string",
            "format": "gcp-service-account-email",
            "pattern": cls._pattern.pattern,
            "description": "A GCP service account email.",
            "examples": ["my-service-account@my-project.iam.gserviceaccount.com"],
            "title": "ServiceAccountEmail",
        }


class Region(StrEnum):
    """GCP cloud regions.

    Source: https://cloud.google.com/compute/docs/regions-zones
    """

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


class Zone(str):
    """A validated GCP zone (e.g. us-central1-a).

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
