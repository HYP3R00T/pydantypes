from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.gcp.compute import CloudRunServiceName


class CRModel(BaseModel):
    name: CloudRunServiceName


@pytest.mark.parametrize("value", ["my-service", "a", "a-long-service-name"])
class TestCloudRunServiceNameValid:
    def test_pydantic_accepts(self, value: str) -> None:
        m = CRModel(name=value)
        assert m.name == value


@pytest.mark.parametrize(
    "value",
    [
        "",
        "1starts",
        "-starts",
        "ends-",
        "a" * 50,
        "MyService",
    ],
)
class TestCloudRunServiceNameInvalid:
    def test_pydantic_rejects(self, value: str) -> None:
        with pytest.raises(ValidationError):
            CRModel(name=value)
