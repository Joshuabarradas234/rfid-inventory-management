RFID-Based Inventory Management System (AWS-Centric)

[![CI](https://github.com/OWNER/rfid-inventory-management/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/rfid-inventory-management/actions/workflows/ci.yml)
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
* [Repository Structure](#repository-structure)
* [Setup](#setup)
* [Running Tests](#running-tests)
* [📊 Visual Architecture & Monitoring](#-visual-architecture--monitoring)
* [Contact](#contact)

## Summary

This project implements a real-time inventory management system using RFID, IoT, and AWS cloud services to address challenges in the South African retail supply chain (Pick n Pay branches). It improves inventory accuracy, reduces stockouts, and meets local compliance regulations such as ICASA, NRCS, and POPIA.

## Architecture Diagram

**Figure 1:** RFID Inventory System Architecture (AWS-based). Shows flow of data from RFID devices through AWS IoT Core, AWS Lambda, DynamoDB, and SAP.
![RFID Inventory System Architecture](https://github.com/Joshuabarradas234/rfid-inventory-management/blob/main/Figure%201.png?raw=true)
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

### CloudFormation Deployment

Build the Lambda package and deploy the core infrastructure:

```bash
Package the Lambda code
zip -j process_scan.zip lambda/process_scan/*
aws s3 cp process_scan.zip s3://<your-bucket>/

# Deploy the stack
aws cloudformation deploy \
  --template-file infra/template.yaml \
  --stack-name rfid-infra \
 --capabilities CAPABILITY_IAM \
  --parameter-overrides LambdaS3Bucket=<your-bucket>
```

To remove the stack when finished:

```bash
aws cloudformation delete-stack --stack-name rfid-infra
```
## Sample Payload (JSON)

```json
{
  "item_id": "ITEM_001",
  "expiry_date": "2025-03-15T12:00:00Z",
 "location": "Shelf_A1",
  "device_id": "READER_42",
  "timestamp": "2024-05-01T08:30:00Z"
}
```
See [docs/payloads.md](docs/payloads.md) for field descriptions.

## Lambda Function Snippets

### DynamoDB PutItem Lambda (Python)

```python
def lambda_handler(event, context):
    import boto3
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Inventory')
    try:
       item_id = event.get('item_id')
        expiry_date = event.get('expiry_date')
        location = event.get('location')
        device_id = event['device_id']
        timestamp = event['timestamp']
        if not all([item_id, expiry_date, location]):
            raise ValueError("Missing required fields in event")
        table.put_item(Item={
            'item_id': item_id,
            'expiry_date': expiry_date,
            'location': location,
            'device_id': device_id,
            'timestamp': timestamp
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

## Repository Structure

```
rfid-inventory-management/
├── docs/            # Diagrams, reports, figures
├── lambda/          # Lambda function code
├── iot-simulator/   # Simulation scripts
├── quicksight/      # Dashboard definitions
├── compliance/      # POPIA, ICASA docs
├── tests/           # Unit tests
├── requirements.txt # Python dependencies
└── README.md        # Project README
```

## Setup

Install the runtime dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Settings are read from environment variables or an optional `config.json` file at the repository root.
Environment variables take precedence over file values. Defaults are used when neither source is
provided.

| Name | Default | Description |
| --- | --- | --- |
| `TABLE_NAME` | `Inventory` | DynamoDB table used by the Lambda function. |
| `IOT_TOPIC` | `rfid/scan` | MQTT topic for the IoT simulator publisher. |

Example `config.json`:

```json
{
  "TABLE_NAME": "Inventory",
  "IOT_TOPIC": "rfid/scan"
}
```


For development and testing, install the additional dependencies:

```bash
pip install -r requirements.txt -r requirements-dev.txt
```
## Running Tests

Unit tests are implemented with [pytest](https://pytest.org). After installing the development dependencies, run:
```
pytest
```

The suite covers the Lambda DynamoDB handler and the IoT simulator sample publisher.

## 📊 Visual Architecture & Monitoring

**Figure 1: RFID Inventory System Architecture (AWS-based)**  
Shows data flow from RFID tags to IoT Core, Lambda, DynamoDB, and SAP.  
![Figure 1](https://github.com/Joshuabarradas234/rfid-inventory-management/blob/main/Figure%201.png?raw=true)

**Figure 2: AWS IoT Core and Lambda Data Pipeline**  
Visualizes how MQTT messages from RFID readers are routed to Lambda.  
![Figure 2](https://github.com/Joshuabarradas234/rfid-inventory-management/blob/main/Figure%202.png?raw=true)

**Figure 3: AWS to SAP AII Integration Workflow**  
Shows how processed inventory data flows from AWS to SAP Auto-ID Infrastructure (AII) by converting IoT events into SAP IDocs and sending them via OData.  
![Figure 3](https://github.com/Joshuabarradas234/rfid-inventory-management/blob/main/Figure%203.png?raw=true)

**Figure 4: Scalability and Failover Testing Setup**  
Illustrates the test environment with simulated RFID devices, load testing tools, and monitoring components.  
![Figure 4](https://github.com/Joshuabarradas234/rfid-inventory-management/blob/main/Figure%204.png?raw=true)

**Figure 5: CloudWatch Metrics Dashboard**  
Displays real-time IoT throughput, Lambda invocations, DynamoDB usage, and API latency.  
![Figure 5](https://github.com/Joshuabarradas234/rfid-inventory-management/blob/main/Figure%205.png?raw=true)

**Figure 6: DynamoDB Table Schema View**  
Shows how inventory data is structured with item_id, expiry_date, and SAP integration fields.  
![Figure 6](https://github.com/Joshuabarradas234/rfid-inventory-management/blob/main/Figure%206.png?raw=true)


**Figure 7: IoT Core Rule Setup**  
Highlights the SQL-based IoT rule that routes scans to Lambda.  
![Figure 7](https://github.com/Joshuabarradas234/rfid-inventory-management/blob/main/Figure%207.png?raw=true)

**Figure 8: QuickSight Analytics Dashboard**  
Displays top-selling SKUs, items near expiry, and scan trends.  
![Figure 8](https://github.com/Joshuabarradas234/rfid-inventory-management/blob/main/Figure%208.png?raw=true)

**Figure 9: CloudWatch – Event Logs Summary**  
Confirms real-time ingestion and minimal latency.  
![Figure 9](https://github.com/Joshuabarradas234/rfid-inventory-management/blob/main/Figure%209.png?raw=true)

**Figure 10: CloudWatch – MQTT Subscriptions**  
Tracks successful MQTT event delivery to Lambda.  
![Figure 10](https://github.com/Joshuabarradas234/rfid-inventory-management/blob/main/Figure%2010.png?raw=true)

**Figure 11: CloudWatch – Detailed Metrics (06:35 UTC)**  
Shows burst load with ~0.979s latency and Lambda/SNS alerts.  
![Figure 11](https://github.com/Joshuabarradas234/rfid-inventory-management/blob/main/Figure%2011.png?raw=true)

**Figure 12: CloudWatch – TopicMatch Execution (06:40 UTC)**  
AWS IoT rule triggers Lambda in real time.  
![Figure 12](https://github.com/Joshuabarradas234/rfid-inventory-management/blob/main/Figure%2012.png?raw=true)

**Figure 13: CloudWatch – Protocol Success Overview (1.04s)**  
Latency confirmation for full pipeline: IoT → Lambda → DynamoDB.  
![Figure 13](https://github.com/Joshuabarradas234/rfid-inventory-management/blob/main/Figure%2013.png?raw=true)

## License
This project is licensed under the [MIT License](LICENSE).

## Contact  
For questions, feedback, or collaboration, feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/joshua-barradas-433292212/)


