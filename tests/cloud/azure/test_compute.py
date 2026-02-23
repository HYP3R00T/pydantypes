"""Tests for Azure compute types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.azure.compute import (
    AksClusterName,
    ApiManagementName,
    AppServiceName,
    ContainerAppName,
    FunctionAppName,
    LogAnalyticsWorkspaceName,
)


class FunctionAppNameModel(BaseModel):
    field: FunctionAppName


class AppServiceNameModel(BaseModel):
    field: AppServiceName


class AksClusterNameModel(BaseModel):
    field: AksClusterName


class ContainerAppNameModel(BaseModel):
    field: ContainerAppName


class LogAnalyticsModel(BaseModel):
    field: LogAnalyticsWorkspaceName


class ApiManagementModel(BaseModel):
    field: ApiManagementName


@pytest.mark.parametrize("value", ["my-app", "ab", "myapp123"])
def test_valid_function_app_name(value: str) -> None:
    m = FunctionAppNameModel(field=value)
    assert m.field == value


@pytest.mark.parametrize(
    "value",
    ["a", "-starts", "ends-", "a" * 61],
)
def test_invalid_function_app_name(value: str) -> None:
    with pytest.raises(ValidationError):
        FunctionAppNameModel(field=value)


def test_function_app_name_serialization() -> None:
    m = FunctionAppNameModel(field="my-app")
    assert m.model_dump()["field"] == "my-app"


def test_function_app_name_json_schema() -> None:
    schema = FunctionAppNameModel.model_json_schema()
    props = schema["properties"]["field"]
    assert props["type"] == "string"


@pytest.mark.parametrize("value", ["my-app-service", "a", "app123"])
def test_valid_app_service_name(value: str) -> None:
    m = AppServiceNameModel(field=value)
    assert m.field == value


@pytest.mark.parametrize("value", ["-starts", "ends-", ""])
def test_invalid_app_service_name(value: str) -> None:
    with pytest.raises(ValidationError):
        AppServiceNameModel(field=value)


def test_app_service_name_serialization() -> None:
    m = AppServiceNameModel(field="my-app-service")
    assert m.model_dump()["field"] == "my-app-service"


@pytest.mark.parametrize("value", ["my-aks-cluster", "a", "cluster_123"])
def test_valid_aks_cluster_name(value: str) -> None:
    m = AksClusterNameModel(field=value)
    assert m.field == value


@pytest.mark.parametrize("value", ["-starts", "", "a" * 64])
def test_invalid_aks_cluster_name(value: str) -> None:
    with pytest.raises(ValidationError):
        AksClusterNameModel(field=value)


def test_aks_cluster_name_serialization() -> None:
    m = AksClusterNameModel(field="my-aks-cluster")
    assert m.model_dump()["field"] == "my-aks-cluster"


@pytest.mark.parametrize("value", ["my-container-app", "a", "app1"])
def test_valid_container_app_name(value: str) -> None:
    m = ContainerAppNameModel(field=value)
    assert m.field == value


@pytest.mark.parametrize("value", ["1starts", "MyApp", "-starts", ""])
def test_invalid_container_app_name(value: str) -> None:
    with pytest.raises(ValidationError):
        ContainerAppNameModel(field=value)


def test_container_app_name_serialization() -> None:
    m = ContainerAppNameModel(field="my-container-app")
    assert m.model_dump()["field"] == "my-container-app"


@pytest.mark.parametrize("value", ["my-log-analytics", "abcd"])
def test_valid_log_analytics_workspace_name(value: str) -> None:
    m = LogAnalyticsModel(field=value)
    assert m.field == value


@pytest.mark.parametrize("value", ["-starts", "ab", "a", ""])
def test_invalid_log_analytics_workspace_name(value: str) -> None:
    with pytest.raises(ValidationError):
        LogAnalyticsModel(field=value)


def test_log_analytics_workspace_name_serialization() -> None:
    m = LogAnalyticsModel(field="my-log-analytics")
    assert m.model_dump()["field"] == "my-log-analytics"


@pytest.mark.parametrize("value", ["my-apim", "a", "apim123"])
def test_valid_api_management_name(value: str) -> None:
    m = ApiManagementModel(field=value)
    assert m.field == value


@pytest.mark.parametrize("value", ["1starts", "-starts", ""])
def test_invalid_api_management_name(value: str) -> None:
    with pytest.raises(ValidationError):
        ApiManagementModel(field=value)


def test_api_management_name_serialization() -> None:
    m = ApiManagementModel(field="my-apim")
    assert m.model_dump()["field"] == "my-apim"
