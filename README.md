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

![Figure 1](Figure%201.png)

### Figure 2A: AWS IoT Core and Lambda Data Pipeline

![Figure 2](Figure%202.png)

### Figure 3A: AWS to SAP AII Integration Workflow

![Figure 3](Figure%203.png)

### Figure 4A: Scalability and Failover Testing Setup

![Figure 4](Figure%204.png)

### Figure 5A: CloudWatch Metrics Dashboard

![Figure 5](Figure%205.png)

### Figure 6A: DynamoDB Table Schema View

![Figure 6](Figure%206.png)

### Figure 7A: IoT Core Rule Setup

![Figure 7](Figure%207.png)

### Figure 8A: QuickSight Analytics Dashboard

![Figure 8](Figure%208.png)

### Figure 9A: CloudWatch – Event Logs Summary

![Figure 9](Figure%209.png)

### Figure 10A: CloudWatch – Subscription and Publish Events

![Figure 10](Figure%2010.png)

### Figure 11A: CloudWatch – Detailed Metrics at 06:35 UTC

![Figure 11](Figure%2011.png)

### Figure 12A: CloudWatch – TopicMatch Execution at 06:40 UTC

![Figure 12](Figure%2012.png)

### Figure 13A: CloudWatch – Protocol Success (1.04s Latency)

![Figure 13](Figure%2013.png)

## Contact

For any questions, feedback, or collaboration opportunities, please connect with me on [LinkedIn](https://www.linkedin.com/in/joshua-barradas-433292212/)

