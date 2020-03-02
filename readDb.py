from dateutil import tz
from dateutil import parser
import boto3
import pandas as pd


def get_table():
    dynamodb = boto3.resource('dynamodb')

    return dynamodb.Table('iot-1-click')


def get_triggers(table, key):
    response = table.get_item(
        Key={
            'DeviceID': key
        }
    )
    triggers = response['Item']['Triggers']

    return pd.DataFrame.from_dict(triggers)


def to_local(timestamp):
    utc = parser.parse(timestamp)

    return utc.astimezone(tz.tzlocal())


def to_minute_res(timestamp):

    return timestamp.floor('min')


if __name__ == "__main__":

    table = get_table()
    # Get triggers using device ID of button
    triggers = get_triggers(table, 'G030PM045103HXCC')
    triggers['Timestamp'] = triggers.iloc[:, 1].apply(
        to_local).apply(to_minute_res)



