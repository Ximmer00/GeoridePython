#!/user/bin/env python3

import requests 
import sys
import json

GEORIDE_API_HOST = "https://api.georide.fr"
GEORIDE_API_ENDPOINT_LOGIN = "/user/login"

email = sys.argv[1]
password = sys.argv[2]

data = {'email': email, 'password': password}
encoded_data = json.dumps(data).encode('utf-8')

print(encoded_data)

response = requests.post(GEORIDE_API_HOST + GEORIDE_API_ENDPOINT_LOGIN, data=encoded_data, headers={'Content-Type': 'application/json'})
print(response.text)

