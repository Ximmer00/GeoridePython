#!/user/bin/env python3

import requests
import sys
import json
import re
import getopt

GEORIDE_API_HOST = "https://api.georide.fr"
GEORIDE_API_ENDPOINT_LOGIN = "/user/login"
GEORIDE_API_ENDPOINT_TRAKERS = "/user/trackers"
GEORIDE_API_ENDPOINT_LOCK = "/tracker/:trackerId/lock"
GEORIDE_API_ENDPOINT_UNLOCK = "/tracker/:trackerId/unlock"
GEORIDE_API_ENDPOINT_TOGGLE_LOCK = "/tracker/:trackerId/toggleLock"


# email = sys.argv[1]
# password = sys.argv[2]
email = "ximmer00@gmail.com"
password = "INeSIsTiOLErnutheNeYEalFO"

def request_to_api(sub_url, reqType, *args, **kwargs):
    """fonction de requete a l'api"""
    head = kwargs.get('header', None)
    encoded_data = kwargs.get('data', None)

    if reqType == 'POST':
        response = requests.post(GEORIDE_API_HOST + sub_url, data=encoded_data,
                                 headers={'Content-Type': 'application/json'})
    elif reqType == 'GET':
        response = requests.get(GEORIDE_API_HOST + sub_url, headers=head)
    else:
        print("ALERTE !!")

    if response:
        return response  # returning the response decoded
    else:
        print(r.status_code)  # Stopping programm with the error
        sys.exit()

def get_auth_header(token):
    """Retourne le header avec l'Authorization token """
    return {"Authorization": "Bearer " + token}

def get_token(email, password):
    """Récupère le token d'authentificatio"""
    # function to getting the account token (available 30 days)
    data = {'email': email, 'password': password}
    encoded_data = json.dumps(data).encode('utf-8')
    response = request_to_api(GEORIDE_API_ENDPOINT_LOGIN,'POST', data=encoded_data)
    content = response.json()  # transforming reponse in hash
    return content['authToken']  # giving back the token



token = get_auth_header(get_token(email,password))
response = request_to_api(GEORIDE_API_ENDPOINT_TRAKERS, 'GET', header=token)
content = response.json()
kilometers = content[0]['odometer']/1000
print(re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % kilometers))
