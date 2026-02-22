from __future__ import annotations

import pytest
from pydantic import BaseModel
from pydantic_core import PydanticCustomError

from pydantypes.devops.terraform import TerraformResourceAddress


class TfModel(BaseModel):
    addr: TerraformResourceAddress


class TestTerraformValid:
    def test_aws_instance(self) -> None:
        addr = TerraformResourceAddress("aws_instance.web")
        assert addr.resource_type == "aws_instance"
        assert addr.resource_name == "web"

    def test_google_compute(self) -> None:
        addr = TerraformResourceAddress("google_compute_instance.default")
        assert addr.resource_type == "google_compute_instance"
        assert addr.resource_name == "default"

    def test_null_resource(self) -> None:
        addr = TerraformResourceAddress("null_resource.this")
        assert addr.resource_type == "null_resource"
        assert addr.resource_name == "this"

    def test_pydantic_model(self) -> None:
        m = TfModel(addr="aws_instance.web")
        assert isinstance(m.addr, TerraformResourceAddress)


class TestTerraformInvalid:
    def test_empty(self) -> None:
        with pytest.raises(PydanticCustomError):
            TerraformResourceAddress("")

    def test_no_dot(self) -> None:
        with pytest.raises(PydanticCustomError):
            TerraformResourceAddress("no-dot")

    def test_starts_with_dot(self) -> None:
        with pytest.raises(PydanticCustomError):
            TerraformResourceAddress(".starts-with-dot")

    def test_starts_with_digit(self) -> None:
        with pytest.raises(PydanticCustomError):
            TerraformResourceAddress("1invalid.name")

    def test_empty_name(self) -> None:
        with pytest.raises(PydanticCustomError):
            TerraformResourceAddress("type.")
