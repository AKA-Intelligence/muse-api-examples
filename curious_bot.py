import json
import requests
import getpass

from muse_util import muse_server, signin, choose_member

def get_contextual_question(sent,used_question_ids,jwt):
    endpoint = '/chat/question/'
    data = {'context':sent,
            'used_ids':used_question_ids,
            'random':False}
    headers = {'Authorization':'Bearer ' + jwt}
    response = requests.post(muse_server+endpoint,
                             data=json.dumps(data))
    question = response.json()['data']['question']
    question_id = response.json()['data']['question_id']
    return question, question_id 

def main():
    email = raw_input("email: ")
    password = getpass.getpass("password: ")
    jwt = signin(email,password)
    used_question_ids = []
    while True:
        user_sent = raw_input("What would you like me to ask you about? > ")
        question, question_id = get_contextual_question(user_sent, used_question_ids, jwt)
        used_question_ids.append(question_id)
        print question

if __name__ == "__main__":
    main()