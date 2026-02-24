"""AWS messaging types."""

from __future__ import annotations

import re
from typing import Any, ClassVar

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError

from pydantypes._internal import _str_type_core_schema


# Source: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html
class SqsQueueUrl(str):
    """An SQS Queue URL with parsed components."""

    _pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"^https://sqs\.([a-z0-9-]+)\.amazonaws\.com/(\d{12})/([a-zA-Z0-9_-]+(\.fifo)?)$"
    )

    region: str
    account_id: str
    queue_name: str

    def __new__(cls, value: str) -> SqsQueueUrl:
        """Create and validate a new SqsQueueUrl instance."""
        m = cls._pattern.match(value)
        if not m:
            raise PydanticCustomError(
                "sqs_queue_url",
                "Invalid SQS Queue URL: {value}",
                {"value": value},
            )
        queue_name = m.group(3)
        if len(queue_name) > 80:
            raise PydanticCustomError(
                "sqs_queue_url",
                "Invalid SQS Queue URL: queue name exceeds 80 characters. Got: {value}",
                {"value": value},
            )
        instance = str.__new__(cls, value)
        instance.region = m.group(1)
        instance.account_id = m.group(2)
        instance.queue_name = queue_name
        return instance

    @classmethod
    def _validate(cls, value: str) -> SqsQueueUrl:
        """Validate a string as an SQS Queue URL."""
        return cls(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Return the Pydantic core schema for SqsQueueUrl."""
        return _str_type_core_schema(cls, source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """Return the JSON schema for SqsQueueUrl."""
        return {
            "type": "string",
            "format": "aws-sqs-queue-url",
            "pattern": cls._pattern.pattern,
            "description": "An AWS SQS Queue URL",
            "examples": ["https://sqs.us-east-1.amazonaws.com/123456789012/my-queue"],
            "title": "SqsQueueUrl",
        }
