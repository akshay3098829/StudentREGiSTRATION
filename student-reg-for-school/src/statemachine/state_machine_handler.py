import json
import logging
import os
from datetime import datetime
from http import HTTPStatus

from botocore.client import BaseClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(name=__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", logging.INFO))


class StateMachineHandler:
    step_function_client: BaseClient
    state_machine_arn: str

    def __init__(self, step_function_client: BaseClient, sm_arn: str):
        self.step_function_client = step_function_client
        self.sm_arn = sm_arn

    def initiate(self, step_function_execution_id: str, request: str) -> (int, str):
        """
        Initiate AWS step function and formulate an HTTP response to send back to the caller.

        :param step_function_execution_id: id of run
        :param request: request
        :return: status, start_date
        """

        logger.info("Step function execution id: %s", step_function_execution_id)

        logger.debug("Starting execution of Step Function\nARN: %s\nName: %s\nRequest: %s",
                     self.sm_arn,
                     step_function_execution_id,
                     request
                     )

        response: dict = self.step_function_client.start_execution(
            stateMachineArn=self.sm_arn,
            name=step_function_execution_id,
            input=request
        )
        logger.debug("Start execution response: %s", response)

        return response
