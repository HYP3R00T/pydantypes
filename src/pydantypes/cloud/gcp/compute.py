from __future__ import annotations

import re
from typing import Annotated

from pydantic import AfterValidator, WithJsonSchema
from pydantic_core import PydanticCustomError

_CLOUD_RUN_SERVICE_NAME_RE = re.compile(r"^[a-z]([a-z0-9-]{0,47}[a-z0-9])?$")


def _validate_cloud_run_service_name(v: str) -> str:
    if not _CLOUD_RUN_SERVICE_NAME_RE.match(v):
        raise PydanticCustomError(
            "gcp_cloud_run_service_name",
            "Invalid GCP Cloud Run service name: {value}",
            {"value": v},
        )
    return v


CloudRunServiceName = Annotated[
    str,
    AfterValidator(_validate_cloud_run_service_name),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": _CLOUD_RUN_SERVICE_NAME_RE.pattern,
            "description": "A GCP Cloud Run service name (1-49 lowercase chars).",
            "examples": ["my-service"],
            "title": "CloudRunServiceName",
        }
    ),
]
