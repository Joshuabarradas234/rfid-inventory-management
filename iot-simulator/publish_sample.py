
import json
import random
from datetime import datetime

import boto3

IOT TOPIC = "rfid/scan"


def build payload() -> dict:
return {
"item_id": f"ITEM_{random. randint (1, 999): 03d}",
"expiry_date": "2025-03-15T12:00:00z"
"location":
"Shelf_A1"
"device id":
"READER 42"
"timestamp": datetime.utcnow().replace(microsecond=0). isoformat()  +
"z",
}


def main()
-> None:
client = boto3.client ("iot-data")
payload = build_payload()
client.publish(topic=I0T_TOPIC, qos=1, payload=json. dumps (payload) )
print ("Published payload:", payload)
if__name__=="__main__":
main()
