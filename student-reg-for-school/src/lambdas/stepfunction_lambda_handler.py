from datetime import datetime
from src.utils.tracker_utils import update_tracker,Status
def lambda_handler(event, context):
    print("stepfunction111111111111111111111",event)
    dob=event["dob"]
    age=event["age"]
    phone=event["phone"]
    length=len(phone)
    present_age = calculate_age(dob)
    student_id=event["student_id"]
    if present_age != age or length != 10:
       update_tracker(student_id=student_id,status=Status.VERIFICATIONREJECTED)
    else:
        update_tracker(student_id=student_id,status=Status.VERIFICATIONSUCCESS)   
    if present_age==age:
        return{"dob":True}
    else:
        return{"dob":False}
def calculate_age(dob):
    # Convert the date of birth string to a datetime object
    dob_date = datetime.strptime(dob, "%d-%m-%Y")

    # Get today's date
    today_date = datetime.today()

    # Calculate the age
    age = today_date.year - dob_date.year - ((today_date.month, today_date.day) < (dob_date.month, dob_date.day))

    return age