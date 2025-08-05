RFID-Based Inventory Management System (AWS-Centric)

![AWS](https://img.shields.io/badge/AWS-IoT%20Core-orange?logo=amazon-aws)
![Python](https://img.shields.io/badge/Language-Python-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

## 📚 Table of Contents

* [Summary](#summary)
* [Architecture Diagram](#architecture-diagram)
* [AWS Services Used](#aws-services-used)
* [System Components Overview](#system-components-overview)
* [Key Skills Demonstrated](#key-skills-demonstrated)
* [Deployment Instructions](#deployment-instructions)
* [Sample Payload (JSON)](#sample-payload-json)
* [Lambda Function Snippets](#lambda-function-snippets)
* [CloudWatch Metrics & Monitoring](#cloudwatch-metrics--monitoring)
* [Performance Highlights](#performance-highlights)
* [Compliance & Risk Handling](#compliance--risk-handling)
* [Cost Estimates](#cost-estimates)
* [Future Enhancements](#future-enhancements)
* [Suggested Repository Structure](#suggested-repository-structure)
* [📊 Visual Architecture & Monitoring](#-visual-architecture--monitoring)
* [Contact](#contact)

## Summary

This project implements a real-time inventory management system using RFID, IoT, and AWS cloud services to address challenges in the South African retail supply chain (Pick n Pay branches). It improves inventory accuracy, reduces stockouts, and meets local compliance regulations such as ICASA, NRCS, and POPIA.

## Architecture Diagram

**Figure 1:** RFID Inventory System Architecture (AWS-based). Shows flow of data from RFID devices through AWS IoT Core, AWS Lambda, DynamoDB, and SAP.

## AWS Services Used

* **AWS IoT Core:** Handles MQTT message ingestion.
* **AWS Lambda:** Serverless compute for processing events.
* **Amazon DynamoDB:** NoSQL database storing inventory data.
* **Amazon SNS:** Notification service for alerts.
* **Amazon QuickSight:** Visualization of inventory metrics.
* **Amazon CloudWatch:** Monitors performance, latency, errors.

## System Components Overview

* **RFID Tags & Readers:** Enable non-line-of-sight inventory tracking.
* **IoT Device Simulator:** Simulates large-scale tag scans.
* **AWS IoT Core:** Ingests scans, routes via rules.
* **AWS Lambda:** Processes scans, updates DB, sends alerts.
* **Amazon DynamoDB:** Stores inventory records.
* **Amazon SNS:** Publishes notifications.
* **Amazon QuickSight:** Dashboards for insights.
* **Amazon CloudWatch:** Logs and monitors the system.
* **SAP AII Integration:** Sends updates as IDocs to SAP ERP.

## Key Skills Demonstrated

* AWS IoT Core, Lambda, DynamoDB, SNS, CloudWatch, QuickSight
* Serverless event-driven architecture
* POPIA, ICASA, NRCS compliance design
* SAP AII enterprise integration
* IoT simulation and load testing
* ROI analysis and cloud cost optimization

## Deployment Instructions

1. **IoT Core:** Configure MQTT topic `rfid/scan` to trigger Lambda.
2. **Lambda:** Deploy with IAM permissions and environment variables.
3. **DynamoDB:** Table `Inventory` with `item_id` as partition key.
4. **SNS:** Topic `InventoryAlerts`, subscribe emails/SMS.
5. **QuickSight:** Create datasets and dashboards.
6. **Monitoring:** Use CloudWatch to verify performance.

## Sample Payload (JSON)

```json
{
  "item_id": "ITEM_001",
  "expiry_date": "2025-03-15T12:00:00Z",
  "location": "Shelf_A1"
}
```

## Lambda Function Snippets

### DynamoDB PutItem Lambda (Python)

```python
def lambda_handler(event, context):
    import boto3
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Inventory')
    try:
        item_id = event['item_id']
        expiry_date = event['expiry_date']
        location = event['location']
        table.put_item(Item={
            'item_id': item_id,
            'expiry_date': expiry_date,
            'location': location
        })
        return {'statusCode': 200, 'body': 'Scan recorded'}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}
```

### SAP AII Integration Lambda (Python)

```python
def lambda_handler(event, context):
    import requests
    idoc_payload = {
        "IDOC": {
            "E1EDK01": {"ACTION": "03", "CURCY": "ZAR"},
            "E1EDP01": {
                "POSEX": "00010",
                "MATNR": event['item_id'],
                "MENGE": "1",
                "MEINS": "EA"
            }
        }
    }
    response = requests.post("https://sap.example.com/idoc", json=idoc_payload)
    return {'statusCode': response.status_code, 'body': response.text}
```

## CloudWatch Metrics & Monitoring

Metrics monitored:

* IoT throughput (RFID scans/sec)
* Lambda latency (< 200 ms)
* Error rate (< 1%)
* MQTT subscription success

Alerts are triggered if performance thresholds are breached.

## Performance Highlights

| Metric                  | AWS Implementation | Baseline (Legacy) |
| ----------------------- | ------------------ | ----------------- |
| Message Throughput      | \~950 msg/s        | \~500 msg/s       |
| Avg. Processing Latency | < 200 ms           | 350–500 ms        |
| Error Rate              | \~0.8%             | \~4%              |
| Forecast Accuracy       | \~92% (peak)       | \~75–80%          |
| ROI Payback Period      | \~12–14 months     | \~18–24 months    |

## Compliance & Risk Handling

* **ICASA:** RFID hardware certified (\~ZAR 15k–30k).
* **POPIA:** AES-256 encryption, IAM least privilege, audit logs.
* **NRCS:** Hardware safety tested (ZAR 90k–360k).

## Cost Estimates

| Item                  | Estimated Cost       | Details                          |
| --------------------- | -------------------- | -------------------------------- |
| RFID Tags (UHF)       | \$0.05–\$0.10 each   | Bulk pricing                     |
| RFID Readers          | \$1,200–\$2,500 each | Impinj, Zebra                    |
| Environmental Sensors | \$20–\$50 each       | Optional add-ons                 |
| AWS Cloud Services    | < \$100/month        | IoT Core, Lambda, DynamoDB, etc. |
| Total Implementation  | \$50k–\$200k         | Hardware, cloud, SAP integration |

## Future Enhancements

* Blockchain traceability (Amazon QLDB)
* Hybrid backup (Azure IoT Edge)
* Predictive analytics (SageMaker, Forecast)
* Mobile apps for staff scanning
* Automated SAP-triggered restocking

## Suggested Repository Structure

```
rfid-inventory-management/
├── docs/            # Diagrams, reports
├── lambda/          # Lambda function code
├── iot-simulator/   # Simulation scripts
├── quicksight/      # Dashboard definitions
├── compliance/      # POPIA, ICASA docs
└── README.md        # Project README
```

## 📊 Visual Architecture & Monitoring

### Figure 1: RFID Inventory System Architecture (AWS-based)
Shows data flow from RFID tags to IoT Core, Lambda, DynamoDB, and SAP.  
![Figure 1](Figure%201.png)

### Figure 2: AWS IoT Core and Lambda Data Pipeline
Visualizes how MQTT messages from RFID readers are routed to Lambda.  
![Figure 2](Figure%202.png)

### Figure 3: AWS to SAP AII Integration Workflow
Shows how processed inventory data flows from AWS to SAP Auto-ID Infrastructure (AII) by converting IoT events into SAP IDocs and sending them via OData.  
![Figure 3](Figure%203.png)

### Figure 4: Scalability and Failover Testing Setup
Illustrates the test environment with simulated RFID devices, load testing tools, and monitoring components used to evaluate system performance under stress.  
![Figure 4](Figure%204.png)

### Figure 5: CloudWatch Metrics Dashboard
Displays a sample Amazon CloudWatch dashboard with real-time metrics including IoT message throughput, Lambda invocations, DynamoDB capacity usage, and API latency—helping detect system bottlenecks and anomalies.  
![Figure 5](Figure%205.png)

### Figure 6: DynamoDB Table Schema View
Shows the table schema and sample entries, including primary key (item_id), secondary indexes (e.g., expiry_date), and attributes—illustrating how inventory data is structured for fast queries and SAP integration.  
![Figure 6](Figure%206.png)

### Figure 7: IoT Core Rule Setup
Displays the AWS IoT Core rule that routes rfid/scan messages to the processing Lambda. Highlights the SQL-based filter used to validate payloads before triggering the function.  
![Figure 7](Figure%207.png)

### Figure 8: QuickSight Analytics Dashboard
Visualizes inventory metrics such as items near expiry, top-selling SKUs, and scan frequency by location. Supports data-driven restocking and promotion planning.  
![Figure 8](Figure%208.png)

### Figure 9: CloudWatch Dashboard – Event Logs Summary
Highlights system event logs for IoT and Lambda operations, confirming real-time ingestion and processing with minimal latency across the full pipeline.  
![Figure 9](Figure%209.png)

### Figure 10: CloudWatch Dashboard – Subscription and Publish Events
Tracks successful MQTT subscriptions and publishes in the simulation environment, confirming reliable message delivery from devices through AWS IoT Core to Lambda.  
![Figure 10](Figure%2010.png)

### Figure 11: CloudWatch Dashboard – Detailed Metrics at 06:35 UTC
Snapshot shows a burst of activity at 06:35 UTC, with a performance metric of ~0.979 confirming sub-second processing latency and timely alert triggering via Lambda/SNS.  
![Figure 11](Figure%2011.png)

### Figure 12: CloudWatch Dashboard – TopicMatch Execution at 06:40 UTC
This view captures the AWS IoT rule (ProcessRFIDMessages) triggering the Lambda function at 06:40 UTC. It confirms real-time event processing and subsequent SNS alerting for that inventory update.  
![Figure 12](Figure%2012.png)

### Figure 13: CloudWatch Dashboard – Protocol Success Overview (1.04 Latency)
At 06:36 UTC, this CloudWatch panel shows overall protocol success and a processing latency of 1.04 seconds in the IoT → Lambda → DynamoDB pipeline, demonstrating the system’s responsiveness.  
![Figure 13](Figure%2013.png)


## Contact

For any questions, feedback, or collaboration opportunities, please connect with me on [LinkedIn](https://www.linkedin.com/in/joshua-barradas-433292212/)

