"""Tests for AWS database types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.aws.database import DynamoDbTableName, RdsInstanceId


class DynamoModel(BaseModel):
    table: DynamoDbTableName


class RdsModel(BaseModel):
    instance: RdsInstanceId


@pytest.mark.parametrize("value", ["my-table", "a.b.c", "MyTable_123", "abc"])
def test_valid_dynamodb_table_name(value: str) -> None:
    model = DynamoModel(table=value)
    assert model.table == value


@pytest.mark.parametrize("value", ["ab", "", "a" * 256, "table name"])
def test_invalid_dynamodb_table_name(value: str) -> None:
    with pytest.raises(ValidationError):
        DynamoModel(table=value)


def test_dynamodb_table_name_serialization() -> None:
    model = DynamoModel(table="my-table")
    assert model.model_dump() == {"table": "my-table"}
    json_str = model.model_dump_json()
    restored = DynamoModel.model_validate_json(json_str)
    assert restored.table == model.table


@pytest.mark.parametrize("value", ["my-db-instance", "a", "mydb123"])
def test_valid_rds_instance_id(value: str) -> None:
    model = RdsModel(instance=value)
    assert model.instance == value


@pytest.mark.parametrize("value", ["", "1starts-with-number", "my--db", "my-db-"])
def test_invalid_rds_instance_id(value: str) -> None:
    with pytest.raises(ValidationError):
        RdsModel(instance=value)


def test_rds_instance_id_serialization() -> None:
    model = RdsModel(instance="my-db-instance")
    assert model.model_dump() == {"instance": "my-db-instance"}
    json_str = model.model_dump_json()
    restored = RdsModel.model_validate_json(json_str)
    assert restored.instance == model.instance
