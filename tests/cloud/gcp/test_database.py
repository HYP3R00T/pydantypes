"""Tests for GCP database types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.gcp.database import (
    BigQueryDatasetId,
    BigQueryTableId,
    CloudSqlInstanceId,
    SpannerDatabaseId,
    SpannerInstanceId,
)


class BQModel(BaseModel):
    dataset: BigQueryDatasetId


class SQLModel(BaseModel):
    instance: CloudSqlInstanceId


class BQTableModel(BaseModel):
    table: BigQueryTableId


class SpannerInstModel(BaseModel):
    instance: SpannerInstanceId


class SpannerDbModel(BaseModel):
    database: SpannerDatabaseId


@pytest.mark.parametrize("value", ["my_dataset", "A", "dataset_123"])
class TestBigQueryDatasetIdValid:
    def test_pydantic_accepts(self, value: str) -> None:
        m = BQModel(dataset=value)
        assert m.dataset == value


@pytest.mark.parametrize(
    "value",
    [
        "",
        "has spaces",
        "has-hyphens",
        "a" * 1025,
    ],
)
class TestBigQueryDatasetIdInvalid:
    def test_pydantic_rejects(self, value: str) -> None:
        with pytest.raises(ValidationError):
            BQModel(dataset=value)


def test_bigquery_dataset_id_serialization() -> None:
    m = BQModel(dataset="my_dataset")
    assert m.model_dump()["dataset"] == "my_dataset"


@pytest.mark.parametrize("value", ["my-sql-instance", "a"])
class TestCloudSqlInstanceIdValid:
    def test_pydantic_accepts(self, value: str) -> None:
        m = SQLModel(instance=value)
        assert m.instance == value


@pytest.mark.parametrize(
    "value",
    [
        "",
        "1starts",
        "-starts",
        "MyInstance",
        "a" * 85,
    ],
)
class TestCloudSqlInstanceIdInvalid:
    def test_pydantic_rejects(self, value: str) -> None:
        with pytest.raises(ValidationError):
            SQLModel(instance=value)


def test_cloud_sql_instance_id_length_limit() -> None:
    """84-char instance ID is valid, 85 is not."""
    valid = "a" + "b" * 83
    m = SQLModel(instance=valid)
    assert m.instance == valid

    with pytest.raises(ValidationError):
        SQLModel(instance="a" + "b" * 84)


def test_cloud_sql_instance_id_serialization() -> None:
    m = SQLModel(instance="my-sql-instance")
    assert m.model_dump()["instance"] == "my-sql-instance"


@pytest.mark.parametrize(
    "value",
    [
        "my-project.my_dataset.my_table",
        "my-project:my_dataset.my_table",
        "123456789012.my_dataset.my_table",
    ],
)
def test_valid_bigquery_table_id(value: str) -> None:
    m = BQTableModel(table=value)
    assert str(m.table) == value


@pytest.mark.parametrize(
    "value",
    [
        "just-a-string",
        "project",
        ".dataset.table",
        "project.dataset",
    ],
)
def test_invalid_bigquery_table_id(value: str) -> None:
    with pytest.raises(ValidationError):
        BQTableModel(table=value)


def test_bigquery_table_id_properties_standard() -> None:
    m = BQTableModel(table="my-project.my_dataset.my_table")
    assert m.table.project_id == "my-project"
    assert m.table.dataset_id == "my_dataset"
    assert m.table.table_id == "my_table"


def test_bigquery_table_id_properties_legacy() -> None:
    m = BQTableModel(table="my-project:my_dataset.my_table")
    assert m.table.project_id == "my-project"
    assert m.table.dataset_id == "my_dataset"
    assert m.table.table_id == "my_table"


def test_bigquery_table_id_serialization() -> None:
    m = BQTableModel(table="my-project.my_dataset.my_table")
    assert m.model_dump()["table"] == "my-project.my_dataset.my_table"


def test_bigquery_table_id_json_schema() -> None:
    schema = BQTableModel.model_json_schema()
    props = schema["properties"]["table"]
    assert props["type"] == "string"
    assert props["format"] == "gcp-bigquery-table-id"


def test_bigquery_table_id_existing_instance() -> None:
    t = BigQueryTableId("my-project.my_dataset.my_table")
    m = BQTableModel(table=t)
    assert m.table is t


@pytest.mark.parametrize("value", ["my-spanner-instance", "ab"])
def test_valid_spanner_instance_id(value: str) -> None:
    m = SpannerInstModel(instance=value)
    assert m.instance == value


@pytest.mark.parametrize("value", ["a", "", "1starts", "a" * 65])
def test_invalid_spanner_instance_id(value: str) -> None:
    with pytest.raises(ValidationError):
        SpannerInstModel(instance=value)


def test_spanner_instance_id_serialization() -> None:
    m = SpannerInstModel(instance="my-spanner-instance")
    assert m.model_dump()["instance"] == "my-spanner-instance"


@pytest.mark.parametrize("value", ["my-spanner-db", "ab"])
def test_valid_spanner_database_id(value: str) -> None:
    m = SpannerDbModel(database=value)
    assert m.database == value


@pytest.mark.parametrize("value", ["a", "", "1starts", "a" * 31])
def test_invalid_spanner_database_id(value: str) -> None:
    with pytest.raises(ValidationError):
        SpannerDbModel(database=value)


def test_spanner_database_id_serialization() -> None:
    m = SpannerDbModel(database="my-spanner-db")
    assert m.model_dump()["database"] == "my-spanner-db"
