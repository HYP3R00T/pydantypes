from __future__ import annotations

import re
from typing import Annotated

from pydantic import AfterValidator, WithJsonSchema
from pydantic_core import PydanticCustomError

_BIGQUERY_DATASET_ID_RE = re.compile(r"^[a-zA-Z0-9_]{1,1024}$")
_CLOUD_SQL_INSTANCE_ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")


def _validate_bigquery_dataset_id(v: str) -> str:
    if not _BIGQUERY_DATASET_ID_RE.match(v):
        raise PydanticCustomError(
            "gcp_bigquery_dataset_id",
            "Invalid GCP BigQuery dataset ID: {value}",
            {"value": v},
        )
    return v


def _validate_cloud_sql_instance_id(v: str) -> str:
    if len(v) > 98:
        raise PydanticCustomError(
            "gcp_cloud_sql_instance_id",
            "Invalid GCP Cloud SQL instance ID: {value}",
            {"value": v},
        )
    if not _CLOUD_SQL_INSTANCE_ID_RE.match(v):
        raise PydanticCustomError(
            "gcp_cloud_sql_instance_id",
            "Invalid GCP Cloud SQL instance ID: {value}",
            {"value": v},
        )
    return v


BigQueryDatasetId = Annotated[
    str,
    AfterValidator(_validate_bigquery_dataset_id),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": _BIGQUERY_DATASET_ID_RE.pattern,
            "description": "A GCP BigQuery dataset ID.",
            "examples": ["my_dataset"],
            "title": "BigQueryDatasetId",
        }
    ),
]

CloudSqlInstanceId = Annotated[
    str,
    AfterValidator(_validate_cloud_sql_instance_id),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": _CLOUD_SQL_INSTANCE_ID_RE.pattern,
            "description": "A GCP Cloud SQL instance ID (max 98 chars).",
            "examples": ["my-sql-instance"],
            "title": "CloudSqlInstanceId",
        }
    ),
]
