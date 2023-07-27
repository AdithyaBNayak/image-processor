try:
    import unzip_requirements
    import req
    from PIL import Image
except:
    pass    

import json
import base64
import boto3
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
    '''
        Function Responsible to Take the Image from the API
        Upload the Image to S3
        Also Send the data to queue    
    '''
    logger.info(event)
    # Put the Object into the Bucket
    image_data = json.loads(event['body'])
    image_file = image_data['file']
    
    # Decode the base64-encoded string
    decoded_bytes = base64.b64decode(image_file.replace("data:image/jpeg;base64,",""))
    logger.info(decoded_bytes)
    
    image_key = f"{int(time.time())}_{uuid.uuid4().hex}.jpg"
    try:
        
        s3.put_object(
            Bucket= s3_name,
            Key=f"uploads/{image_key}",
            Body=decoded_bytes,
            ContentType='image/jpeg'
        )
        
    except Exception as e:
        logger.info("Error in Uploading the Image to S3")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to Upload the image.'})
        }     

    try:
        # Add a message to the SQS queue for thumbnail generation
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps({
                'image_key': image_key
            })
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Image uploaded successfully.'})
        }
        
    except Exception as e:
        logger.info("Failed to Send the image to Thumbnail Generator.")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to Send the image to Thumbnail Generator.'})
        }    
