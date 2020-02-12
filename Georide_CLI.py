#!/usr/bin/env python3

import requests
import json
import re
import sys
import getopt
import time

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

def get_to_api(sub_url, *args, **kwargs):
    """fonction de requete GET a l'api"""
    head = kwargs.get('header', None)
    encoded_data = kwargs.get('data', None)

    response = requests.get(GEORIDE_API_HOST + sub_url, headers=head)

    if response:
        return response  # returning the response decoded
    else:
        print(response.status_code)  # Stopping programm with the error
        sys.exit()

def post_to_api(sub_url, *args, **kwargs):
    """fonction de requete POST a l'api"""
    head = kwargs.get('header', None)
    encoded_data = kwargs.get('data', None)

    if encoded_data:
        response = requests.post(GEORIDE_API_HOST + sub_url, data=encoded_data, headers={'Content-Type': 'application/json'})
    else:
        response = requests.post(GEORIDE_API_HOST + sub_url, headers=head)

    if response:
        return response  # returning the response decoded
    else:
        print(response.status_code)  # Stopping programm with the error
        sys.exit()


def get_auth_header(token):
    """Retourne le header avec l'Authorization token """
    return{"Authorization": "Bearer " + token}


def get_token(email, password):
    """Recupere le token d'authentificatio"""
    # function to getting the account token (available 30 days)
    data = {'email': email, 'password': password}
    encoded_data = json.dumps(data).encode('utf-8')
    response = post_to_api(GEORIDE_API_ENDPOINT_LOGIN, data=encoded_data)
    content = response.json()  # transforming reponse in hash
    return content['authToken']  # giving back the token


def get_trackers(auth_header):  # This def needs improvement about listing of trackers
    """Recupere la liste des trackers que l'user peut lock"""
    content = get_to_api(GEORIDE_API_ENDPOINT_TRAKERS, header=auth_header)
    response = content.json()
    trackers = []
    for json_tracker in response:
        if json_tracker['canLock']:
            trackers.append(json_tracker)
    return trackers


def lock_tracker(tracker_id, bearer_header):
    try:
        response = post_to_api(GEORIDE_API_ENDPOINT_LOCK.replace(':trackerId', str(tracker_id)), header=bearer_header)
    except Exception as e:
        print(e)
        sys.exit(2)
    if response.status_code != 204:
        return False
    return True


def unlock_tracker(tracker_id, bearer_header):
    try:
        response = post_to_api(GEORIDE_API_ENDPOINT_UNLOCK.replace(':trackerId', str(tracker_id)), header=bearer_header)
    except Exception as e:
        print(e)
        sys.exit(2)
    if response.status_code != 204:
        return False
    return True


def toggle_tracker(tracker_id, bearer_header):
    try:
        response = post_to_api(GEORIDE_API_ENDPOINT_TOGGLE_LOCK.replace(':trackerId', str(tracker_id)), header=bearer_header)
    except Exception as e:
        print(e)
        sys.exit(2)
    if response.status_code != 204:
        return False
    return True


def get_pos(tracker):
    return tracker['latitude'], tracker['longitude']

################################################################################
################################################################################
####################  Functions for this script (local) ########################
################################################################################
################################################################################

def usage():
    print("Usage of Script_CLI.py :\n")
    print("python Script_CLI.py --email your@email.com --password your_password --command command_to_run\n")
    print("Commands are : 'lock', 'unlock', 'status', 'locate'.")

def show_loc(lat, lon):
    url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
    print(f"Well, this are the coordinates of your the tracker : \nLatitude = {lat},\t longitude = {lon}")
    print(f"Url to access with google : {url}")


def printing_state(tracker_state, tracker_name):
    state = ("unlock", "lock")[tracker_state]
    print(f"{tracker_name} is {state}")

def show_status(auth_header, tracker_id):
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

def parse_cli():
    """fonction pour récup les options passées en CLI"""
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'e:p:c:h', ['email=', 'password=', 'command='])
    except getopt.GetoptError:
        #Print a message or do something useful
        print('Something went wrong!')
        usage()
        sys.exit(2)

    for o, a in opts:
        if o == '-h':
            usage()
            sys.exit(2)
        elif (o == '-e' or o == '--email'):
            email = a
        elif (o == '-p' or o == '--password'):
            password = a
        elif (o == '-c' or o == '--command'):
            command = a
        else:
            usage()
            sys.exit(2)
    try:
        if email is None or command is None or password is None:
            usage()
            sys.exit(2)
    except UnboundLocalError:
        usage()
        sys.exit(2)
    return email, password, command

def config_main():
    email_main, password_main, command = parse_cli()
    if not (re.match(r"^[\w_\.]+@[a-zA-Z]+?\.[a-zA-Z]{1,6}",email_main)):
      print("Email is not an correct, exiting ..")
      sys.exit(1)
    return email_main, password_main, command

def command_treat(command, auth_header, tracker):
    if (command == "lock"):
        lock_tracker(tracker['trackerId'], auth_header)
        print("Locked !")
    elif(command == "unlock"):
        unlock_tracker(tracker['trackerId'], auth_header)
        print("Unlocked !")
    elif(command == "toggle"):
        toggle_tracker(tracker['trackerId'], auth_header)
        print("Toggled !")
    elif(command == "status"):
        show_status(auth_header, tracker)
    elif(command == "locate"):
        lat, long = get_pos(tracker)
        show_loc(lat,long)
    else:
        print("Wrong command !\nExiting now..")
        sys.exit(1)


def Main():
    mail, password, command = config_main()
    header = get_auth_header(get_token(mail, password))
    tracker_raw = get_trackers(header)
    tracker = tracker_raw[0]
    command_treat(command, header, tracker)

Main()
