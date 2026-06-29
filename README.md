# RFID Inventory Management System — AWS

## The Business Problem

Pick n Pay's 40+ retail branches were running on manual barcode scanning — staff with handheld scanners, periodic stock counts, nightly batch syncs to SAP. The system couldn't distinguish whether an item was on the shelf, in the storeroom, or in transit. Stockouts weren't detected until a shelf was already empty and a customer complained.

**The measurable cost:**
- 8–12% of SKUs out of stock at any point in the day
- 2 full staff shifts per week per branch spent on manual stock counts — non-value-adding labour
- Emergency restocking orders at premium cost when stockouts cascaded

**The ask:** Track every item in real time from goods-in to point-of-sale. Alert staff before a stockout happens, not after. Sync to SAP automatically.

## Results

| Metric | Before | After |
|---|---|---|
| Stockout rate | 8–12% of SKUs | Reduced by 20–22% |
| Sales uplift | Baseline | ~10% increase from improved availability |
| Processing latency | 350–500ms (batch) | <200ms real-time |
| Message throughput | ~500 msg/s | ~950 msg/s |
| Forecast accuracy | 75–80% | ~92% at peak |
| ROI payback period | — | 12–14 months |

*Business outcomes (stockout reduction, sales uplift, forecast accuracy) are from the Pick n Pay branch deployment. Throughput and latency (~950 msg/s, <200ms) were validated using the included iot-simulator under synthetic load.*

## Architecture

```
RFID Readers → AWS IoT Core (MQTT: rfid/scan)
                      ↓ IoT Rules Engine
               Lambda (process_scan)
                      ↓              ↓              ↓
               DynamoDB        SAP AII (IDoc)   SNS (low-stock alert)
                      ↓
               QuickSight (analytics)  +  CloudWatch (monitoring)
```

**Why IoT Core over Kinesis? Why DynamoDB over RDS? Why Lambda over EC2?** Full service selection reasoning is in [DECISION_RECORD.md](./DECISION_RECORD.md).

## AWS Services & Why Each Was Chosen

| Service | Role | Why chosen |
|---|---|---|
| AWS IoT Core | RFID message ingestion (MQTT) | Device management + MQTT native — Kinesis doesn't manage device auth |
| IoT Rules Engine | Message routing + SQL filtering | Routes to targets without invoking Lambda for every message |
| AWS Lambda | Scan event processing | Event-driven, scales to zero — no polling loops, no idle compute |
| Amazon DynamoDB | Inventory state store | Sub-10ms reads; key-value pattern; auto-scales at peak |
| Amazon SNS | Low-stock alerts | Decouples notification logic — add channels (SMS, Slack) without touching Lambda |
| Amazon QuickSight | Analytics dashboards | Native AWS integration; shows top-selling SKUs, expiry tracking, scan trends |
| Amazon CloudWatch | Monitoring and alerting | End-to-end latency, Lambda error rate, MQTT subscription success |
| SAP AII (IDoc) | ERP integration | Standard SAP interface — SAP business rules still execute correctly |

## POPIA & Compliance

- **ICASA:** All RFID hardware operates in certified frequency bands (ZAR 15k–30k certification cost)
- **NRCS:** Hardware safety testing complete (ZAR 90k–360k)
- **POPIA:** AES-256 encryption for any customer-linked data; IAM least privilege; CloudTrail audit logs; no raw PII in Lambda logs

## Sample RFID Scan Event

```json
{
  "item_id": "ITEM_001",
  "expiry_date": "2025-03-15T12:00:00Z",
  "location": "Shelf_A1",
  "device_id": "READER_42",
  "timestamp": "2024-05-01T08:30:00Z"
}
```

## Monthly Cloud Cost (~$2,500/month at 950 msg/sec)

The biggest driver is DynamoDB write volume (~$1,500/month at this message rate). IoT Core messaging is ~$960/month. Lambda is almost noise by comparison. Against the stockout-reduction value, cloud ROI payback is 12–14 months total. Full cost model in [DECISION_RECORD.md](./DECISION_RECORD.md).

## Visual Evidence (Figures 1–13)

- **Figure 1:** Full system architecture (RFID → IoT Core → Lambda → DynamoDB → SAP)
- **Figure 2:** AWS IoT Core and Lambda data pipeline
- **Figure 3:** Lambda → SAP AII IDoc integration workflow
-  **Figure 4:** CloudWatch RFID-IoT-Monitoring dashboard — MQTT protocol operations, message processing, and rule execution
- **Figure 5:** CloudWatch metrics dashboard (IoT throughput, Lambda latency, DynamoDB)
- **Figure 6:** DynamoDB table schema with item_id, expiry, SAP integration fields
- **Figure 7:** IoT Core Rule setup (SQL routing to Lambda)
- **Figure 8:** QuickSight analytics — top-selling SKUs, expiry tracking, scan trends
- **Figures 9–13:** CloudWatch event logs, MQTT subscription confirmation, latency evidence

## What I'd Change at 10× Scale

At 400 branches and 9,500 msg/sec, DynamoDB costs alone reach ~$15,000/month. The fix: provisioned DynamoDB capacity with DAX (write-through cache to coalesce rapid duplicate scans), route high-volume branches to Kinesis Data Streams instead of IoT Core message-by-message pricing, and add Lambda-level deduplication within 5-second windows. Full analysis in [DECISION_RECORD.md](./DECISION_RECORD.md).

## Repository Structure

```
rfid-inventory-management/
├── lambda/           # process_scan.py, sap_integration.py
├── iot-simulator/    # Simulates RFID scan events at load
├── infra/            # CloudFormation template
├── compliance/       # POPIA, ICASA documentation
├── docs/             # Architecture diagrams, reports
├── quicksight/       # Dashboard definitions
├── tests/            # Unit tests (pytest)
├── DECISION_RECORD.md
└── README.md
```

## Contact

**Joshua Barradas** | [LinkedIn](https://www.linkedin.com/in/joshua-barradas-433292212/) | Leeds, UK
