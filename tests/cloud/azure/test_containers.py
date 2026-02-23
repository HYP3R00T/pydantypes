"""Tests for Azure container types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.azure.containers import ContainerRegistryName


class ContainerRegistryModel(BaseModel):
    field: ContainerRegistryName


@pytest.mark.parametrize("value", ["mycontainerregistry", "abcde", "Registry123"])
def test_valid_container_registry_name(value: str) -> None:
    m = ContainerRegistryModel(field=value)
    assert m.field == value


@pytest.mark.parametrize("value", ["abcd", "my-registry", "a" * 51, ""])
def test_invalid_container_registry_name(value: str) -> None:
    with pytest.raises(ValidationError):
        ContainerRegistryModel(field=value)


def test_container_registry_name_serialization() -> None:
    m = ContainerRegistryModel(field="mycontainerregistry")
    assert m.model_dump()["field"] == "mycontainerregistry"
