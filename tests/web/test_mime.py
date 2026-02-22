"""Tests for MIME type."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.web.mime import MimeType


class MimeModel(BaseModel):
    mime: MimeType


@pytest.mark.parametrize(
    ("value", "expected_type", "expected_subtype", "expected_params"),
    [
        ("application/json", "application", "json", {}),
        ("text/html", "text", "html", {}),
        ("text/html;charset=utf-8", "text", "html", {"charset": "utf-8"}),
        ("image/png", "image", "png", {}),
        ("application/vnd.api+json", "application", "vnd.api+json", {}),
    ],
)
def test_valid_mime_type(
    value: str,
    expected_type: str,
    expected_subtype: str,
    expected_params: dict,
) -> None:
    model = MimeModel(mime=value)
    assert str(model.mime) == value
    assert model.mime.type == expected_type
    assert model.mime.subtype == expected_subtype
    assert model.mime.parameters == expected_params


@pytest.mark.parametrize("value", ["", "invalid", "/json", "text/"])
def test_invalid_mime_type(value: str) -> None:
    with pytest.raises(ValidationError):
        MimeModel(mime=value)


def test_mime_type_serialization() -> None:
    model = MimeModel(mime="application/json")
    assert model.model_dump() == {"mime": "application/json"}
    json_str = model.model_dump_json()
    restored = MimeModel.model_validate_json(json_str)
    assert restored.mime == model.mime


def test_mime_type_existing_instance() -> None:
    mime = MimeType("application/json")
    model = MimeModel(mime=mime)
    assert model.mime is mime


def test_mime_type_json_schema() -> None:
    schema = MimeModel.model_json_schema()
    field_schema = schema["properties"]["mime"]
    assert field_schema["type"] == "string"
    assert field_schema["format"] == "mime-type"
