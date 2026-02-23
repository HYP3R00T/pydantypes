"""Tests for GCP messaging types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pydantypes.cloud.gcp.messaging import PubSubSubscriptionName, PubSubTopicName


class PSModel(BaseModel):
    topic: PubSubTopicName


class SubModel(BaseModel):
    sub: PubSubSubscriptionName


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

    def test_project_number(self) -> None:
        t = PubSubTopicName("projects/123456789012/topics/my-topic")
        assert t.project_id == "123456789012"
        assert t.topic_name == "my-topic"


@pytest.mark.parametrize(
    "value",
    [
        "my-project/topics/my-topic",
        "projects/ab/topics/my-topic",
        "projects/my-project/topics/ab",
        "projects/my-project/topics/1bad",
        "projects/my-project/topics/googTopic",
        "projects/my-project/topics/GoogTopic",
    ],
)
class TestPubSubTopicNameInvalid:
    def test_pydantic_rejects(self, value: str) -> None:
        with pytest.raises(ValidationError):
            PSModel(topic=value)


def test_pubsub_topic_name_serialization() -> None:
    m = PSModel(topic="projects/my-project/topics/my-topic")
    assert m.model_dump()["topic"] == "projects/my-project/topics/my-topic"


def test_pubsub_topic_name_json_schema() -> None:
    schema = PSModel.model_json_schema()
    props = schema["properties"]["topic"]
    assert props["type"] == "string"
    assert props["format"] == "gcp-pubsub-topic-name"


def test_pubsub_topic_name_existing_instance() -> None:
    t = PubSubTopicName("projects/my-project/topics/my-topic")
    m = PSModel(topic=t)
    assert m.topic is t


@pytest.mark.parametrize(
    "value",
    [
        "projects/my-project/subscriptions/my-subscription",
        "projects/123456789012/subscriptions/my-subscription",
    ],
)
def test_valid_pubsub_subscription_name(value: str) -> None:
    m = SubModel(sub=value)
    assert str(m.sub) == value


def test_pubsub_subscription_name_properties() -> None:
    s = PubSubSubscriptionName("projects/my-project/subscriptions/my-subscription")
    assert s.project_id == "my-project"
    assert s.subscription_name == "my-subscription"


@pytest.mark.parametrize(
    "value",
    [
        "my-project/subscriptions/my-sub",
        "projects/ab/subscriptions/my-sub",
        "projects/my-project/subscriptions/ab",
        "projects/my-project/subscriptions/1bad",
        "projects/my-project/subscriptions/googSub",
    ],
)
def test_invalid_pubsub_subscription_name(value: str) -> None:
    with pytest.raises(ValidationError):
        SubModel(sub=value)


def test_pubsub_subscription_name_serialization() -> None:
    m = SubModel(sub="projects/my-project/subscriptions/my-subscription")
    assert m.model_dump()["sub"] == "projects/my-project/subscriptions/my-subscription"


def test_pubsub_subscription_name_json_schema() -> None:
    schema = SubModel.model_json_schema()
    props = schema["properties"]["sub"]
    assert props["type"] == "string"
    assert props["format"] == "gcp-pubsub-subscription-name"


def test_pubsub_subscription_name_existing_instance() -> None:
    s = PubSubSubscriptionName("projects/my-project/subscriptions/my-subscription")
    m = SubModel(sub=s)
    assert m.sub is s
