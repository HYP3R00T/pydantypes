"""Tests for SQL types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.data.sql import TableIdentifier


class TableModel(BaseModel):
    table: TableIdentifier


@pytest.mark.parametrize(
    ("value", "catalog", "schema_name", "table_name"),
    [
        ("public.users", None, "public", "users"),
        ("my_catalog.my_schema.my_table", "my_catalog", "my_schema", "my_table"),
        ("_private.table_1", None, "_private", "table_1"),
    ],
)
def test_valid_table_identifier(
    value: str, catalog: str | None, schema_name: str, table_name: str
) -> None:
    model = TableModel(table=value)
    assert str(model.table) == value
    assert model.table.catalog == catalog
    assert model.table.schema_name == schema_name
    assert model.table.table_name == table_name


@pytest.mark.parametrize(
    "value",
    [
        "single",
        "",
        "a.b.c.d",
        "1invalid.table",
        "schema.1table",
    ],
)
def test_invalid_table_identifier(value: str) -> None:
    with pytest.raises(ValidationError):
        TableModel(table=value)


def test_table_identifier_serialization() -> None:
    model = TableModel(table="public.users")
    assert model.model_dump() == {"table": "public.users"}
    json_str = model.model_dump_json()
    restored = TableModel.model_validate_json(json_str)
    assert restored.table == model.table
    assert restored.table.schema_name == "public"


def test_table_identifier_existing_instance() -> None:
    t = TableIdentifier("public.users")
    model = TableModel(table=t)
    assert model.table is t


def test_table_identifier_json_schema() -> None:
    schema = TableModel.model_json_schema()
    field_schema = schema["properties"]["table"]
    assert field_schema["type"] == "string"
    assert field_schema["format"] == "sql-table-identifier"
