import boto3
import json
# Send message to SQS queue
def send_sqs_message(name: str, message: dict) -> str:
    sqs = boto3.client('sqs')
    queue = sqs.get_queue_url(QueueName=name)
    response = sqs.send_message(QueueUrl=queue['QueueUrl'], MessageBody=json.dumps(message))
    return response