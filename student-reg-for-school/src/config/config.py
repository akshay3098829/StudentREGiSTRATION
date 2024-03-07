import os


class AppConfig:
    REGION_NAME = "ap-south-1"
    STMachine_SM_ARN = os.environ.get("STMachine_SM_ARN", None)
   
