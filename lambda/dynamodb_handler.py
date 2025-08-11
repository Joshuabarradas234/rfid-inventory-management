"""Lambda function to persist RFID scan events to DynamoDB."""

import os
from datetime import datetime
from typing import Any, Dict

import boto3

TABLE_NAME = os.environ.get("TABLE_NAME", "Inventory")
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
