import requests
import json



data = [



    
    {
       
        "student_id": 6,
        "date": "2025-09-26",
        "status": "ABSENT",
        
    },
    {
        
        "student_id": 10,
        "date": "2025-09-26",
        "status": "PRESENT",
       
    }
    
]



url="http://127.0.0.1:8000/api/student/attendance/mark/"
json_data=json.dumps(data)
response = requests.post(url, json=json_data)




print( response.status_code)
print(response.json())