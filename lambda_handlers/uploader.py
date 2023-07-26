import json
import boto3
import base64
import time
import uuid
import os
from aws_lambda_powertools import Logger

logger = Logger()

s3 = boto3.client('s3')
sqs = boto3.client('sqs')
s3_name = os.getenv('s3')

queue_url = os.getenv('queue')

def image_uploader(event, context):
    body = json.loads(event['body'])
    image_data = base64.b64decode(body['image'])
    image_key = f"uploads/{int(time.time())}_{uuid.uuid4().hex}.jpg"
    
    s3.put_object(
        Bucket= s3_name,
        Key=image_key,
        Body=image_data
    )

    # Add a message to the SQS queue for thumbnail generation
    sqs.send_message(
        QueueUrl=queue_url,  # You'll get this from the AWS console or programmatically
        MessageBody=json.dumps({
            'image_key': image_key
        })
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Image uploaded successfully.'})
    }
