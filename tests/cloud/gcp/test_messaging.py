from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.gcp.messaging import PubSubTopicName


class PSModel(BaseModel):
    topic: PubSubTopicName


class TestPubSubTopicNameValid:
    def test_basic(self) -> None:
        t = PubSubTopicName("projects/my-project/topics/my-topic")
        assert t.project_id == "my-project"
        assert t.topic_name == "my-topic"

    def test_complex_topic(self) -> None:
        t = PubSubTopicName("projects/my-project/topics/My.Topic_123")
        assert t.topic_name == "My.Topic_123"

    def test_pydantic_model(self) -> None:
        m = PSModel(topic="projects/my-project/topics/my-topic")
        assert isinstance(m.topic, PubSubTopicName)


@pytest.mark.parametrize(
    "value",
    [
        "my-project/topics/my-topic",
        "projects/ab/topics/my-topic",
        "projects/my-project/topics/ab",
        "projects/my-project/topics/1bad",
    ],
)
class TestPubSubTopicNameInvalid:
    def test_pydantic_rejects(self, value: str) -> None:
        with pytest.raises(ValidationError):
            PSModel(topic=value)
