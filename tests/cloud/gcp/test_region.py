"""Tests for GCP region and zone types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.gcp.region import Region, Zone


class ZoneModel(BaseModel):
    zone: Zone


class TestRegion:
    def test_valid_member(self) -> None:
        assert Region.US_CENTRAL1 == "us-central1"
        assert Region.EUROPE_WEST1 == "europe-west1"

    def test_from_value(self) -> None:
        r = Region("us-central1")
        assert r is Region.US_CENTRAL1

    def test_invalid(self) -> None:
        with pytest.raises(ValueError, match="invalid-region"):
            Region("invalid-region")

    def test_africa_south1(self) -> None:
        assert Region.AFRICA_SOUTH1 == "africa-south1"


@pytest.mark.parametrize("value", ["us-central1-a", "europe-west1-b"])
class TestZoneValid:
    def test_pydantic_accepts(self, value: str) -> None:
        m = ZoneModel(zone=value)
        assert isinstance(m.zone, Zone)

    def test_properties(self, value: str) -> None:
        z = Zone(value)
        assert z.zone_letter in "abcdefghij"
        assert len(z.region) > 0


@pytest.mark.parametrize(
    "value",
    [
        "us-central1",
        "invalid-region1-a",
        "us-central1-1",
    ],
)
class TestZoneInvalid:
    def test_pydantic_rejects(self, value: str) -> None:
        with pytest.raises(ValidationError):
            ZoneModel(zone=value)


def test_zone_serialization() -> None:
    m = ZoneModel(zone="us-central1-a")
    assert m.model_dump()["zone"] == "us-central1-a"
