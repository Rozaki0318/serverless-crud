import json
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    print("UPDATE OF CRUD FUNCTION")
    #print(event)
    print("HTTP METHOD: {}".format(event['httpMethod']))

    dynamodb_client = boto3.client('dynamodb', endpoint_url='http://dynamodb-local:8000')
    
    table_names = dynamodb_client.list_tables()
    table = table_names['TableNames'][0]

    data = json.loads(event['body'])
    print(data)

    try:
        res = dynamodb_client.update_item(
            TableName=table,
            Key={
                "id": {"S": data['id']}
            },
            UpdateExpression='SET #name = :val',
            ExpressionAttributeNames={
                "#name": "name",
            },
            ExpressionAttributeValues={
                ":val": {"S": data['name']},
            },
            ReturnValues="UPDATED_NEW",
        )
    except ClientError as err:
        logger.error(
            "Couldn't insert data.Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
        raise

    return {
        "statusCode": 200,
        "headers":{
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(
            [{
                "Data": res,
            }]
        ),
    }

