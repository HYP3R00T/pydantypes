"""Tests for Azure database types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.azure.database import (
    CosmosDbAccountName,
    DatabricksWorkspaceName,
    DataFactoryName,
    RedisCacheName,
    SqlServerName,
)


class CosmosDbAccountNameModel(BaseModel):
    field: CosmosDbAccountName


class SqlServerNameModel(BaseModel):
    field: SqlServerName


class RedisCacheNameModel(BaseModel):
    field: RedisCacheName


class DataFactoryNameModel(BaseModel):
    field: DataFactoryName


class DatabricksModel(BaseModel):
    field: DatabricksWorkspaceName


# --- CosmosDbAccountName tests ---


@pytest.mark.parametrize("value", ["my-cosmos-account", "abc", "a0b"])
def test_valid_cosmos_db_account_name(value: str) -> None:
    m = CosmosDbAccountNameModel(field=value)
    assert m.field == value


@pytest.mark.parametrize("value", ["ab", "MyAccount", "-start"])
def test_invalid_cosmos_db_account_name(value: str) -> None:
    with pytest.raises(ValidationError):
        CosmosDbAccountNameModel(field=value)


def test_cosmos_db_account_name_serialization() -> None:
    m = CosmosDbAccountNameModel(field="my-cosmos-account")
    assert m.model_dump()["field"] == "my-cosmos-account"


# --- SqlServerName tests ---


@pytest.mark.parametrize("value", ["my-sql-server", "a", "server1"])
def test_valid_sql_server_name(value: str) -> None:
    m = SqlServerNameModel(field=value)
    assert m.field == value


@pytest.mark.parametrize("value", ["-start", "MyServer"])
def test_invalid_sql_server_name(value: str) -> None:
    with pytest.raises(ValidationError):
        SqlServerNameModel(field=value)


def test_sql_server_name_serialization() -> None:
    m = SqlServerNameModel(field="my-sql-server")
    assert m.model_dump()["field"] == "my-sql-server"


def test_sql_server_name_json_schema() -> None:
    schema = SqlServerNameModel.model_json_schema()
    props = schema["properties"]["field"]
    assert props["type"] == "string"


# --- RedisCacheName tests ---


@pytest.mark.parametrize("value", ["my-redis-cache", "ab", "redis123"])
def test_valid_redis_cache_name(value: str) -> None:
    m = RedisCacheNameModel(field=value)
    assert m.field == value


@pytest.mark.parametrize("value", ["-starts", "my--redis", "a"])
def test_invalid_redis_cache_name(value: str) -> None:
    with pytest.raises(ValidationError):
        RedisCacheNameModel(field=value)


def test_redis_cache_name_serialization() -> None:
    m = RedisCacheNameModel(field="my-redis-cache")
    assert m.model_dump()["field"] == "my-redis-cache"


# --- DataFactoryName tests ---


@pytest.mark.parametrize("value", ["my-data-factory", "abc", "factory123"])
def test_valid_data_factory_name(value: str) -> None:
    m = DataFactoryNameModel(field=value)
    assert m.field == value


@pytest.mark.parametrize("value", ["-starts", "my--factory", "ab"])
def test_invalid_data_factory_name(value: str) -> None:
    with pytest.raises(ValidationError):
        DataFactoryNameModel(field=value)


def test_data_factory_name_serialization() -> None:
    m = DataFactoryNameModel(field="my-data-factory")
    assert m.model_dump()["field"] == "my-data-factory"


# --- DatabricksWorkspaceName tests ---


@pytest.mark.parametrize("value", ["my-databricks-ws", "abc", "ws_123"])
def test_valid_databricks_workspace_name(value: str) -> None:
    m = DatabricksModel(field=value)
    assert m.field == value


@pytest.mark.parametrize("value", ["-starts", "ab", ""])
def test_invalid_databricks_workspace_name(value: str) -> None:
    with pytest.raises(ValidationError):
        DatabricksModel(field=value)


def test_databricks_workspace_name_serialization() -> None:
    m = DatabricksModel(field="my-databricks-ws")
    assert m.model_dump()["field"] == "my-databricks-ws"
