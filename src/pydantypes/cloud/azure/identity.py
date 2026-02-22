"""Azure identity types: SubscriptionId, TenantId, ResourceGroupName, Region."""

from __future__ import annotations

import re
import sys
from typing import Annotated

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from enum import Enum

    class StrEnum(str, Enum):
        pass


from pydantic import AfterValidator, WithJsonSchema
from pydantic_core import PydanticCustomError

_UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)

_RESOURCE_GROUP_PATTERN = re.compile(r"^[a-zA-Z0-9_\-.()]{1,90}$")


# --- SubscriptionId ---


def _validate_subscription_id(v: str) -> str:
    if not _UUID_PATTERN.match(v):
        raise PydanticCustomError(
            "azure_subscription_id",
            "Invalid Azure Subscription ID: {value}",
            {"value": v},
        )
    return v.lower()


SubscriptionId = Annotated[
    str,
    AfterValidator(_validate_subscription_id),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            "description": "Azure Subscription ID (UUID).",
            "examples": ["12345678-1234-1234-1234-123456789012"],
            "title": "SubscriptionId",
        }
    ),
]


# --- TenantId ---


def _validate_tenant_id(v: str) -> str:
    if not _UUID_PATTERN.match(v):
        raise PydanticCustomError(
            "azure_tenant_id",
            "Invalid Azure Tenant ID: {value}",
            {"value": v},
        )
    return v.lower()


TenantId = Annotated[
    str,
    AfterValidator(_validate_tenant_id),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            "description": "Azure Tenant ID (UUID).",
            "examples": ["12345678-1234-1234-1234-123456789012"],
            "title": "TenantId",
        }
    ),
]


# --- ResourceGroupName ---


def _validate_resource_group_name(v: str) -> str:
    if not _RESOURCE_GROUP_PATTERN.match(v) or v.endswith("."):
        raise PydanticCustomError(
            "azure_resource_group_name",
            "Invalid Azure Resource Group name: {value}",
            {"value": v},
        )
    return v


ResourceGroupName = Annotated[
    str,
    AfterValidator(_validate_resource_group_name),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": r"^[a-zA-Z0-9_\-.()]{1,90}$",
            "description": "Azure Resource Group name.",
            "examples": ["my-resource-group"],
            "title": "ResourceGroupName",
        }
    ),
]


# --- Region ---


class Region(StrEnum):
    """Azure region identifiers."""

    # US
    EASTUS = "eastus"
    EASTUS2 = "eastus2"
    WESTUS = "westus"
    WESTUS2 = "westus2"
    WESTUS3 = "westus3"
    CENTRALUS = "centralus"
    NORTHCENTRALUS = "northcentralus"
    SOUTHCENTRALUS = "southcentralus"
    WESTCENTRALUS = "westcentralus"

    # Canada
    CANADACENTRAL = "canadacentral"
    CANADAEAST = "canadaeast"

    # Brazil
    BRAZILSOUTH = "brazilsouth"
    BRAZILSOUTHEAST = "brazilsoutheast"

    # Europe
    NORTHEUROPE = "northeurope"
    WESTEUROPE = "westeurope"
    UKSOUTH = "uksouth"
    UKWEST = "ukwest"
    FRANCECENTRAL = "francecentral"
    FRANCESOUTH = "francesouth"
    GERMANYWESTCENTRAL = "germanywestcentral"
    GERMANYNORTH = "germanynorth"
    SWITZERLANDNORTH = "switzerlandnorth"
    SWITZERLANDWEST = "switzerlandwest"
    NORWAYEAST = "norwayeast"
    NORWAYWEST = "norwaywest"
    SWEDENCENTRAL = "swedencentral"

    # Asia Pacific
    EASTASIA = "eastasia"
    SOUTHEASTASIA = "southeastasia"
    JAPANEAST = "japaneast"
    JAPANWEST = "japanwest"
    AUSTRALIAEAST = "australiaeast"
    AUSTRALIASOUTHEAST = "australiasoutheast"
    AUSTRALIACENTRAL = "australiacentral"

    # India
    CENTRALINDIA = "centralindia"
    SOUTHINDIA = "southindia"
    WESTINDIA = "westindia"

    # Korea
    KOREACENTRAL = "koreacentral"
    KOREASOUTH = "koreasouth"

    # Middle East and Africa
    UAENORTH = "uaenorth"
    UAECENTRAL = "uaecentral"
    SOUTHAFRICANORTH = "southafricanorth"
    SOUTHAFRICAWEST = "southafricawest"

    # Other
    QATARCENTRAL = "qatarcentral"
    ISRAELCENTRAL = "israelcentral"
    ITALYNORTH = "italynorth"
    POLANDCENTRAL = "polandcentral"
    SPAINCENTRAL = "spaincentral"
    MEXICOCENTRAL = "mexicocentral"

    # US Government
    USGOVVIRGINIA = "usgovvirginia"
    USGOVARIZONA = "usgovarizona"
    USGOVIOWA = "usgoviowa"
    USGOVTEXAS = "usgovtexas"

    # China
    CHINAEAST = "chinaeast"
    CHINAEAST2 = "chinaeast2"
    CHINANORTH = "chinanorth"
    CHINANORTH2 = "chinanorth2"
