import json
import boto3
import os
from aws_lambda_powertools import Logger

logger = Logger()

s3 = boto3.client('s3')
sqs = boto3.client('sqs')
s3_name = os.getenv('s3')

def generate_thumbnail(image_data):
    '''
       Function that creates the thumbnail
    '''
    
    # Need to add Thumbnail Creation Logic
    return image_data

def image_processor(event, context):
    '''
    Handler reponsible to get data from SQS, 
        create the thumbnail and 
        store it back in s3
    '''
    logger.info(event)
    try:
        sqs_record = event['Records'][0]
        s3_obj = json.loads(sqs_record['body'])
        image_key = s3_obj['image_key']
        thumbnail_key = f"thumbnails/{image_key}.jpg"

        # Get the stored object from S3 Uploads
        logger.info(f"Image Key = {image_key}")
        image_object = s3.get_object(
            Bucket=s3_name,
            Key=f"uploads/{image_key}"
        )
        logger.info(image_object['Body'].read())

        thumbnail_data = generate_thumbnail(image_object['Body'].read())

        s3.put_object(
            Bucket=s3_name,
            Key=thumbnail_key,
            Body=thumbnail_data
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Thumbnail generated successfully.'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to generate thumbnail.'})
        }