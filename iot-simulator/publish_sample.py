import json
import random
from datetime import datetime

import boto3

IOT_TOPIC = "rfid/scan"


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
    client.publish(topic=IOT_TOPIC, qos=1, payload=json.dumps(payload))
    print("Published payload:", payload)


if __name__ == "__main__":
    main()
