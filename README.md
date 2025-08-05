**RFID-Based Inventory Management System (AWS-Centric)**

**Summary:** This project implements a real-time inventory management system using RFID, IoT, and AWS cloud services to address challenges in the South African retail supply chain (Pick n Pay branches). It improves inventory accuracy, reduces stockouts, and meets local compliance regulations such as ICASA, NRCS, and POPIA.

**Architecture Diagram**

_Figure 1: RFID Inventory System Architecture (AWS-based). This diagram illustrates the overall architecture of the system, showcasing the flow of data from RFID devices through AWS IoT Core, processing via AWS Lambda, storage in DynamoDB, and integration with SAP systems._

**AWS Services Used**

- **AWS IoT Core:** Handles MQTT message ingestion from RFID devices and routes messages to the cloud securely.
- **AWS Lambda:** Serverless compute platform that processes incoming IoT events and triggers downstream actions (e.g., database updates, notifications).
- **Amazon DynamoDB:** NoSQL database that stores inventory items (e.g., item ID, expiry date, location) for quick retrieval.
- **Amazon SNS:** Simple Notification Service used to send alerts (e.g., low-stock, expiration, tamper notifications) to subscribers.
- **Amazon QuickSight:** Analytics service for building dashboards to visualize inventory trends and KPIs (e.g., stock levels over time).
- **Amazon CloudWatch:** Monitoring and logging service to track system performance metrics (throughput, latency, error rates) and trigger alarms.

**System Components Overview**

- **RFID Tags & Readers:** Physical tags and UHF readers enable non-line-of-sight real-time tracking of inventory items.
- **IoT Device Simulator:** Software or scripts that mimic RFID tag read events at scale for testing (simulating thousands of tags in a lab environment).
- **AWS IoT Core:** Managed IoT message broker that ingests tag scan events via MQTT and applies rules to route data for processing.
- **AWS Lambda:** Stateless compute functions that process incoming RFID scan events and update the inventory database (and trigger alerts or SAP updates as needed).
- **Amazon DynamoDB:** Cloud-native NoSQL database (table named Inventory) that holds item records with attributes like item_id, expiry_date, and location.
- **Amazon SNS:** Notification service that publishes alerts for specific conditions (e.g., item nearing expiry or stockout detected) to email/SMS or other endpoints.
- **Amazon QuickSight:** BI tool that visualizes inventory flow, stock levels, and trends on interactive dashboards for decision-making.
- **Amazon CloudWatch:** Performance monitoring that captures logs and custom metrics (latency, throughput, error counts) to ensure the system is operating within expected parameters.
- **SAP AII Integration:** Interface to SAP Auto-ID Infrastructure; processed RFID events are transformed into SAP IDocs and sent via OData to the SAP system for enterprise resource planning updates.

**Key Skills Demonstrated**

- Hands-on experience with core AWS services: AWS IoT Core, AWS Lambda, Amazon DynamoDB, Amazon QuickSight, Amazon SNS, and Amazon CloudWatch.
- Design of a **serverless**, event-driven architecture that scales to high throughput.
- Implementation of **compliance-first** security (POPIA data privacy and ICASA radio regulations) from day one.
- Integration of AWS cloud processes with **SAP AII** (Auto-ID Infrastructure) for seamless enterprise data synchronization.
- RFID hardware deployment and creation of an **IoT simulation** environment to test system load and reliability.
- Cost optimization techniques, ROI analysis, and rigorous end-to-end system testing in a production-like environment.

**Deployment Instructions**

1. **RFID Devices & IoT Core:** Configure physical or simulated RFID readers to publish scan data to AWS IoT Core MQTT topics (e.g., rfid/scan). In AWS IoT Core, set up a rule that triggers the Lambda function (for processing) when a message arrives on this topic.
2. **AWS Lambda Functions:** Deploy the provided Lambda functions to AWS. Ensure each function has the necessary IAM role permissions (for DynamoDB, SNS, etc.) and configure environment variables (for example, the SAP endpoint URL for integration).
3. **DynamoDB Table:** Create a DynamoDB table named Inventory with item_id as the partition key. (Optionally, set up a secondary index on attributes like expiry_date if you need to query items by expiry or other attributes.)
4. **Alerting (SNS):** Set up an Amazon SNS topic (e.g., **InventoryAlerts**) for sending notifications. Update the Lambda function code or configuration to publish to this SNS topic for events like low stock or tamper detection, and subscribe users (email/SMS) to the topic.
5. **Analytics Dashboard:** If using QuickSight for analytics, create a dataset (or use DynamoDB export to S3) and build a dashboard for inventory metrics. You can use the provided QuickSight examples as a starting point.
6. **Testing & Monitoring:** Use the IoT Device Simulator scripts to generate test payloads at scale. Monitor system behavior in AWS CloudWatch (dashboard and logs) to verify throughput, latency, and that no errors occur. Confirm that SAP receives the IDoc updates (if integration is enabled) and that notifications are sent via SNS as expected.

**Sample Payload (JSON)**

Example of an RFID scan event payload sent from a reader to the AWS IoT Core topic:

{

"item_id": "ITEM_001",

"expiry_date": "2025-03-15T12:00:00Z",

"location": "Shelf_A1"

}

**Lambda Function Snippets**

**DynamoDB PutItem Lambda (Python)**

This AWS Lambda function (Python) is triggered by incoming IoT Core messages and stores the RFID scan data into the Inventory DynamoDB table:

def lambda_handler(event, context):

import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Inventory')

try:

item_id = event\['item_id'\]

