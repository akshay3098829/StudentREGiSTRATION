import requests
import json
 
url = "https://poj8wdc4rf.execute-api.ap-south-1.amazonaws.com/dev/students/registration/details"
headers = {"Content-Type": "application/json"}
req={
    "firstname": "Akhil",
    "lastname": "Doe",
    "gender": "male",
    "dob": "17-06-2002",
    "age": 6,
    "std": 1,
    "phone":"9048935467"    
}
payload=json.dumps(req)
response = requests.request("POST", url, headers=headers, data=payload)
print(json.dumps(req, indent=4))
print(response.status_code, response.reason)
print(json.dumps(response.json(), indent=4))