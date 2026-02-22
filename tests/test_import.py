"""Smoke tests — verify the package is importable."""

import pydantypes


def test_version() -> None:
    assert isinstance(pydantypes.__version__, str)


def test_subpackages_importable() -> None:
    from pydantypes import data, devops, web  # noqa: F401
    from pydantypes.cloud import aws, azure, gcp  # noqa: F401
