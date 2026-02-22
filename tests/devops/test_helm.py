from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.devops.helm import HelmChartName


class HelmModel(BaseModel):
    name: HelmChartName


class TestHelmChartNameValid:
    @pytest.mark.parametrize("value", ["nginx", "cert-manager", "0-start-with-num"])
    def test_valid_names(self, value: str) -> None:
        m = HelmModel(name=value)
        assert m.name == value


class TestHelmChartNameInvalid:
    def test_empty(self) -> None:
        with pytest.raises(ValidationError):
            HelmModel(name="")

    def test_starts_with_dash(self) -> None:
        with pytest.raises(ValidationError):
            HelmModel(name="-starts")

    def test_uppercase(self) -> None:
        with pytest.raises(ValidationError):
            HelmModel(name="UPPER")

    def test_has_spaces(self) -> None:
        with pytest.raises(ValidationError):
            HelmModel(name="has spaces")

    def test_has_dots(self) -> None:
        with pytest.raises(ValidationError):
            HelmModel(name="has.dots")
