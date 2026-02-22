"""Azure database types: CosmosDbAccountName, SqlServerName."""

from __future__ import annotations

import re
from typing import Annotated

from pydantic import AfterValidator, WithJsonSchema
from pydantic_core import PydanticCustomError

_COSMOS_DB_ACCOUNT_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{1,42}[a-z0-9]$")
_SQL_SERVER_NAME_PATTERN = re.compile(r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$")


# --- CosmosDbAccountName ---


def _validate_cosmos_db_account_name(v: str) -> str:
    if not _COSMOS_DB_ACCOUNT_NAME_PATTERN.match(v):
        raise PydanticCustomError(
            "azure_cosmos_db_account_name",
            "Invalid Azure Cosmos DB account name: {value}",
            {"value": v},
        )
    return v


CosmosDbAccountName = Annotated[
    str,
    AfterValidator(_validate_cosmos_db_account_name),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": r"^[a-z0-9][a-z0-9-]{1,42}[a-z0-9]$",
            "description": "Azure Cosmos DB account name.",
            "examples": ["my-cosmos-account"],
            "title": "CosmosDbAccountName",
        }
    ),
]


# --- SqlServerName ---


def _validate_sql_server_name(v: str) -> str:
    if not _SQL_SERVER_NAME_PATTERN.match(v):
        raise PydanticCustomError(
            "azure_sql_server_name",
            "Invalid Azure SQL Server name: {value}",
            {"value": v},
        )
    return v


SqlServerName = Annotated[
    str,
    AfterValidator(_validate_sql_server_name),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$",
            "description": "Azure SQL Server name.",
            "examples": ["my-sql-server"],
            "title": "SqlServerName",
        }
    ),
]
