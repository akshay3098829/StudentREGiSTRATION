import json
import os
from http import HTTPStatus
from typing import Union, Dict, Any, List
from datetime import timedelta, datetime, timezone
import uuid
from src.utils.validation import RequestValidator, ValidationError
from src.utils.awsutils import send_sqs_message
STUDENT_REG_QUEUE = os.environ.get(
    "STUDENT_THROTTLING_QUEUE", "student_reg_throttle"
)
UTC_OFFSET: int = 10
INSTANCE_DATE_FORMAT: str = "%Y-%m-%dT%H%M%S"
def lambda_handler(event, context):
    print("EVENT",event)
    return student_registration(event)
def student_registration(event: Dict[str, Any]) -> Dict[str, Any]:
    request: dict = json.loads(event["body"])
    errors=RequestValidator.validate_request(request)
    if errors:
        error_details: dict = {
            "student_id": None,
            "message": f"Invalid request: found {len(errors)} error(s)",
            "errorDetails": [e.error for e in errors],
        }
        return format_response(HTTPStatus.BAD_REQUEST,error_details)
    now: datetime = datetime.now(tz=timezone.utc)   
    dt: str = (now + timedelta(hours=UTC_OFFSET)).strftime(INSTANCE_DATE_FORMAT)
    student_id: str = f"{dt}-{str(uuid.uuid4())}" 
    request["student_id"]=student_id
    send_msg_to_queue(request)
    return format_response(
        HTTPStatus.OK,
        {"studentId":student_id,
        "message":"Student verification in progress"}
        )
    
def format_response(
    status_code: HTTPStatus, body: Union[Dict[str, Any], str]
) -> Dict[str, Any]:
    """
    Formats a response object/string to a valid HTTP response.

    :param status_code: The response status code.
    :param body: The response object/string.
    :returns: Formatted HTTP response.
    """
    body_text: str = json.dumps(body) if isinstance(body, dict) else body
    return {"statusCode": status_code.value, "body": body_text}
def send_msg_to_queue(request: dict):
    response = send_sqs_message(STUDENT_REG_QUEUE, request)
    status_code: int = response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code == HTTPStatus.OK:
        print("Successfully queued  request on student queue.")
        return format_response(
            HTTPStatus.OK,
            {"message": "queed"},
        )        

    