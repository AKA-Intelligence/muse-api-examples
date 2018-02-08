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

def chat(user_text,jwt,member_id):
	endpoint = muse_server + '/scripted/'
	data = {'user_text':user_text,'member_id':member_id}
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

if __name__ == '__main__':
	email = raw_input("email: ")
	password = getpass.getpass("password: ")

	jwt = signin(email,password)
	member_id = choose_member(jwt)

	while True:
		user_text = raw_input('[U] ')
		try:
			chat_resp = chat(user_text,jwt,member_id)['data']['lines_out']
		except:
			jwt = signin(email,password)
			chat_resp = chat(user_text,jwt,member_id)['data']['lines_out']

		for line in chat_resp:
			print '[B]', line['line']