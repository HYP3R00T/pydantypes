"""Tests for GCP compute types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.gcp.compute import CloudFunctionName, CloudRunServiceName, ComputeResourceName


class CRModel(BaseModel):
    name: CloudRunServiceName


class ComputeModel(BaseModel):
    name: ComputeResourceName


class CFModel(BaseModel):
    name: CloudFunctionName


@pytest.mark.parametrize("value", ["my-service", "a", "a-long-service-name"])
class TestCloudRunServiceNameValid:
    def test_pydantic_accepts(self, value: str) -> None:
        m = CRModel(name=value)
        assert m.name == value


@pytest.mark.parametrize(
    "value",
    [
        "",
        "1starts",
        "-starts",
        "ends-",
        "a" * 50,
        "MyService",
    ],
)
class TestCloudRunServiceNameInvalid:
    def test_pydantic_rejects(self, value: str) -> None:
        with pytest.raises(ValidationError):
            CRModel(name=value)


def test_cloud_run_service_name_serialization() -> None:
    m = CRModel(name="my-service")
    assert m.model_dump()["name"] == "my-service"


@pytest.mark.parametrize("value", ["my-vm-instance", "a", "my-resource-123"])
def test_valid_compute_resource_name(value: str) -> None:
    m = ComputeModel(name=value)
    assert m.name == value


@pytest.mark.parametrize("value", ["", "1starts", "-starts", "ends-", "a" * 64, "MyVM"])
def test_invalid_compute_resource_name(value: str) -> None:
    with pytest.raises(ValidationError):
        ComputeModel(name=value)


def test_compute_resource_name_serialization() -> None:
    m = ComputeModel(name="my-vm-instance")
    assert m.model_dump()["name"] == "my-vm-instance"


@pytest.mark.parametrize("value", ["my-function", "a", "my-func-123"])
def test_valid_cloud_function_name(value: str) -> None:
    m = CFModel(name=value)
    assert m.name == value


@pytest.mark.parametrize("value", ["", "1starts", "-starts", "ends-", "a" * 50, "MyFunc"])
def test_invalid_cloud_function_name(value: str) -> None:
    with pytest.raises(ValidationError):
        CFModel(name=value)


def test_cloud_function_name_serialization() -> None:
    m = CFModel(name="my-function")
    assert m.model_dump()["name"] == "my-function"
