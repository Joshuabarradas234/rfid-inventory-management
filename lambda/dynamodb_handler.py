"""Lambda function to persist RFID scan events to DynamoDB."""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import boto3
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
table = None


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Validate required fields and store the scan event."""
   for field in REQUIRED_FIELDS:
        if field not in event:
            message = f"Missing required field: {field}"
            logger.warning(message)
            return {"statusCode": 400, "body": message}

        # Validate timestamp format
    try:
        datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
 except ValueError as exc:
        logger.warning("Timestamp validation failed: %s", exc)
        return {"statusCode": 400, "body": str(exc)}

    item = {field: event[field] for field in REQUIRED_FIELDS}
        global table
    if table is None:
        try:
            dynamodb = boto3.resource("dynamodb")
            table = dynamodb.Table(TABLE_NAME)
        except (BotoCoreError, ClientError) as exc:
            logger.error("Failed to access DynamoDB table: %s", exc)
            return {"statusCode": 500, "body": "Error accessing database"}

    try:   
        table.put_item(Item=item)
         logger.info("Successfully stored item %s", item["item_id"])
        return {"statusCode": 200, "body": "Scan recorded"}
    except (BotoCoreError, ClientError) as exc:
        logger.error("DynamoDB put_item failed: %s", exc)
        return {"statusCode": 500, "body": "Error writing to database"}
    except Exception as exc:  # pragma: no cover - fallback
        logger.exception("Unexpected error writing to DynamoDB")
        return {"statusCode": 500, "body": str(exc)}
