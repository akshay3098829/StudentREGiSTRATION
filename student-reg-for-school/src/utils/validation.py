from dataclasses import dataclass
from typing import Tuple, Optional, List
@dataclass
class ValidationError:
    error: str

    def __hash__(self):
        """
        Define a hashing function as we'll be adding records of this class to a set.

        :return:
        """
        return hash(self.error)
class RequestValidator:
    @staticmethod
    def validate_request(
        request: dict, 
    ) -> List[ValidationError]:
        validation_errors: List[ValidationError] = []
        age_vs_std = {1:6,2:7,3:8,4:9,5:10,6:11,7:12,8:13,9:14,10:15,11:16,12:17}
        if not request:
            validation_errors.append(ValidationError("Request is empty"))
            return validation_errors
        print("firstname validation starting",request["firstname"])
        if "firstname" not in request or not request["firstname"]:
            print("eroor in firstname")
            validation_errors.append(ValidationError("firstname not in request or firstname is None"))
        if request["std"] in age_vs_std:
            std=request["std"]
            print("STD",std)
            requ_age= age_vs_std[std]
            print("REQAGE",requ_age)
            if  request["age"]<requ_age:
                validation_errors.append(ValidationError("Age is less for the std"))
        return validation_errors    