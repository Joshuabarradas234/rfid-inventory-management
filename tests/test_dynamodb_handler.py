import importlib.util
from pathlib import Path
import types
import sys


class _DummyResource:
    def Table(self, name):  # noqa: D401
        return types.SimpleNamespace()

sys.modules.setdefault(
    "boto3", types.SimpleNamespace(resource=lambda service: _DummyResource())
)

spec = importlib.util.spec_from_file_location(
       "dynamodb_handler",
    Path(__file__).resolve().parents[1] / "lambda" / "dynamodb_handler.py",
)
dynamodb_handler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dynamodb_handler)


class DummyTable:
    def __init__(self):
        self.items = []

    def put_item(self, Item):  # noqa: N803
        self.items.append(Item)


def valid_event():
    return {
        "item_id": "ITEM_001",
        "expiry_date": "2025-03-15T12:00:00Z",
        "location": "Shelf_A1",
        "device_id": "READER_42",
        "timestamp": "2024-05-01T08:30:00Z",
    }


def test_lambda_handler_success(monkeypatch):
    table = DummyTable()
    monkeypatch.setattr(dynamodb_handler, "table", table)
    response = dynamodb_handler.lambda_handler(valid_event(), None)
    assert response["statusCode"] == 200
    assert table.items[0]["item_id"] == "ITEM_001"


def test_lambda_handler_missing_field(monkeypatch):
    table = DummyTable()
    monkeypatch.setattr(dynamodb_handler, "table", table)
    event = valid_event()
    del event["item_id"]
    response = dynamodb_handler.lambda_handler(event, None)
    assert response["statusCode"] == 400
    assert "Missing required field: item_id" in response["body"]


def test_lambda_handler_invalid_timestamp(monkeypatch):
    table = DummyTable()
    monkeypatch.setattr(dynamodb_handler, "table", table)
    event = valid_event()
    event["timestamp"] = "bad-timestamp"
    response = dynamodb_handler.lambda_handler(event, None)
    assert response["statusCode"] == 400
