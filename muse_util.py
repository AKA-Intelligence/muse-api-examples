import json
import requests

muse_server = 'http://muse.themusio.com/api'

def signin(email,password):
    endpoint = '/auth/signin/'
    data = {'email':email,'password':password}
    headers = {'Content-Type':'application/json'}
    response = requests.post(muse_server+endpoint,
                             data=json.dumps(data),
                             headers=headers)
    return response.json()['access_token']

def choose_member(access_token):
    endpoint = '/member/'
    headers = {'Authorization':'Bearer '+access_token}
    response = requests.get(muse_server+endpoint,
                            headers=headers)
    members = response.json()['data']
    member_ids = [str(member['member_id']) for member in members]
    def print_members():
        print "Choose a member"
        for member in members:
            print member['member_id'], member['first_name'], member['last_name']
    print_members()
    chosen_member_id = str(raw_input('member id> '))
    while chosen_member_id not in member_ids:
        print "Not a valid member id. Choose a member:"
        print_members()
        chosen_member_id = str(raw_input('member id> '))
    return chosen_member_id
