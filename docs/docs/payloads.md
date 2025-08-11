# Payload Reference

The system exchanges inventory information using a JSON payload with the following fields:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `item_id` | string | Unique identifier for the inventory item |
| `expiry_date` | string (ISO 8601) | Expiration date in UTC |
| `location` | string | Physical or logical location of the item |
| `device_id` | string | Identifier for the RFID reader or IoT device that captured the scan |
| `timestamp` | string (ISO 8601) | Time the scan was recorded |

## Sample Payload

```json
{
  "item_id": "ITEM_001",
  "expiry_date": "2025-03-15T12:00:00Z",
  "location": "Shelf_A1",
  "device_id": "READER_42",
  "timestamp": "2024-05-01T08:30:00Z"
}
```
iot-simulator/publish_sample.py
New
