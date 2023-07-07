import json
import boto3
import logging

def lambda_handler(event, context):
    print("CRUD FUNCTION")

    dynamodb_client = boto3.client('dynamodb', endpoint_url='http://dynamodb-local:8000')

    print("##DYNAMDB CLIENT##:{}".format(dynamodb_client))

    res = dynamodb_client.list_tables()
    print("##DYNAMODB TABLE##:{}".format(res['TableNames']))
    table = res['TableNames'][0]

    res_scan = dynamodb_client.scan(
        TableName = table,
    )

    return {
        "statusCode": 200,
        "headers":{
            "Access-Control-Allow-Origin": "*",
            #"Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(
            [{
                "Data": res_scan,
            }]
        ),
    }

