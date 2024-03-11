import requests
import json
 
url = "https://cmjr7ahs2d.execute-api.ap-south-1.amazonaws.com/dev/students/registration/details"
headers = {"Content-Type": "application/json"}
req={
    "firstname": "Kripaa1",
    "lastname": "M",
    "gender": "male",
    "dob": "28-04-2001",
    "age": 22,
    "std": 2,
    "phone":"9048935461"    
}
payload=json.dumps(req)
response = requests.request("POST", url, headers=headers, data=payload)
print(json.dumps(req, indent=4))
print(response.status_code, response.reason)
print(json.dumps(response.json(), indent=4))