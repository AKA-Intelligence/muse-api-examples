import json
import requests
import getpass

from muse_util import muse_server, signin, choose_member

def chat(user_text,jwt,member_id):
    endpoint = "/chat/"
    data = {'user_text':user_text,'member_id':member_id}
    headers = {'content-type':'application/json',
               'Authorization':'Bearer '+jwt}
    resp = requests.post(muse_server + endpoint,
                         data=json.dumps(data),
                         headers=headers)
    return resp.json()      

def main():
    email = raw_input("email: ")
    password = getpass.getpass("password: ")
    jwt = signin(email,password)
    member_id = choose_member(jwt)
    while True:
        user_text = raw_input('[U] ')
        try:
            chat_resp = chat(user_text,jwt,member_id)['data']['text_out']['text']
        except:
            jwt = signin(email,password)
            chat_resp = chat(user_text,jwt,member_id)['data']['text_out']['text']
        print '[B]', chat_resp

if __name__ == "__main__":
    main()