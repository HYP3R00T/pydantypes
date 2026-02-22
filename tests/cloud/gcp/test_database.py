from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.gcp.database import BigQueryDatasetId, CloudSqlInstanceId


class BQModel(BaseModel):
    dataset: BigQueryDatasetId


class SQLModel(BaseModel):
    instance: CloudSqlInstanceId


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
        "a" * 99,
    ],
)
class TestCloudSqlInstanceIdInvalid:
    def test_pydantic_rejects(self, value: str) -> None:
        with pytest.raises(ValidationError):
            SQLModel(instance=value)
