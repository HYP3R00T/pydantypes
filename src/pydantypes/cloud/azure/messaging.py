"""Azure messaging types: ServiceBusNamespace."""

from __future__ import annotations

import re
from typing import Annotated

from pydantic import AfterValidator, WithJsonSchema
from pydantic_core import PydanticCustomError

_SERVICE_BUS_NAMESPACE_PATTERN = re.compile(r"^[a-zA-Z](?!.*--)[a-zA-Z0-9-]{4,48}[a-zA-Z0-9]$")


def _validate_service_bus_namespace(v: str) -> str:
    if not _SERVICE_BUS_NAMESPACE_PATTERN.match(v):
        raise PydanticCustomError(
            "azure_service_bus_namespace",
            "Invalid Azure Service Bus namespace: {value}",
            {"value": v},
        )
    return v


ServiceBusNamespace = Annotated[
    str,
    AfterValidator(_validate_service_bus_namespace),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": r"^[a-zA-Z](?!.*--)[a-zA-Z0-9-]{4,48}[a-zA-Z0-9]$",
            "description": "Azure Service Bus namespace.",
            "examples": ["my-servicebus-ns"],
            "title": "ServiceBusNamespace",
        }
    ),
]