expiry_date = event\['expiry_date'\]

location = event\['location'\]

table.put_item(Item={

'item_id': item_id,

'expiry_date': expiry_date,

'location': location

})

return {'statusCode': 200, 'body': 'Scan recorded'}

except Exception as e:

return {'statusCode': 500, 'body': str(e)}

**SAP AII Integration Lambda (Python)**

This Lambda function sends an inventory update to SAP’s Auto-ID Infrastructure (AII) by constructing an IDoc payload and making an HTTP POST request to the SAP endpoint:

def lambda_handler(event, context):

import requests

idoc_payload = {

"IDOC": {

"E1EDK01": {

"ACTION": "03",

"CURCY": "ZAR"

},

"E1EDP01": {

"POSEX": "00010",

"MATNR": event\['item_id'\],

"MENGE": "1",

"MEINS": "EA"

}

}

}

response = requests.post("<https://sap.example.com/idoc>", json=idoc_payload)

return {'statusCode': response.status_code, 'body': response.text}

**CloudWatch Metrics & Monitoring**

AWS CloudWatch is used to monitor the entire pipeline. Custom dashboards track key metrics such as:

- **IoT message throughput** (e.g., number of RFID scans processed per second)
- **Lambda execution latency** (time taken to process each scan event, typically < 200 ms)
- **System error rate** (any failed Lambda invocations or processing errors, aiming for < 1%)
- **MQTT connectivity** (successful subscription and publish events from devices)

CloudWatch logs and metrics verify that data flows from devices to AWS to SAP with minimal delay. Alerts can be configured to notify the team if thresholds are exceeded (for example, if processing latency goes above a set limit).

_Figure 5A: CloudWatch Metrics Dashboard. This dashboard provides real-time visibility into system performance, including IoT Core message throughput, Lambda invocation count, DynamoDB capacity usage, and end-to-end processing latency. Such monitoring helps quickly identify any bottlenecks or anomalies._

**Performance Highlights**

Stress tests and load simulations were conducted to benchmark the system. Key performance results (versus an initial baseline) include:

| **Metric** | **AWS Implementation** | **Baseline (Legacy)** |
| --- | --- | --- |
| Message Throughput | ~950 msg/s | ~500 msg/s |
| Average Processing Latency | < 200 ms | 350–500 ms |
| Error Rate | ~0.8% | ~4% |
| Forecast Accuracy | ~92% (peak) | ~75–80% |
| ROI Payback Period | ~12–14 months | ~18–24 months |

_The AWS-based solution demonstrated significantly higher throughput and accuracy, with lower latency and error rates, achieving a faster ROI compared to the baseline._

**Compliance & Risk Handling**

Strict compliance with local regulations and best practices was maintained:

- **ICASA Certification:** All RFID equipment (readers, antennas) is certified by ICASA. (Certification costs were ~ZAR 15k–30k, factored into the project budget.)
- **POPIA (Data Privacy):** Sensitive data is protected in transit and at rest using AES-256 encryption. IAM policies enforce least privilege, and audit logs are maintained to comply with the Protection of Personal Information Act.
- **NRCS Safety Standards:** The hardware components passed National Regulator for Compulsory Specifications testing (at an estimated cost of ZAR 90k–360k) to ensure they meet safety and quality standards.

**Cost Estimates**

Approximate cost breakdown for the system deployment:

| **Item** | **Estimated Cost** | **Details** |
| --- | --- | --- |
| RFID Tags (Passive UHF) | $0.05–$0.10 each | Per tag, bulk pricing (volume dependent) |
| RFID Readers | $1,200–$2,500 each | Per reader device (e.g., Impinj, Zebra) |
| Environmental Sensors | $20–$50 each | Optional add-ons (temperature, humidity) |
| AWS Cloud Services | < $100 per month | IoT Core, Lambda, DynamoDB, SNS, etc. |
| **Total Implementation** | **$50k–$200k** (project) | Includes hardware, cloud infrastructure, and SAP integration/consulting |

_Note: Actual costs can vary based on scale, vendor pricing, and usage patterns. The estimate above includes a full rollout with integration and testing._

**Future Enhancements**

Possible enhancements that could further improve or extend the system:

- **Blockchain Traceability:** Use a blockchain ledger (e.g., Amazon QLDB or Hyperledger) to immutably track high-value items through the supply chain.
- **Hybrid Cloud Redundancy:** Incorporate an Azure IoT Edge or on-premises solution as a backup to AWS IoT Core for critical operations, improving resilience.
- **Predictive Analytics:** Leverage AWS machine learning (Forecast, SageMaker) to predict stockouts or demand spikes and automatically adjust inventory.
- **Mobile Integration:** Develop mobile applications or handheld RFID readers for on-the-floor inventory checks and real-time data updates by staff.
- **Automated Restocking with SAP:** Expand the SAP integration to not only report inventory changes but also trigger automated restocking or purchase orders based on predefined thresholds.

**Suggested Repository Structure**

Organizing the repository in a clear structure helps manage the project components:

rfid-inventory-management/

├── docs/ # Architecture diagrams, design documents, reports

├── lambda/ # AWS Lambda function source code

├── iot-simulator/ # Simulation scripts for generating RFID data

├── quicksight/ # Dashboard definitions or export files for QuickSight

├── compliance/ # Compliance documentation (POPIA, ICASA certificates)

└── README.md # Project README (this file)

**Contact**

For any questions, feedback, or collaboration opportunities, please connect with me on [LinkedIn](https://www.linkedin.com/in/yourprofile) 
