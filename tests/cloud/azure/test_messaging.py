"""Tests for messaging."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.azure.messaging import ServiceBusNamespace


class ServiceBusNamespaceModel(BaseModel):
    field: ServiceBusNamespace


@pytest.mark.parametrize("value", ["myservicebus123", "abcdef", "my-servicebus-ns"])
def test_valid_service_bus_namespace(value: str) -> None:
    m = ServiceBusNamespaceModel(field=value)
    assert m.field == value


@pytest.mark.parametrize("value", ["abcde", "1start", "a--bad-ns", "abcde-"])
def test_invalid_service_bus_namespace(value: str) -> None:
    with pytest.raises(ValidationError):
        ServiceBusNamespaceModel(field=value)


def test_service_bus_namespace_serialization() -> None:
    m = ServiceBusNamespaceModel(field="myservicebus123")
    assert m.model_dump()["field"] == "myservicebus123"


def test_service_bus_namespace_json_schema() -> None:
    schema = ServiceBusNamespaceModel.model_json_schema()
    props = schema["properties"]["field"]
    assert props["type"] == "string"
