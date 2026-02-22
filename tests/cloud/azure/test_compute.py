"""Tests for compute."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.azure.compute import FunctionAppName


class FunctionAppNameModel(BaseModel):
    field: FunctionAppName


@pytest.mark.parametrize("value", ["my-app", "ab", "myapp123"])
def test_valid_function_app_name(value: str) -> None:
    m = FunctionAppNameModel(field=value)
    assert m.field == value


@pytest.mark.parametrize(
    "value",
    ["a", "-starts", "ends-", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"],
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
