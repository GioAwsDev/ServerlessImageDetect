import json
import boto3
import os
import sys
import uuid
import logging

def lambda_handler(event, context):
	
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    rekognition_client = boto3.client('rekognition')
    dynamodb_client = client = boto3.client('dynamodb')
    
    logger.info('Found event{}'.format(event))
    
    
    for record in event['Records']:
        # Read the value of the eventSource attribute. 
        #
        # You can use this to conditionally handle events 
        # from different triggers in the same lambda function.
        event_source = record['eventSource']
        logger.info(event_source)
        
        # read S3 bucket and object key
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key'] 
        min_confidence = 90
        
        logger.info('Found bucket ' +  bucket)
        logger.info('Found key ' + key)
        
        # use Amazon Rekognition to detect text in the image
        rekognition_results = rekognition_client.detect_text(
            Image = {'S3Object': {'Bucket': bucket,'Name': key}}, Filters = {'WordFilter': {'MinConfidence': min_confidence}})
        
        # write results of text detection to DynamoDB
        for result in rekognition_results['TextDetections']:
            
            vehplate = result['DetectedText']
            confidence = str(result['Confidence'])
            
            logger.info('Found text ' + vehplate)
            
            dynamodb_response = dynamodb_client.put_item(
                Item={'vehicle': {'S': vehplate},'filename': {'S': key}, 'confidence': {'N':confidence}},
                ReturnConsumedCapacity='TOTAL',
                TableName='plateindex')
                
            logger.info('DynamDBResponse ' + format(dynamodb_response))


    # return the entities that were detected.
    return {
    'statusCode': 200,
    }