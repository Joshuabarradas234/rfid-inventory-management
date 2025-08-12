import json
import importlib.util
from pathlib import Path
import sys
import types

import pytest

sys.modules["boto3"] = types.SimpleNamespace(client=lambda service: None)

spec = importlib.util.spec_from_file_location(
    "publish_sample",
    Path(__file__).resolve().parents[1] / "iot-simulator" / "publish_sample.py",
)
publish_sample = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publish_sample)


def test_build_payload_structure():
    payload = publish_sample.build_payload()
    assert {
        "item_id",
        "expiry_date",
        "location",
        "device_id",
        "timestamp",
    } <= payload.keys()
    assert payload["item_id"].startswith("ITEM_")
    assert payload["timestamp"].endswith("Z")


def test_main_success(monkeypatch, capsys):
    published = {}

    class DummyClient:
        def publish(self, topic, qos, payload):  # noqa: D401
            published["topic"] = topic
            published["payload"] = payload

    def fake_client(service):
        return DummyClient()

    monkeypatch.setattr(publish_sample.boto3, "client", fake_client)
    publish_sample.main()
    assert published["topic"] == publish_sample.IOT_TOPIC
    assert set(json.loads(published["payload"]).keys()) >= {
        "item_id",
        "expiry_date",
        "location",
        "device_id",
        "timestamp",
    }
    assert "Published payload" in capsys.readouterr().out


def test_main_publish_failure(monkeypatch):
    class DummyClient:
        def publish(self, topic, qos, payload):
            raise RuntimeError("network error")

    def fake_client(service):
        return DummyClient()

    monkeypatch.setattr(publish_sample.boto3, "client", fake_client)
    with pytest.raises(RuntimeError):
        publish_sample.main()

def test_main_uses_env_topic(monkeypatch):
    published = {}

    class DummyClient:
        def publish(self, topic, qos, payload):
            published["topic"] = topic

    def fake_client(service):
        return DummyClient()

    monkeypatch.setattr(publish_sample.boto3, "client", fake_client)
    monkeypatch.setenv("IOT_TOPIC", "custom/topic")
    publish_sample.main()
    assert published["topic"] == "custom/topic"
