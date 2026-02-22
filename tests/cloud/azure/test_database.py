"""Tests for database."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.azure.database import CosmosDbAccountName, SqlServerName


class CosmosDbAccountNameModel(BaseModel):
    field: CosmosDbAccountName


class SqlServerNameModel(BaseModel):
    field: SqlServerName


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
