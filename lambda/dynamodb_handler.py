"""Lambda function to persist RFID scan events to DynamoDB."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import boto3


def _get_setting(name: str, default: str) -> str:
    """Return configuration value from environment or config file."""
    if name in os.environ:
        return os.environ[name]
    config_path = Path(__file__).resolve().parents[1] / "config.json"
    if config_path.exists():
        try:
            with config_path.open() as f:  # pragma: no cover - file access
                data = json.load(f)
            return data.get(name, default)
        except Exception:  # pragma: no cover - optional
            pass
    return default


TABLE_NAME = _get_setting("TABLE_NAME", "Inventory")
REQUIRED_FIELDS = [
    "item_id",
    "expiry_date",
    "location",
    "device_id",
    "timestamp",
]


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Validate required fields and store the scan event."""
    try:
        for field in REQUIRED_FIELDS:
            if field not in event:
                raise KeyError(f"Missing required field: {field}")

        # Validate timestamp format
        datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))

        item = {field: event[field] for field in REQUIRED_FIELDS}
        table.put_item(Item=item)
        return {"statusCode": 200, "body": "Scan recorded"}
    except (KeyError, ValueError) as e:
        return {"statusCode": 400, "body": str(e)}
    except Exception as e:  # pragma: no cover - fallback
        return {"statusCode": 500, "body": str(e)}
