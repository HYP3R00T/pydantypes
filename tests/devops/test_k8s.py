from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError
from pydantic_core import PydanticCustomError

from pydantypes.devops.k8s import (
    K8sLabelKey,
    K8sLabelValue,
    K8sNamespaceName,
    K8sResourceName,
)


class NsModel(BaseModel):
    ns: K8sNamespaceName


class ResModel(BaseModel):
    name: K8sResourceName


class LabelKeyModel(BaseModel):
    key: K8sLabelKey


class LabelValueModel(BaseModel):
    val: K8sLabelValue


class TestK8sNamespaceNameValid:
    def test_default(self) -> None:
        m = NsModel(ns="default")
        assert m.ns == "default"

    def test_kube_system(self) -> None:
        m = NsModel(ns="kube-system")
        assert m.ns == "kube-system"

    def test_single_char(self) -> None:
        m = NsModel(ns="a")
        assert m.ns == "a"

    def test_max_length(self) -> None:
        m = NsModel(ns="a" * 63)
        assert len(m.ns) == 63


class TestK8sNamespaceNameInvalid:
    def test_empty(self) -> None:
        with pytest.raises(ValidationError):
            NsModel(ns="")

    def test_starts_with_dash(self) -> None:
        with pytest.raises(ValidationError):
            NsModel(ns="-starts")

    def test_ends_with_dash(self) -> None:
        with pytest.raises(ValidationError):
            NsModel(ns="ends-")

    def test_uppercase(self) -> None:
        with pytest.raises(ValidationError):
            NsModel(ns="UPPER")

    def test_too_long(self) -> None:
        with pytest.raises(ValidationError):
            NsModel(ns="a" * 64)


class TestK8sResourceNameValid:
    def test_deployment(self) -> None:
        m = ResModel(name="my-deployment")
        assert m.name == "my-deployment"

    def test_single_char(self) -> None:
        m = ResModel(name="a")
        assert m.name == "a"

    def test_subdomain(self) -> None:
        m = ResModel(name="sub.domain.name")
        assert m.name == "sub.domain.name"


class TestK8sResourceNameInvalid:
    def test_empty(self) -> None:
        with pytest.raises(ValidationError):
            ResModel(name="")

    def test_starts_with_dash(self) -> None:
        with pytest.raises(ValidationError):
            ResModel(name="-starts")

    def test_too_long(self) -> None:
        with pytest.raises(ValidationError):
            ResModel(name="a" * 254)

    def test_consecutive_dots(self) -> None:
        with pytest.raises(ValidationError):
            ResModel(name="has..dots")


class TestK8sLabelKeyValid:
    def test_simple_name(self) -> None:
        k = K8sLabelKey("app")
        assert k.prefix is None
        assert k.name == "app"

    def test_version(self) -> None:
        k = K8sLabelKey("version")
        assert k.prefix is None
        assert k.name == "version"

    def test_prefixed_key(self) -> None:
        k = K8sLabelKey("app.kubernetes.io/name")
        assert k.prefix == "app.kubernetes.io"
        assert k.name == "name"

    def test_my_label(self) -> None:
        k = K8sLabelKey("my-label")
        assert k.prefix is None
        assert k.name == "my-label"

    def test_pydantic_model(self) -> None:
        m = LabelKeyModel(key="version")
        assert isinstance(m.key, K8sLabelKey)


class TestK8sLabelKeyInvalid:
    def test_empty(self) -> None:
        with pytest.raises(PydanticCustomError):
            K8sLabelKey("")

    def test_empty_prefix(self) -> None:
        with pytest.raises(PydanticCustomError):
            K8sLabelKey("/name")

    def test_name_too_long(self) -> None:
        with pytest.raises(PydanticCustomError):
            K8sLabelKey("a" * 64)


class TestK8sLabelValueValid:
    def test_version(self) -> None:
        m = LabelValueModel(val="v1.0")
        assert m.val == "v1.0"

    def test_production(self) -> None:
        m = LabelValueModel(val="production")
        assert m.val == "production"

    def test_empty(self) -> None:
        m = LabelValueModel(val="")
        assert m.val == ""

    def test_single_char(self) -> None:
        m = LabelValueModel(val="a")
        assert m.val == "a"

    def test_max_length(self) -> None:
        m = LabelValueModel(val="a" * 63)
        assert len(m.val) == 63


class TestK8sLabelValueInvalid:
    def test_starts_with_dash(self) -> None:
        with pytest.raises(ValidationError):
            LabelValueModel(val="-starts")

    def test_ends_with_dash(self) -> None:
        with pytest.raises(ValidationError):
            LabelValueModel(val="ends-")

    def test_too_long(self) -> None:
        with pytest.raises(ValidationError):
            LabelValueModel(val="a" * 64)

    def test_has_spaces(self) -> None:
        with pytest.raises(ValidationError):
            LabelValueModel(val="has spaces")
