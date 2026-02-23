"""Tests for AWS monitoring types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.aws.monitoring import CloudWatchLogGroupName


class CwModel(BaseModel):
    log_group: CloudWatchLogGroupName


@pytest.mark.parametrize("value", ["/my-app/production", "my-log-group", "#special"])
def test_valid_cloudwatch_log_group_name(value: str) -> None:
    model = CwModel(log_group=value)
    assert model.log_group == value


@pytest.mark.parametrize("value", ["", "aws/reserved", "my log group"])
def test_invalid_cloudwatch_log_group_name(value: str) -> None:
    with pytest.raises(ValidationError):
        CwModel(log_group=value)


def test_cloudwatch_log_group_name_serialization() -> None:
    model = CwModel(log_group="/my-app/production")
    assert model.model_dump() == {"log_group": "/my-app/production"}
