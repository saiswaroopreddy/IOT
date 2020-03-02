import json
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    logger.info('Received event: ' + json.dumps(event))

    item = {
        'ClickType': event['deviceEvent']['buttonClicked']['clickType'],
        'ReportedTime': event['deviceEvent']['buttonClicked']['reportedTime']
    }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('iot-1-click')

    try:
        response = table.update_item(
            Key={
                'DeviceID': event['deviceInfo']['deviceId']
            },
            UpdateExpression='SET Triggers = list_append(Triggers, :item)',
            ExpressionAttributeValues={
                ':item': [item]
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ValidationException':
            response = table.put_item(
                Item={
                    'DeviceID': event['deviceInfo']['deviceId'],
                    'PlacementInfo': event['placementInfo'],
                    'Triggers': [item]
                }
            )
        else:
            raise e

    return response
