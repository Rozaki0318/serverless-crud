import json
import boto3
import logging

def lambda_handler(event, context):
    print("DELETE OF CRUD FUNCTION")
    print(event)
    print("HTTP METHOD: {}".format(event['httpMethod']))


    dynamodb_client = boto3.client('dynamodb', endpoint_url='http://dynamodb-local:8000')
    table_names = dynamodb_client.list_tables()
    table = table_names['TableNames'][0]

    data = json.loads(event['body'])
    print(data)
    print(data['id'])
    print(data['name'])

    res = dynamodb_client.delete_item(
        TableName=table,
        Key={
            "id": {"S": data['id']}
        }
    )
    print(res)

    return {
        "statusCode": 200,
        "headers":{
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(
            [{
                "Data": 'hello post',
            }]
        ),
    }

