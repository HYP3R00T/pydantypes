"""Tests for Azure region types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.azure.region import Region


class RegionModel(BaseModel):
    field: Region


def test_valid_region() -> None:
    m = RegionModel(field="eastus")
    assert m.field == Region.EASTUS


def test_invalid_region() -> None:
    with pytest.raises(ValidationError):
        RegionModel(field="invalid-region")


def test_region_enum_values() -> None:
    assert Region.WESTEUROPE == "westeurope"
    assert Region.JAPANEAST == "japaneast"


def test_new_regions() -> None:
    assert Region.NEWZEALANDNORTH == "newzealandnorth"
    assert Region.TAIWANNORTH == "taiwannorth"
