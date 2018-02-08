import json
import requests
import getpass
from config import muse_server

def signin(email,password):
	endpoint = muse_server + '/auth/signin/'
	data = {'email':email,'password':password}
	headers = {'content-type':'application/json'}
	resp = requests.post(endpoint,
		data=json.dumps(data),
		headers=headers)
	jwt = resp.json()['access_token']
	return jwt

def chat(user_text,jwt,member_id,bot_emotion):
	endpoint = muse_server + '/chat/'
	data = {'user_text':user_text,'member_id':member_id,'bot_emotion':bot_emotion}
	headers = {'content-type':'application/json',
			   'Authorization':'Bearer '+jwt}
	resp = requests.post(endpoint,
		data=json.dumps(data),
		headers=headers)
	return resp.json()		

def choose_member(jwt):
	endpoint = '/member/'
	headers = {'Authorization':'Bearer '+jwt}
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

def choose_bot_emotion():
	options = ['neutral', 'anger', 'joy', 'fear', 'sadness']
	def print_options():
		print("Choose bot emotion. Options are: neutral, anger, joy, fear, sadness")
	bot_emotion = str(raw_input('bot emotion> '))
	while bot_emotion not in options:
		print "Not a valid bot emotion."
		print_options()
		bot_emotion = str(raw_input('bot emotion> '))
	return bot_emotion






if __name__ == '__main__':
	email = raw_input("email: ")
	password = getpass.getpass("password: ")

	jwt = signin(email,password)
	member_id = choose_member(jwt)
	bot_emotion = choose_bot_emotion()

	while True:
		user_text = raw_input('[U] ')
		try:
			chat_resp = chat(user_text,jwt,member_id,bot_emotion)['data']['text_out']['text']
		except:
			jwt = signin(email,password)
			chat_resp = chat(user_text,jwt,member_id,bot_emotion)['data']['text_out']['text']

		print '[B]', chat_resp