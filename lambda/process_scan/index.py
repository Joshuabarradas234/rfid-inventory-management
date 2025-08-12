"""Lambda handler for processing RFID scan events."""

import json
import logging
import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError


from botocore.exceptions import BotoCoreError, ClientError
dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def handler(event, context):
    """Persist the scan event and publish an alert."""
    item = json.loads(event["body"]) if "body" in event else event
    try:
        table.put_item(Item=item)
        sns.publish(
            TopicArn=os.environ["ALERT_TOPIC_ARN"],
            Message=json.dumps(item),
        )
    except (BotoCoreError, ClientError) as exc:
        message = (
            "Failed to persist scan or publish alert: "
            f"{exc}"
        )
        logger.exception(message)
        return {"statusCode": 500, "body": message}
    return {"statusCode": 200, "body": "ok"}
