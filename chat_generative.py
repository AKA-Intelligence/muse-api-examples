import json
import requests
import getpass

muse_server = 'https://muse.themusio.com/api'

def signin(email,password):
	endpoint = muse_server + '/auth/signin/'
	data = {'email':email,'password':password}
	headers = {'content-type':'application/json'}
	resp = requests.post(endpoint,
		data=json.dumps(data),
		headers=headers)
	jwt = resp.json()['access_token']
	return jwt

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
	print_options()
	bot_emotion = str(raw_input('bot emotion> '))
	while bot_emotion.lower() not in options:
		print "Not a valid bot emotion."
		print_options()
		bot_emotion = str(raw_input('bot emotion> '))
	return bot_emotion


def comprehend(passage,question,jwt,member_id):
	headers = {'Authorization':'Bearer '+jwt}
	data = {'passages':[passage],'questions':[question]}
	res = requests.post(muse_server+'/nlp/machine-comprehension/',json=data, headers=headers)
	return res.json()[0]['best_span_str']

def chat_generate(context,bot_emotion,jwt,member_id):
	headers = {'Authorization':'Bearer '+jwt}
	context = context[-3:]
	data = {'context':context,'emotion':bot_emotion}
	res = requests.post(muse_server+'/chat/generate/',json=data, headers=headers)
	return res.json()['data']['response']


if __name__ == '__main__':
	email = raw_input("email: ")
	password = getpass.getpass("password: ")

	jwt = signin(email,password)
	member_id = choose_member(jwt)
	bot_emotion = choose_bot_emotion()

	chat_hist = []

	while True:
		user_text = raw_input('[U] ')

		chat_hist = chat_hist + [user_text]

		resp_generative = chat_generate(
			context=chat_hist,
			bot_emotion=bot_emotion,
			jwt=jwt,
			member_id=member_id)

		chat_hist = chat_hist + [resp_generative]

		print '[B]', resp_generative