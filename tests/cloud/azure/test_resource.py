"""Tests for Azure resource types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.azure.resource import ResourceId

VALID_RID = (
    "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myR"
    "G/providers/Microsoft.Compute/virtualMachines/myVM"
)
VALID_RID2 = (
    "/subscriptions/abcdef01-2345-6789-abcd-ef0123456789/resourceGroups/tes"
    "t-rg/providers/Microsoft.Storage/storageAccounts/myacct"
)
VALID_NESTED_RID = (
    "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myR"
    "G/providers/Microsoft.Sql/servers/myserver/databases/mydb"
)


class ResourceIdModel(BaseModel):
    field: ResourceId


@pytest.mark.parametrize(
    "value",
    [
        VALID_RID,
        VALID_RID2,
        VALID_NESTED_RID,
    ],
)
def test_valid_resource_id(value: str) -> None:
    m = ResourceIdModel(field=value)
    assert str(m.field) == value


@pytest.mark.parametrize(
    "value",
    [
        "not-a-resource-id",
        "/subscriptions/invalid-uuid/resourceGroups/rg/providers/Ms/type/name",
        "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg",
    ],
)
def test_invalid_resource_id(value: str) -> None:
    with pytest.raises(ValidationError):
        ResourceIdModel(field=value)


def test_resource_id_properties() -> None:
    m = ResourceIdModel(field=VALID_RID)
    assert m.field.subscription_id == "12345678-1234-1234-1234-123456789012"
    assert m.field.resource_group == "myRG"
    assert m.field.provider_namespace == "Microsoft.Compute"
    assert m.field.resource_type == "virtualMachines"
    assert m.field.resource_name == "myVM"
    assert m.field.resource_path == "/virtualMachines/myVM"


def test_nested_resource_id_properties() -> None:
    m = ResourceIdModel(field=VALID_NESTED_RID)
    assert m.field.provider_namespace == "Microsoft.Sql"
    assert m.field.resource_type == "databases"
    assert m.field.resource_name == "mydb"
    assert m.field.resource_path == "/servers/myserver/databases/mydb"


def test_resource_id_serialization() -> None:
    m = ResourceIdModel(field=VALID_RID)
    data = m.model_dump()
    assert data["field"] == VALID_RID


def test_resource_id_json_schema() -> None:
    schema = ResourceIdModel.model_json_schema()
    props = schema["properties"]["field"]
    assert props["type"] == "string"
    assert props["format"] == "azure-resource-id"


def test_resource_id_existing_instance() -> None:
    rid = ResourceId(VALID_RID)
    m = ResourceIdModel(field=rid)
    assert m.field is rid
