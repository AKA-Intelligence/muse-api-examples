from config import muse_server
import getpass

import numpy as np

import requests
import json

import ipdb

def signin(email,password):
	endpoint = '/auth/signin/'
	data = {'email':email,'password':password}
	headers = {'Content-Type':'application/json'}
	response = requests.post(muse_server+endpoint,
		data=json.dumps(data),headers=headers)
	return response.json()['access_token']

def get_candidate_responses(sent,source='1'):
	endpoint = '/chat/engine/retrieve/'
	data = {'text':sent,'source':str(source)}
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
	return best_response

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

def choose_data_source():
	options = [1,2,3]
	def print_options():
		print("Choose response data source. Options are 1,2,3")
	print_options()
	data_source = str(raw_input('data source> '))
	while int(data_source.lower()) not in options:
		print "Not a valid data source."
		print_options()
		data_source = str(raw_input('data source> '))
	return data_source

def post_chatlog(member_id,text_in,text_out,access_token):
	endpoint = '/chatlog/%s/'%str(member_id)
	headers = {"Authorization":"Bearer "+access_token}
	data = {"text_in":text_in,"text_out":text_out}
	response = requests.post(muse_server+endpoint,
		data=json.dumps(data),headers=headers)

def analyze_intent(text,access_token):
	endpoint = '/nlp/intent/'
	headers = {"Authorization":"Bearer "+access_token}
	data = {"text":text}
	response = requests.post(muse_server+endpoint,
		data=json.dumps(data),headers=headers)
	intent = response.json()['data']['intent']

	labels = []
	scores = []

	for label,score in intent.items():
		labels.append(label)
		scores.append(score)

	best_label = labels[np.argmax(scores)]
	return best_label

if __name__ == '__main__':
	email = raw_input("email: ")
	password = getpass.getpass("password: ")

	access_token = signin(email,password)
	member_id = choose_member(access_token)
	data_source = choose_data_source()

	while True:
		print("USER INPUT")
		text_in = raw_input(" - ")
		intent = analyze_intent(text_in, access_token)
		if intent != 'other':
			text_out = 'Sorry, I cannot understand how to handle %s yet.'%intent
		else:
			candidates = get_candidate_responses(text_in,source=data_source)
		print("TOP 5 RESPONSE CANDIDATES FROM DATA SOURCE "+str(data_source))
		for candidate in candidates[:5]:
			print(' - '+candidate)
		
		
