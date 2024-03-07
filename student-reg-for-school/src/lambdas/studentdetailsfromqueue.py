import json
import os
import boto3
from typing import Any, Dict, Tuple, Optional, List
from decimal import Decimal
from functools import lru_cache
from botocore.client import BaseClient
from src.statemachine.state_machine_handler import StateMachineHandler
from http import HTTPStatus
from src.config.config import AppConfig
REGION: str = os.environ.get("REGION", "ap-south-1")
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)

        return json.JSONEncoder.default(self, obj)
@lru_cache(maxsize=1)
def get_step_function_client() -> BaseClient:
    """
    Retrieves a step function client for interaction with the step function AWS API.

    :returns: The step function client.
    """
    return boto3.client("stepfunctions", region_name=REGION)

def lambda_handler(event,context):
    print(event)
    for record in event["Records"]:
        record = json.loads(record["body"])
        intiate_step_function(request=record)
    print("EVENTFROMQUE_TRIGGERED")    
    return
def intiate_step_function(request: Dict[str,Any]):
    step_function_client = get_step_function_client()
    sm_handler = StateMachineHandler(step_function_client,
                                     AppConfig.STMachine_SM_ARN)
    step_function_id = request["student_id"]
    response = sm_handler.initiate(
            step_function_id, json.dumps(request, cls=JSONEncoder)
        )
    status_code: int = response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code == HTTPStatus.OK:
        print("STEP_FUN_SUCESS")
    else:
        print("STEP_FUN_FAILURE")    
    return