"""Tests for JWT type."""

from __future__ import annotations

import base64
import json

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.web.jwt import Jwt


def _make_jwt(header: dict, payload: dict, sig: str = "signature") -> str:
    h = base64.urlsafe_b64encode(json.dumps(header).encode()).rstrip(b"=").decode()
    p = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b"=").decode()
    s = base64.urlsafe_b64encode(sig.encode()).rstrip(b"=").decode()
    return f"{h}.{p}.{s}"


class JwtModel(BaseModel):
    token: Jwt


def test_valid_jwt() -> None:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": "1234567890", "name": "John Doe"}
    token = _make_jwt(header, payload)
    model = JwtModel(token=token)
    assert model.token.header == header
    assert model.token.payload == payload


def test_valid_jwt_empty_signature() -> None:
    header = {"alg": "none"}
    payload = {"sub": "test"}
    h = base64.urlsafe_b64encode(json.dumps(header).encode()).rstrip(b"=").decode()
    p = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b"=").decode()
    token = f"{h}.{p}."
    model = JwtModel(token=token)
    assert model.token.header == header
    assert model.token.payload == payload


@pytest.mark.parametrize(
    "value",
    [
        "not-a-jwt",
        "a.b",
        "a.b.c.d",
        "",
    ],
)
def test_invalid_jwt(value: str) -> None:
    with pytest.raises(ValidationError):
        JwtModel(token=value)


def test_jwt_invalid_header_json() -> None:
    # Header that's not valid JSON
    h = base64.urlsafe_b64encode(b"not-json").rstrip(b"=").decode()
    p = base64.urlsafe_b64encode(b'{"sub":"test"}').rstrip(b"=").decode()
    with pytest.raises(ValidationError):
        JwtModel(token=f"{h}.{p}.sig")


def test_jwt_serialization() -> None:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": "1234567890"}
    token = _make_jwt(header, payload)
    model = JwtModel(token=token)
    json_str = model.model_dump_json()
    restored = JwtModel.model_validate_json(json_str)
    assert restored.token == model.token
    assert restored.token.header == header
    assert restored.token.payload == payload


def test_jwt_existing_instance() -> None:
    token = _make_jwt({"alg": "HS256"}, {"sub": "test"})
    jwt = Jwt(token)
    model = JwtModel(token=jwt)
    assert model.token is jwt


def test_jwt_json_schema() -> None:
    schema = JwtModel.model_json_schema()
    field_schema = schema["properties"]["token"]
    assert field_schema["type"] == "string"
    assert field_schema["format"] == "jwt"
