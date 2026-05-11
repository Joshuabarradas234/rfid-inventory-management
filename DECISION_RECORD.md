# Decision Record — RFID Inventory Management System

**Project:** Real-Time RFID Inventory Management on AWS  
**Customer:** Pick n Pay — South African major retail group (40+ branches)  
**Author:** Joshua Barradas  
**Date:** May 2026  

---

## 1. Customer & Context

### Who is the customer?
Pick n Pay is one of South Africa's largest retail chains, with 40+ branches. Their inventory management relied on manual barcode scanning — staff walking the aisles with handheld scanners, periodic stock counts, and a nightly batch sync to SAP ERP. This process was slow, error-prone, and couldn't detect stockouts until a shelf was already empty.

### What business problem are they solving?
Stockouts were costing the business in two ways: lost sales at the shelf, and emergency restocking orders at premium cost. The barcode-based system couldn't tell them whether an item was on the shelf, in the storeroom, or in transit — only that it had been scanned at some point. When an item went missing or depleted, they found out from customer complaints, not from their system.

**The measurable problem:**
- Stockout rate: ~8–12% of SKUs out of stock at any point in the day
- Each stockout = lost sale + customer frustration + potential brand switch
- Manual stock counts: 2 full staff shifts per week per branch, entirely non-value-adding labour

**The ask:** Track every item in real time from goods-in to point-of-sale. Alert staff before a stockout happens, not after. Sync to SAP without manual intervention.

