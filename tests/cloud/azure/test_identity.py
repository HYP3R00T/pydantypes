"""Tests for identity."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.azure.identity import (
    Region,
    ResourceGroupName,
    SubscriptionId,
    TenantId,
)


class SubscriptionIdModel(BaseModel):
    field: SubscriptionId


class TenantIdModel(BaseModel):
    field: TenantId


class ResourceGroupNameModel(BaseModel):
    field: ResourceGroupName


class RegionModel(BaseModel):
    field: Region


# --- SubscriptionId tests ---


def test_valid_subscription_id() -> None:
    m = SubscriptionIdModel(field="12345678-1234-1234-1234-123456789012")
    assert m.field == "12345678-1234-1234-1234-123456789012"


def test_subscription_id_case_normalization() -> None:
    m = SubscriptionIdModel(field="ABCDEF01-2345-6789-ABCD-EF0123456789")
    assert m.field == "abcdef01-2345-6789-abcd-ef0123456789"


@pytest.mark.parametrize("value", ["not-a-uuid", "12345", ""])
def test_invalid_subscription_id(value: str) -> None:
    with pytest.raises(ValidationError):
        SubscriptionIdModel(field=value)


def test_subscription_id_serialization() -> None:
    m = SubscriptionIdModel(field="12345678-1234-1234-1234-123456789012")
    assert m.model_dump()["field"] == "12345678-1234-1234-1234-123456789012"


def test_subscription_id_json_schema() -> None:
    schema = SubscriptionIdModel.model_json_schema()
    props = schema["properties"]["field"]
    assert props["type"] == "string"


# --- TenantId tests ---


def test_valid_tenant_id() -> None:
    m = TenantIdModel(field="12345678-1234-1234-1234-123456789012")
    assert m.field == "12345678-1234-1234-1234-123456789012"


def test_tenant_id_case_normalization() -> None:
    m = TenantIdModel(field="ABCDEF01-2345-6789-ABCD-EF0123456789")
    assert m.field == "abcdef01-2345-6789-abcd-ef0123456789"


@pytest.mark.parametrize("value", ["not-a-uuid", "xyz"])
def test_invalid_tenant_id(value: str) -> None:
    with pytest.raises(ValidationError):
        TenantIdModel(field=value)


def test_tenant_id_serialization() -> None:
    m = TenantIdModel(field="12345678-1234-1234-1234-123456789012")
    assert m.model_dump()["field"] == "12345678-1234-1234-1234-123456789012"


# --- ResourceGroupName tests ---


@pytest.mark.parametrize("value", ["my-resource-group", "rg1", "my_rg(1)"])
def test_valid_resource_group_name(value: str) -> None:
    m = ResourceGroupNameModel(field=value)
    assert m.field == value


@pytest.mark.parametrize(
    "value",
    [
        "name.",
        "",
        "a\tb",
        "a" * 91,
    ],
)
def test_invalid_resource_group_name(value: str) -> None:
    with pytest.raises(ValidationError):
        ResourceGroupNameModel(field=value)


def test_resource_group_name_serialization() -> None:
    m = ResourceGroupNameModel(field="my-rg")
    assert m.model_dump()["field"] == "my-rg"


# --- Region tests ---


def test_valid_region() -> None:
    m = RegionModel(field="eastus")
    assert m.field == Region.EASTUS


def test_invalid_region() -> None:
    with pytest.raises(ValidationError):
        RegionModel(field="invalid-region")


def test_region_enum_values() -> None:
    assert Region.WESTEUROPE == "westeurope"
    assert Region.JAPANEAST == "japaneast"
