#!/usr/bin/env python3

import requests
import re
import sys
import getopt

# Init variables
GEORIDE_API_HOST = "https://api.georide.fr"
GEORIDE_API_ENDPOINT_LOGIN = "/user/login"
GEORIDE_API_ENDPOINT_TRAKERS = "/user/trackers"
GEORIDE_API_ENDPOINT_LOCK = "/tracker/:trackerId/lock"
GEORIDE_API_ENDPOINT_UNLOCK = "/tracker/:trackerId/unlock"
GEORIDE_API_ENDPOINT_TOGGLE_LOCK = "/tracker/:trackerId/toggleLock"


################################################################################
################################################################################
#########################   Functions for remote requests ######################

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
    return{"Authorization": "Bearer " + token}


def get_token(email, password):
    """Récupère le token d'authentificatio"""
    # function to getting the account token (available 30 days)
    data = {'email': email, 'password': password}
    encoded_data = json.dumps(data).encode('utf-8')
    request_to_api(GEORIDE_API_ENDPOINT_LOGIN,'POST', data=encoded_data)
    content = response.json()  # transforming reponse in hash
    return content['authToken']  # giving back the token


def get_trackers(auth_header):  # This def needs improvement about listing of trackers
    """Récupère la liste des trackers que l'user peut lock"""
    content = request_to_api(GEORIDE_API_ENDPOINT_TRAKERS, 'GET', header=auth_header)
    response = content.json()
    trackers = []
    for json_tracker in response_data:
        if json_tracker['canLock']:
            trackers.append(GeorideTracker.from_json(json_tracker))
    return trackers


def toggle_tracker(tracker_id, bearer_header):
    response = request_to_api(GEORIDE_API_HOST + GEORIDE_API_ENDPOINT_TOGGLE_LOCK.replace(':trackerId', str(tracker_id)), 'POST', head=bearer_header)
    response_data = response.json()
    return response_data['locked']


def lock_tracker(tracker_id, bearer_header):
    response = request_to_api(GEORIDE_API_HOST + GEORIDE_API_ENDPOINT_LOCK.replace(':trackerId', str(tracker_id)), head=bearer_header)
    if response.status_code != 204:
        return False
    return True


def unlock_tracker(tracker_id, bearer_header):
    response = request_to_api(GEORIDE_API_HOST + GEORIDE_API_ENDPOINT_UNLOCK.replace(':trackerId', str(tracker_id)), head=bearer_header)
    if response.status_code != 204:
        return False
    return True


def get_pos(bearer_header):
    tracker_raw = get_trackers(bearer_header)
    tracker = tracker_raw.json()
    return tracker[0]['latitude'], tracker[0]['longitude']

################################################################################
################################################################################
####################  Functions for this script (local) ########################

def show_loc(lat, lon):
    url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
    print(f"Well, this are the coordinates of your the tracker : \nLatitude = {lat},\t longitude = {lon}")
    print(f"Url to access with google : {url}")


def printing_state(tracker_state, tracker_name):
    # state = "lock" if tracker_state else state = "unlock"
    state = ("unlock", "lock")[tracker_state]
    print("%s is %s" % tracker_name, state)

def show_status(auth_header):
    tracker = get_trackers(auth_header)
    tracker_name = tracker[0]['trackerName']
    kilometers = tracker[0]['odometer'] / 1000
    if (tracker[0]['isLocked']):
        printing_state(1, tracker_name)
    else:
        printing_state(0, tracker_name)
    rounded = int(kilometers)
    final = commify(rounded)
    print(f"{tracker_name} has {final} km")

def commify (text):
    return re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % text)


def config_main():
    email_main = ARGV[0]
    if not (re.match(r"^[\w_\.]+@[a-zA-Z]+?\.[a-zA-Z]{1,6}",email_main)):
      print("Email is not an correct, exiting ..")
      sys.exit(1)
    password_main = ARGV[1]
    return email_main, password_main

def command_treat(command, auth_header, tracker_id):
    if (command == "lock"):
        lock_tracker(tracker_id, auth_header)
        print("Locked !")
    elif(command == "unlock"):
        unlock_tracker(tracker_id, auth_header)
        print("Unlocked !")
    elif(command == "status"):
        show_status(auth_header)
    elif(command == "locate"):
        show_loc(get_pos(auth_header))



def Main():
    mail, password = config_main()
    header = get_auth_header(get_token(mail, password))
    tracker_raw = get_trackers(header)
    tracker_name = tracker_raw[0]['trackerName']
    tracker_id = tracker_raw[0]['trackerId']
    command = ARGV[2]
    command_treat(command, header, tracker_id)

Main()
