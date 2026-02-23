"""Tests for GCP container types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.gcp.containers import ArtifactRegistryImageUri


class ARModel(BaseModel):
    image: ArtifactRegistryImageUri


VALID_IMAGE = "us-docker.pkg.dev/my-project/my-repo/my-image:latest"
VALID_IMAGE_DIGEST = (
    "us-docker.pkg.dev/my-project/my-repo/my-image"
    "@sha256:abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789"
)


@pytest.mark.parametrize(
    "value",
    [
        VALID_IMAGE,
        "us-docker.pkg.dev/my-project/my-repo/my-image",
        VALID_IMAGE_DIGEST,
        "europe-west1-docker.pkg.dev/my-project/my-repo/nested/image:v1",
    ],
)
def test_valid_artifact_registry_image_uri(value: str) -> None:
    m = ARModel(image=value)
    assert str(m.image) == value


def test_artifact_registry_image_uri_properties() -> None:
    m = ARModel(image=VALID_IMAGE)
    assert m.image.location == "us"
    assert m.image.project_id == "my-project"
    assert m.image.repository == "my-repo"
    assert m.image.image == "my-image"
    assert m.image.tag == "latest"
    assert m.image.digest == ""


def test_artifact_registry_image_uri_digest_properties() -> None:
    m = ARModel(image=VALID_IMAGE_DIGEST)
    assert m.image.tag == ""
    assert m.image.digest.startswith("sha256:")


def test_artifact_registry_image_uri_no_tag_no_digest() -> None:
    m = ARModel(image="us-docker.pkg.dev/my-project/my-repo/my-image")
    assert m.image.tag == ""
    assert m.image.digest == ""


@pytest.mark.parametrize(
    "value",
    [
        "not-a-valid-uri",
        "us-docker.pkg.dev/ab/my-repo/my-image",
        "docker.io/library/nginx:latest",
        "",
    ],
)
def test_invalid_artifact_registry_image_uri(value: str) -> None:
    with pytest.raises(ValidationError):
        ARModel(image=value)


def test_artifact_registry_image_uri_serialization() -> None:
    m = ARModel(image=VALID_IMAGE)
    assert m.model_dump()["image"] == VALID_IMAGE


def test_artifact_registry_image_uri_json_schema() -> None:
    schema = ARModel.model_json_schema()
    props = schema["properties"]["image"]
    assert props["type"] == "string"
    assert props["format"] == "gcp-artifact-registry-image-uri"


def test_artifact_registry_image_uri_existing_instance() -> None:
    uri = ArtifactRegistryImageUri(VALID_IMAGE)
    m = ARModel(image=uri)
    assert m.image is uri
