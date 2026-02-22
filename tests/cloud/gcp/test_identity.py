from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.gcp.identity import ProjectId, Region, ServiceAccountEmail, Zone


class ProjModel(BaseModel):
    project: ProjectId


class SAModel(BaseModel):
    email: ServiceAccountEmail


class ZoneModel(BaseModel):
    zone: Zone


@pytest.mark.parametrize("value", ["my-project-123", "abcdef"])
class TestProjectIdValid:
    def test_pydantic_accepts(self, value: str) -> None:
        m = ProjModel(project=value)
        assert m.project == value


@pytest.mark.parametrize("value", ["ab", "My-Project", "-starts", "ends-"])
class TestProjectIdInvalid:
    def test_pydantic_rejects(self, value: str) -> None:
        with pytest.raises(ValidationError):
            ProjModel(project=value)


class TestServiceAccountEmailValid:
    def test_basic(self) -> None:
        sa = ServiceAccountEmail("my-service-account@my-project.iam.gserviceaccount.com")
        assert sa.name == "my-service-account"
        assert sa.project_id == "my-project"

    def test_pydantic_model(self) -> None:
        m = SAModel(email="my-service-account@my-project.iam.gserviceaccount.com")
        assert isinstance(m.email, ServiceAccountEmail)


@pytest.mark.parametrize(
    "value",
    [
        "ab@my-project.iam.gserviceaccount.com",
        "my-service-account@my-project.iam.wrong.com",
        "my-service-account@my-project.com",
        "MY-SERVICE@my-project.iam.gserviceaccount.com",
    ],
)
class TestServiceAccountEmailInvalid:
    def test_pydantic_rejects(self, value: str) -> None:
        with pytest.raises(ValidationError):
            SAModel(email=value)


class TestRegion:
    def test_valid_member(self) -> None:
        assert Region.US_CENTRAL1 == "us-central1"
        assert Region.EUROPE_WEST1 == "europe-west1"

    def test_from_value(self) -> None:
        r = Region("us-central1")
        assert r is Region.US_CENTRAL1

    def test_invalid(self) -> None:
        with pytest.raises(ValueError):
            Region("invalid-region")


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
