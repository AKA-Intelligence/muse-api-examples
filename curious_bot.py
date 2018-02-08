import requests
import json
import getpass

muse_server = 'https://muse.themusio.com/api'

def signin(email,password):
	endpoint = '/auth/signin/'
	data = {'email':email,'password':password}
	headers = {'Content-Type':'application/json'}
	response = requests.post(muse_server+endpoint,
		data=json.dumps(data),headers=headers)
	return response.json()['access_token']

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

if __name__ == "__main__":
	email = raw_input("email: ")
	password = getpass.getpass("password: ")

	jwt = signin(email,password)

	used_question_ids = []
	while True:
		user_sent = raw_input("What would you like me to ask you about? > ")
		question, question_id = get_contextual_question(user_sent, used_question_ids, jwt)
		used_question_ids.append(question_id)
		print question