import os
import boto3
from datetime import datetime, timezone
from enum import Enum
from botocore.client import BaseClient
 
#Environmental variables
REGION: str = os.environ.get("REGION", "ap-south-1")
STUDENT_TABLE_NAME: str = os.environ.get("STUDENT_TABLE_NAME", "")
 
#Boto3 resources
DYNAMODB_RESOURCE: BaseClient = boto3.resource("dynamodb", region_name=REGION)
STUDENT_TABLE: BaseClient = DYNAMODB_RESOURCE.Table(STUDENT_TABLE_NAME)
class Status(str, Enum):
    """
    Status of processes
    """
    VERIFICATIONINPROGRESS = "VERIFICATION_IN_PROGRESS"
    VERIFICATIONSUCCESS = "VERIFICATION_SUCCESS"
    VERIFICATIONREJECTED = "VERIFICATION_REJECTED"
    ADMISSIONCOMPLETED = "ADMISSION_COMPLETED"
    ADMISSIONREJECTED = "ADMISSION_REJECTED"
 
def create_tracker(
        student_id: str,
        firstname: str,
        lastname: str,
        gender: str,
        dob: str,
        age: int,
        std = int,
        phone = str
    ):
    now: datetime = datetime.now(timezone.utc)
    table_item: dict = {
        "student_id": student_id,
        "Firstname": firstname,
        "Lastname": lastname,
        "Gender": gender,
        "DOB": dob,
        "Age": age,
        "Std": std,
        "Phone": phone,
        "Status": Status.VERIFICATIONINPROGRESS.value,
        "CreatedDt": now.isoformat(),
        "UpdatedDt": now.isoformat(),
    }
 
    STUDENT_TABLE.put_item(Item=table_item)
 
 
def update_tracker(
        student_id: str,
        status: Status
):
    update_expression = "SET #status = :s"
    expression_attribute_names = {"#status": "Status"}
    expression_attribute_values = {":s": status.value}
 
    response = STUDENT_TABLE.update_item(
        Key={"student_id": student_id},
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values
    )