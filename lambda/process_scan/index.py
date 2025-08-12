"""Lambda handler for processing RFID scan events."""

import json
import os

import boto3


dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def handler(event, context):
    """Persist the scan event and publish an alert."""
    item = json.loads(event["body"]) if "body" in event else event
    table.put_item(Item=item)
    sns.publish(TopicArn=os.environ["ALERT_TOPIC_ARN"], Message=json.dumps(item))
    return {"statusCode": 200, "body": "ok"}
