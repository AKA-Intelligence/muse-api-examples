import getpass
import requests
import random
import json

muse_server = 'https://muse.themusio.com/api'

def argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)

def signin(email,password):
	endpoint = '/auth/signin/'
	data = {'email':email,'password':password}
	headers = {'Content-Type':'application/json'}
	response = requests.post(muse_server+endpoint,
		data=json.dumps(data),headers=headers)
	return response.json()['access_token']

def get_candidate_responses(sent,access_token):
	endpoint = '/chat/engine/retrieve/default/'
	data = {'text':sent}
	headers = {'Authorization':'Bearer '+access_token}
	response = requests.post(muse_server+endpoint,
		data=json.dumps(data),headers=headers)
	candidates = response.json()['data']['candidates']
	candidates_text = [candidate['text'] for candidate in candidates]
	return candidates_text

def filter_responses(sent,candidates,access_token):
	endpoint = '/nlp/relevance/multi/'
	data = {'text1':sent,'candidates':candidates}
	headers = {'Authorization':'Bearer '+access_token}
	response = requests.post(muse_server+endpoint,
		data=json.dumps(data),headers=headers)
	best_response = response.json()['data']['best']
	candidate_scores = response.json()['data']['scores']
	return best_response, candidate_scores

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

if __name__ == '__main__':
	email = raw_input("email: ")
	password = getpass.getpass("password: ")

	access_token = signin(email,password)
	member_id = choose_member(access_token)

	count = 0
	text_out_2 = raw_input("Type a seed sentence > ")
	while count < 7:


		candidates_1 = get_candidate_responses(text_out_2,access_token)
		best_1, scores_1 = filter_responses(text_out_2,candidates_1,access_token)
		scores_argsort_1 = argsort(scores_1)
		text_out_1 = candidates_1[random.choice(scores_argsort_1[-5:])]


		candidates_2 = get_candidate_responses(text_out_1,access_token)
		best_2, scores_2 = filter_responses(text_out_1,candidates_2,access_token)
		scores_argsort_2 = argsort(scores_2)
		text_out_2 = candidates_2[random.choice(scores_argsort_2[-5:])]

		print 'bot1', text_out_1
		print 'bot2', text_out_2
		count += 1