from __future__ import annotations

import re
from typing import Any, ClassVar

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError

from pydantypes._internal import _str_type_core_schema


class PubSubTopicName(str):
    """A validated GCP Pub/Sub topic name (projects/{project}/topics/{topic})."""

    _pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"^projects/([a-z][a-z0-9-]{4,28}[a-z0-9])/topics/([a-zA-Z][a-zA-Z0-9._~+%-]{2,254})$"
    )
    project_id: str
    topic_name: str

    def __new__(cls, value: str) -> PubSubTopicName:
        m = cls._pattern.match(value)
        if not m:
            raise PydanticCustomError(
                "gcp_pubsub_topic_name",
                "Invalid GCP Pub/Sub topic name: {value}",
                {"value": value},
            )
        instance = str.__new__(cls, value)
        instance.project_id = m.group(1)
        instance.topic_name = m.group(2)
        return instance

    @classmethod
    def _validate(cls, value: str) -> PubSubTopicName:
        return cls(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return _str_type_core_schema(cls, source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {
            "type": "string",
            "format": "gcp-pubsub-topic-name",
            "pattern": cls._pattern.pattern,
            "description": "A GCP Pub/Sub topic name (projects/{project}/topics/{topic}).",
            "examples": ["projects/my-project/topics/my-topic"],
            "title": "PubSubTopicName",
        }
