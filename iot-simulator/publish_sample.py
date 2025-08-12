import json
import os
import logging
import random
from datetime import datetime
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


IOT_TOPIC = _get_setting("IOT_TOPIC", "rfid/scan")


def build_payload() -> dict:
    return {
        "item_id": f"ITEM_{random.randint(1, 999):03d}",
        "expiry_date": "2025-03-15T12:00:00Z",
        "location": "Shelf_A1",
        "device_id": "READER_42",
        "timestamp": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
    }


def main() -> None:
    client = boto3.client("iot-data")
    payload = build_payload()
    topic = IOT_TOPIC
    try:
        client.publish(topic=topic, qos=1, payload=json.dumps(payload))
        print("Published payload:", payload)
    except (BotoCoreError, ClientError) as exc:
        logger.error("boto3 publish failed: %s", exc)
        raise
    except Exception as exc:  # pragma: no cover - fallback
        logger.error("Unexpected error publishing payload: %s", exc)
        raise


if __name__ == "__main__":
    main()
