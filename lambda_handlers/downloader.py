import boto3
import os
import base64
import json
from aws_lambda_powertools import Logger

logger = Logger()
s3 = boto3.client('s3')
s3_name = os.getenv('s3')


def image_downloader(event,context):
    logger.info(event)
    try:
        body = event['pathParameters']
        image_key = body['key']
        
        
        image_object = s3.get_object(
                Bucket=s3_name,
                Key=f"thumbnails/{image_key}"
            )
        
        logger.info(image_object['Body'])

        image = image_object['Body'].read()    
        return {
            "statusCode": 200,
            "body": base64.b64encode(image),
            "isBase64Encoded": True
        }
    except:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to Download the image.'})
        }    