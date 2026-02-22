"""Azure compute types: FunctionAppName."""

from __future__ import annotations

import re
from typing import Annotated

from pydantic import AfterValidator, WithJsonSchema
from pydantic_core import PydanticCustomError

_FUNCTION_APP_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9-]{0,58}[a-zA-Z0-9]$")


def _validate_function_app_name(v: str) -> str:
    if not _FUNCTION_APP_NAME_PATTERN.match(v):
        raise PydanticCustomError(
            "azure_function_app_name",
            "Invalid Azure Function App name: {value}",
            {"value": v},
        )
    return v


FunctionAppName = Annotated[
    str,
    AfterValidator(_validate_function_app_name),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": r"^[a-zA-Z0-9][a-zA-Z0-9-]{0,58}[a-zA-Z0-9]$",
            "description": "Azure Function App name.",
            "examples": ["my-function-app"],
            "title": "FunctionAppName",
        }
    ),
]
