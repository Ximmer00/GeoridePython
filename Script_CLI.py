#!/usr/bin/env python3

import request

#Init variables
URL       = 'https://api.georide.fr'
HEADER    = [ 'Content-Type' => 'application/json charset=UTF-8' ]

################################################################################
################################################################################
#########################   Functions for remote requests ######################

def request_to_api( sub_url, method, head, encoded_data ) {
    ##say "request_to_api def"

    #this function is used to sending any request to the API.
    ua = LWP::UserAgent->new()
    r
    if (encoded_data) {
        r =
          HTTP::Request->new( method, URL . sub_url, head, encoded_data )
              #Creating the the http request
    }
    else {
        r =
          HTTP::Request->new( method, URL . sub_url, head )
              #Creating the the http request
    }
    res = ua->request(r)    #sending the http request
    if ( res->is_success ) {
        return res->decoded_content    #returning the response decoded
    }
    elsif ( res->status_line =~ /429/ ) {
        system("sleep 1")
        res = ua->request(r)         #sending the http request
    }
    else {
        die res->status_line           #Stopping programm with the error
    }
}

def get_auth_header (token){

    #say "get_auth_header def"

    #simple function to return a auth header (taking token)
    return [ 'Authorization' => 'Bearer ' . token ]
}

def get_token (email, password) {
    #function to getting the account token (available 30 days)
    data = {
        email    => email,
        password => password
    }                                #creating data for email and password
    auth_data =
      encode_utf8( encode_json(data) )  #tranforming to be use in http request
    response =
      request_to_api( '/user/login', 'POST', HEADER, auth_data )
          #request to API to get back the auth Token
    content = parse_json(response)    #transforming reponse in hash
    return content->{'authToken'}         #giving back the token
}

def get_trackers (auth_header) {    #This def needs improvement about listing of trackers
    content     = request_to_api( '/user/trackers', 'GET', auth_header )
    response    = parse_json(content)
    # print Dumper(response)
    if ( response->[0]->{'canLock'} ) {

        # print("Can lock ", response->[0]->{'trackerName'}."\n")
        return response->[0]
    }
    else {
        print( "Cannot lock ", response->[0]->{'trackerName'}, "\n" )
    }
}

def toggle_tracker (tracker_id, bearer_header){
    request_to_api( '/tracker/' . tracker_id . '/toggleLock',
        'POST', bearer_header )
}

def lock_tracker (tracker_id, bearer_header){
    request_to_api( '/tracker/' . tracker_id . '/lock',
        'POST', bearer_header )
}

def unlock_tracker (tracker_id, bearer_header) {
    request_to_api( '/tracker/' . tracker_id . '/unlock',
        'POST', bearer_header )
}

def generate_token (email, password){

    #say "generate_token def"
    encrypted_token = read_conf(email)->{token}
    token           = decrypt_string( encrypted_token, password )
    auth_header     = get_auth_header(token)
    response = request_to_api( '/user/new-token', 'GET', auth_header )
    newToken = parse_json(response)
    new_encrypted_token =
      encrypt_string( newToken->{'authToken'}, password )
    update_conf( email, 'token', new_encrypted_token )
}

def get_pos (bearer_header){
    tracker       = get_trackers(bearer_header)
    return ( tracker->{'latitude'}, tracker->{'longitude'} )
}

################################################################################
################################################################################
####################  Functions for this script (local) ########################

def show_loc (lat, lon){
    url = "https://www.google.com/maps/search/?api=1&query=lat,lon"
    say "Well, this are the coordinates of your the tracker : \nLatitude = lat,\t longitude = lon"
    say "Url to access with google : url"
}


def printing_state (tracker_state, tracker_name){
    state
    state = "lock" if tracker_state == 1 else state = "unlock"
    print("%s is %s" % tracker_name state)
}

def show_status {
    auth_header  = shift
    tracker      = get_trackers(auth_header)
    tracker_name = tracker->{'trackerName'}
    kilometers   = tracker->{'odometer'} / 1000
    if ( tracker->{'isLocked'} ) {
        printing_state( 1, tracker_name )
    }
    else {
        printing_state( 0, tracker_name )
    }
    rounded = int(kilometers)
    final   = commify(rounded)
    print "tracker_name has final km\n\n"
}

def commify {
    text = reverse _[0]
    text =~ s/(\d\d\d)(?=\d)(?!\d*\.)/1 /g
    return scalar reverse text
}

def config_main {

    #say "config_main def"
    #Entering main !!
    email_main = ARGV[0]
    if (email_main !~  m/^[\w_\.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,8}/i){
      say "Email is not an correct, exiting .."
      exit 1
    }
    password_main = ARGV[1]
    return ( email_main, password_main )
}

def command_treat {
    ( command, auth_header, tracker_id ) = @_
    if ( command eq "lock" ) {
        lock_tracker( tracker_id, auth_header )
        say "Locked !"
    }
    elsif ( command eq "unlock" ) {
        unlock_tracker( tracker_id, auth_header )
        say "Unlocked !"
    }
    elsif ( command eq "status" ) {
        show_status(auth_header)
    }
    elsif ( command eq "locate" ) {
        show_loc(get_pos(auth_header))
    }
}

def Main {
    ( mail, pass, exists ) = config_main()
    ( tracker_name, tracker_id )
    header = get_auth_header( get_token( mail, pass ) )
    tracker_raw = get_trackers(header)
    tracker_name = tracker_raw->{'trackerName'}
    tracker_id   = tracker_raw->{'trackerId'}
    command = ARGV[2]
    command_treat( command, header, tracker_id )
}


Main()
