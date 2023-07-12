import json
import boto3
import logging

def lambda_handler(event, context):
    print("CREATE OF CRUD FUNCTION")
    print(event)
    print("HTTP METHOD: {}".format(event['httpMethod']))


    dynamodb_client = boto3.client('dynamodb', endpoint_url='http://dynamodb-local:8000')
    table_names = dynamodb_client.list_tables()
    table = table_names['TableNames'][0]

    data = json.loads(event['body'])
    print(data)
    print(data['id'])
    print(data['name'])

    res = dynamodb_client.put_item(
        TableName=table,
        Item={
            "id": {"S": data['id']},
            "name": {"S": data['name']}
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
