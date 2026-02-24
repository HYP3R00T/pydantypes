"""GCP messaging types."""

from __future__ import annotations

import re
from typing import Any, ClassVar

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError

from pydantypes._internal import _str_type_core_schema


# Source: https://cloud.google.com/pubsub/docs/pubsub-basics#resource_names
class PubSubTopicName(str):
    """A validated GCP Pub/Sub topic name (projects/{project}/topics/{topic})."""

    _pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"^projects/([a-z][a-z0-9-]{4,28}[a-z0-9]|\d+)/topics/([a-zA-Z][a-zA-Z0-9._~+%-]{2,254})$"
    )
    project_id: str
    topic_name: str

    def __new__(cls, value: str) -> PubSubTopicName:
        """Create and validate a new PubSubTopicName instance."""
        m = cls._pattern.match(value)
        if not m:
            raise PydanticCustomError(
                "gcp_pubsub_topic_name",
                "Invalid GCP Pub/Sub topic name: {value}",
                {"value": value},
            )
        topic_name = m.group(2)
        if topic_name.lower().startswith("goog"):
            raise PydanticCustomError(
                "gcp_pubsub_topic_name",
                "Invalid GCP Pub/Sub topic name: must not start with 'goog'. Got: {value}",
                {"value": value},
            )
        instance = str.__new__(cls, value)
        instance.project_id = m.group(1)
        instance.topic_name = topic_name
        return instance

    @classmethod
    def _validate(cls, value: str) -> PubSubTopicName:
        """Validate a string as a Pub/Sub topic name."""
        return cls(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Return the Pydantic core schema for PubSubTopicName."""
        return _str_type_core_schema(cls, source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """Return the JSON schema for PubSubTopicName."""
        return {
            "type": "string",
            "format": "gcp-pubsub-topic-name",
            "pattern": cls._pattern.pattern,
            "description": "A GCP Pub/Sub topic name (projects/{project}/topics/{topic}).",
            "examples": ["projects/my-project/topics/my-topic"],
            "title": "PubSubTopicName",
        }


# Source: https://cloud.google.com/pubsub/docs/pubsub-basics#resource_names
class PubSubSubscriptionName(str):
    """A validated GCP Pub/Sub subscription name."""

    _pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"^projects/([a-z][a-z0-9-]{4,28}[a-z0-9]|\d+)"
        r"/subscriptions/([a-zA-Z][a-zA-Z0-9._~+%-]{2,254})$"
    )
    project_id: str
    subscription_name: str

    def __new__(cls, value: str) -> PubSubSubscriptionName:
        """Create and validate a new PubSubSubscriptionName instance."""
        m = cls._pattern.match(value)
        if not m:
            raise PydanticCustomError(
                "gcp_pubsub_subscription_name",
                "Invalid GCP Pub/Sub subscription name: {value}",
                {"value": value},
            )
        sub_name = m.group(2)
        if sub_name.lower().startswith("goog"):
            raise PydanticCustomError(
                "gcp_pubsub_subscription_name",
                "Invalid GCP Pub/Sub subscription name: must not start with 'goog'. Got: {value}",
                {"value": value},
            )
        instance = str.__new__(cls, value)
        instance.project_id = m.group(1)
        instance.subscription_name = sub_name
        return instance

    @classmethod
    def _validate(cls, value: str) -> PubSubSubscriptionName:
        """Validate a string as a Pub/Sub subscription name."""
        return cls(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Return the Pydantic core schema for PubSubSubscriptionName."""
        return _str_type_core_schema(cls, source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """Return the JSON schema for PubSubSubscriptionName."""
        return {
            "type": "string",
            "format": "gcp-pubsub-subscription-name",
            "pattern": cls._pattern.pattern,
            "description": (
                "A GCP Pub/Sub subscription name (projects/{project}/subscriptions/{subscription})."
            ),
            "examples": ["projects/my-project/subscriptions/my-subscription"],
            "title": "PubSubSubscriptionName",
        }
