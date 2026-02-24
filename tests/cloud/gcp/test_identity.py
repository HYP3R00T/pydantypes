"""Tests for GCP identity types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.gcp.identity import (
    BillingAccountId,
    OrganizationId,
    ProjectId,
    ProjectNumber,
    ServiceAccountEmail,
)


class ProjModel(BaseModel):
    project: ProjectId


class ProjNumModel(BaseModel):
    number: ProjectNumber


class BillingModel(BaseModel):
    account: BillingAccountId


class OrgModel(BaseModel):
    org: OrganizationId


class SAModel(BaseModel):
    email: ServiceAccountEmail


@pytest.mark.parametrize("value", ["my-project-123", "abcdef"])
class TestProjectIdValid:
    def test_pydantic_accepts(self, value: str) -> None:
        m = ProjModel(project=value)
        assert m.project == value


@pytest.mark.parametrize("value", ["ab", "My-Project", "-starts", "ends-", "google", "undefined"])
class TestProjectIdInvalid:
    def test_pydantic_rejects(self, value: str) -> None:
        with pytest.raises(ValidationError):
            ProjModel(project=value)


def test_project_id_serialization() -> None:
    m = ProjModel(project="my-project-123")
    assert m.model_dump()["project"] == "my-project-123"


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


def test_service_account_email_serialization() -> None:
    m = SAModel(email="my-service-account@my-project.iam.gserviceaccount.com")
    assert m.model_dump()["email"] == "my-service-account@my-project.iam.gserviceaccount.com"


def test_service_account_email_json_schema() -> None:
    schema = SAModel.model_json_schema()
    props = schema["properties"]["email"]
    assert props["type"] == "string"
    assert props["format"] == "gcp-service-account-email"


def test_service_account_email_existing_instance() -> None:
    sa = ServiceAccountEmail("my-service-account@my-project.iam.gserviceaccount.com")
    m = SAModel(email=sa)
    assert m.email is sa


@pytest.mark.parametrize("value", ["123456789012", "10", "999999"])
def test_valid_project_number(value: str) -> None:
    m = ProjNumModel(number=value)
    assert m.number == value


@pytest.mark.parametrize("value", ["0", "01234", "", "abc"])
def test_invalid_project_number(value: str) -> None:
    with pytest.raises(ValidationError):
        ProjNumModel(number=value)


def test_project_number_serialization() -> None:
    m = ProjNumModel(number="123456789012")
    assert m.model_dump()["number"] == "123456789012"


@pytest.mark.parametrize("value", ["01A2B3-C4D5E6-F7G8H9", "AAAAAA-BBBBBB-CCCCCC"])
def test_valid_billing_account_id(value: str) -> None:
    m = BillingModel(account=value)
    assert m.account == value


@pytest.mark.parametrize("value", ["01a2b3-c4d5e6-f7g8h9", "AAAAAA-BBBBBB", "12345", ""])
def test_invalid_billing_account_id(value: str) -> None:
    with pytest.raises(ValidationError):
        BillingModel(account=value)


def test_billing_account_id_serialization() -> None:
    m = BillingModel(account="01A2B3-C4D5E6-F7G8H9")
    assert m.model_dump()["account"] == "01A2B3-C4D5E6-F7G8H9"


@pytest.mark.parametrize("value", ["1", "123456789012", "999"])
def test_valid_organization_id(value: str) -> None:
    m = OrgModel(org=value)
    assert m.org == value


@pytest.mark.parametrize("value", ["0", "01234", "", "abc"])
def test_invalid_organization_id(value: str) -> None:
    with pytest.raises(ValidationError):
        OrgModel(org=value)


def test_organization_id_serialization() -> None:
    m = OrgModel(org="123456789012")
    assert m.model_dump()["org"] == "123456789012"
