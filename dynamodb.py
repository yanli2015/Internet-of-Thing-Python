from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from numpy import *
import matplotlib.pyplot as pyl

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def put_data_to_DB(temperature):
    endpoint_url = "http://ec2-54-209-92-140.compute-1.amazonaws.com:8000"
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1c', endpoint_url=endpoint_url)
    table = dynamodb.Table('Temperature')
    table.put_item(
        Item=temperature
    )

def get_results_from_DB():
    endpoint_url = "http://ec2-54-209-92-140.compute-1.amazonaws.com:8000"
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1c', endpoint_url=endpoint_url)
    table = dynamodb.Table('Temperature')
    data_list = []
    response = table.scan(
        # FilterExpression=fe,
        # ProjectionExpression=pe,
        # ExpressionAttributeNames=ean
        )

    for i in response['Items']:
        data = json.dumps(i, cls=DecimalEncoder)
        data_list.append(json.loads(data))
        print(data_list[0]["TimeStamp"])
        print(data_list)

    while 'LastEvaluatedKey' in response:
        response = table.scan(
            # ProjectionExpression=pe,
            # FilterExpression=fe,
            # ExpressionAttributeNames= ean,
            ExclusiveStartKey=response['LastEvaluatedKey']
            )
        for i in response['Items']:
            data = json.dumps(i, cls=DecimalEncoder)
            data_list.append(json.loads(data))
            print(data)
    return data_list

def dynamoDB_create_table():
    endpoint_url = "http://ec2-54-209-92-140.compute-1.amazonaws.com:8000"
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1c', endpoint_url=endpoint_url)
    table = dynamodb.create_table(
        TableName='Temperature',
        KeySchema=[
            {
                'AttributeName': 'TimeStamp',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'Temperature_F',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'TimeStamp',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Temperature_F',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

def create_image():
    temp_list = get_results_from_DB()
    x_time = []
    x_count = []
    y_temp = []
    count = 0
    for dic in temp_list:
        x_count.append(count)
        count += 1
        x_time.append(dic["TimeStamp"])
        y_temp.append(float(dic["Temperature_F"]))
    coefficients = polyfit(x_count, y_temp, 6)
    polynomial = poly1d(coefficients)
    xs = arange(0, len(x_count), 0.1)
    ys = polynomial(xs)
    pyl.plot(x_count, y_temp, 'o')
    pyl.plot(xs, ys)
    pyl.ylabel('Temperature_F')
    pyl.xlabel('x')
    # pyl.show()
    pyl.savefig('./static/foo.png')


if __name__ == "__main__":
    # temperature = {}
    # temperature['TimeStamp'] = '2016-12-4 18:23:21'
    # temperature['Temperature_F'] = '72'
    # put_data_to_DB(temperature)
    get_results_from_DB()