### What constraints are they operating under?
- **Latency:** Inventory state must update within seconds of an RFID scan — retail operations staff need live shelf views, not hourly batches.
- **Reliability:** Always-on retail. 24/7 availability required. System failure = blind inventory = stockouts cascade.
- **Compliance:** POPIA (South Africa's data protection law) for any customer-linked data. ICASA certification required for RFID hardware operating in South Africa's radio frequency bands. NRCS certification for hardware safety.
- **Scale:** ~950 messages/second at peak (weekend rush across all branches). Must handle burst without degradation.
- **Integration:** SAP AII (Auto-ID Infrastructure) integration is mandatory — Pick n Pay's ERP is SAP, and all inventory movements must flow as IDocs.
- **Cost:** Hardware investment ($50k–$200k total implementation) is large; ongoing cloud costs must be demonstrably justified by ROI.

---

## 2. Candidate Architectures

### Option A — AWS IoT Core + Lambda + DynamoDB + SNS + QuickSight *(chosen)*
Fully managed, serverless AWS stack. RFID readers publish MQTT messages to IoT Core. IoT Rules engine routes scans to Lambda. Lambda processes events, updates DynamoDB, and pushes IDocs to SAP AII. SNS sends alerts for low-stock events. QuickSight provides analytics dashboards.

### Option B — AWS Kinesis Data Streams + Lambda + DynamoDB
Replace IoT Core with Kinesis for higher throughput ingestion. Kinesis handles up to 1,000 records/second per shard and provides replay capability (retain messages for 7–365 days). More appropriate for pure data streaming without device management.

### Option C — On-premises message broker (RabbitMQ/ActiveMQ) + AWS batch processing
Process RFID scans on-premises using an existing message broker, batch the results, and upload to AWS every 5 minutes for reporting. Avoids real-time cloud dependency.

---

## 3. Chosen Design

**RFID Readers → AWS IoT Core (MQTT) → IoT Rules → Lambda → DynamoDB + SNS + SAP AII**

```
RFID Readers → AWS IoT Core (MQTT topic: rfid/scan)
                      ↓ (IoT Rule: SQL filter)
               Lambda (process_scan)
                      ↓              ↓              ↓
               DynamoDB        SAP AII (IDoc)   SNS (low-stock alert)
                      ↓
               QuickSight (analytics dashboard)
               CloudWatch (monitoring)
```

---

## 4. Why I Chose Each AWS Service (Design Reasoning)

### AWS IoT Core over Kinesis Data Streams
The key question: is this a device management problem or a pure data streaming problem?

RFID readers are IoT devices — they need device authentication (X.509 certificates), device policy enforcement, connection state management, and MQTT protocol support. IoT Core provides all of this natively. Kinesis doesn't manage devices — it's a pure data stream. You'd need to build device auth and MQTT handling separately in front of Kinesis.

Kinesis is the right choice if you're receiving millions of events/second from a known set of producers (e.g., application servers). For hundreds of RFID readers across branches, each needing device identity and MQTT support, IoT Core is the right abstraction. The trade-off: IoT Core has per-message pricing whereas Kinesis uses shard-based pricing (which can be cheaper at very high volume). At ~950 msg/sec, IoT Core pricing was within budget.

### IoT Rules Engine over custom Lambda routing
The IoT Rules Engine processes SQL-like filters on incoming MQTT messages and routes them to targets (Lambda, DynamoDB direct, SNS, S3) without invoking Lambda for every message. For simple routing logic (if topic = 'rfid/scan', trigger Lambda; if error_code != null, alert SNS), the Rules Engine handles this at IoT layer — cheaper and faster than passing everything through Lambda first.

### Lambda over EC2/ECS for scan processing
Each RFID scan is an independent event: read → validate → write to DynamoDB → check stock threshold → optionally alert. There's no shared state between scans. Lambda's event-driven model is a natural fit. An EC2 instance would need a polling loop, auto-scaling configuration, and instance management. Lambda scales automatically from 0 to thousands of concurrent invocations with no configuration. At 950 msg/sec peak, Lambda can handle this comfortably with concurrency limits set appropriately.

### DynamoDB over RDS (PostgreSQL) for inventory data
Inventory events are key-value: item_id → {location, quantity, last_seen, expiry_date}. The access pattern is: write a scan event, read current state by item_id. No complex joins. DynamoDB's single-digit millisecond response time is important — Lambda needs to update DynamoDB and check stock levels within the scan processing budget to maintain <200ms end-to-end latency. RDS would add connection management overhead and latency. DynamoDB also scales automatically — no instance sizing or connection pool tuning required.

### SNS over direct Lambda-to-email notifications
SNS decouples the notification logic from the scan processing Lambda. The scan Lambda publishes to an SNS topic. SNS fans out to email, SMS, or a Slack webhook — whatever ClearPath's operations team uses. If they want to add a new notification channel later, they subscribe to the existing topic without touching the Lambda code. A direct Lambda-to-email approach tightly couples notification logic into scan processing — if the email service is slow or fails, it holds up the scan acknowledgement.

### QuickSight over custom dashboards (Power BI, Tableau)
QuickSight integrates natively with DynamoDB and S3. For a retail ops team that doesn't have Tableau licenses or Power BI infrastructure, a managed AWS-native dashboard is the lowest-friction path to "show me which SKUs are trending toward stockout." The trade-off: QuickSight's visualisation options are less rich than Tableau. For basic inventory analytics (stock levels, scan rates, expiry tracking), it's sufficient.

### SAP AII integration via Lambda + IDoc over direct database write
SAP integration is mandatory — inventory movements must appear in SAP ERP. The options were: write directly to SAP database tables (risky, unsupported, bypasses SAP business logic), use SAP's standard IDoc interface (the correct approach), or use an integration middleware (expensive). Lambda generates IDocs and posts them to SAP's OData endpoint — this is the supported SAP integration pattern. It uses SAP's own interface, which means business rules and validation in SAP still execute correctly.

---

## 5. Trade-off Scorecard

| Dimension | Option A: IoT Core (chosen) | Option B: Kinesis | Option C: On-premises |
|---|---|---|---|
| **Device management** | Native ✅ | Manual ❌ | Manual ❌ |
| **Real-time updates** | Yes (<200ms) ✅ | Yes ✅ | No (5-min batches) ❌ |
| **Cost at 950 msg/sec** | Moderate | Lower at very high volume | Low cloud cost (high infra cost) |
| **Reliability (always-on retail)** | High (managed service) ✅ | High ✅ | Risk of on-prem failure ⚠️ |
| **POPIA compliance** | AWS eu-south-1 compliant ✅ | ✅ | Higher risk (on-prem controls) ⚠️ |
| **SAP integration** | Lambda → IDoc ✅ | Lambda → IDoc ✅ | Complex ❌ |
| **Ops burden** | Low ✅ | Medium ⚠️ | High ❌ |

---

## 6. Cost Model

**Assumptions:** 950 messages/second peak, 12 hours/day retail operation, 30 days/month.

| Service | Unit cost | Volume | Monthly cost |
|---|---|---|---|
| IoT Core (messages) | $0.08 / 100k messages | ~1.2B messages/month at peak | ~$960 |
| IoT Core (connections) | $0.042 / device/month | 200 RFID readers | $8 |
| Lambda | $0.0000166667/GB-s | ~50M invocations × 200ms × 256MB | $40 |
| DynamoDB (on-demand) | $1.25/million writes | ~1.2B writes/month | $1,500 |
| SNS (alerts) | $0.50/million publishes | ~10k alerts/month | <$1 |
| QuickSight | $9/user/month | 5 ops users | $45 |
| CloudWatch | ~flat | — | $20 |
| **Cloud total** | | | **~$2,574/month (~£2,000)** |

**Hardware (one-time):** RFID tags ($0.05–$0.10 each at bulk), readers ($1,200–$2,500 each). Total implementation: $50k–$200k depending on branch count and tag volume.

**Top 3 cloud cost drivers:**
1. **DynamoDB write volume** (~$1,500/month) — 950 msg/sec × 12hrs × 30 days generates enormous write volume
2. **IoT Core message ingestion** (~$960/month) — per-message pricing at this scale
3. **Lambda compute** (~$40/month) — almost noise by comparison

**ROI:** At ~$2,000/month cloud cost against stockout reduction of 20–22% (stockouts were costing significantly more than this in lost sales), ROI payback is 12–14 months on total implementation cost.

---

## 7. At 10× Scale (40 branches → 400 branches, 9,500 msg/sec)

**What breaks first:** DynamoDB cost reaches ~$15,000/month at 10× write volume. IoT Core messaging costs reach ~$9,600/month. Together this is ~$25,000/month — still potentially justified by scale, but the write pattern needs optimisation.

**What I'd change at 10× scale:**

1. **DynamoDB: switch from on-demand to provisioned capacity + DAX.** At predictable high volume, provisioned capacity with auto-scaling is 50–70% cheaper than on-demand. Add DynamoDB Accelerator (DAX) as a write-through cache to reduce DynamoDB write operations by coalescing rapid-succession scans of the same item.

2. **IoT Core → Kinesis Data Streams for high-volume branches.** At 400 branches with 9,500 msg/sec, the per-message IoT Core pricing becomes expensive compared to Kinesis shard pricing. High-volume branches would publish to a Kinesis stream; IoT Core remains for device management, but routes high-volume message paths to Kinesis for cost efficiency.

3. **RFID scan deduplication at Lambda.** At scale, the same item gets scanned multiple times per second by multiple readers. Lambda should deduplicate within a 5-second window before writing to DynamoDB, reducing write volume significantly.

4. **QuickSight → Amazon Managed Grafana or custom dashboard.** At 400 branches with complex analytics needs, QuickSight's per-user pricing and limited customisation becomes a constraint. Managed Grafana with a DynamoDB data source offers richer dashboards with more flexible pricing.
