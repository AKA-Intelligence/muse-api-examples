import string
import json
import random

import requests
import getpass
import numpy as np
from nltk.corpus import stopwords


muse_server = 'https://muse.themusio.com/api'
stop = set(stopwords.words('english'))

# auth / user model
def post_chatlog(member_id,text_in,text_out,access_token):
	endpoint = '/chatlog/%s/'%str(member_id)
	headers = {"Authorization":"Bearer "+access_token}
	data = {"text_in":text_in,"text_out":text_out}
	response = requests.post(muse_server+endpoint,
		data=json.dumps(data),headers=headers)

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


# client util
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


def choose_bot_emotion():
	options = ['neutral', 'anger', 'joy', 'fear', 'sadness']
	def print_options():
		print("Choose bot emotion. Options are: neutral, anger, joy, fear, sadness")
	print_options()
	bot_emotion = str(raw_input('bot emotion> '))
	while bot_emotion not in options:
		print "Not a valid bot emotion."
		print_options()
		bot_emotion = str(raw_input('bot emotion> '))
	return bot_emotion


# chat
## pre-made free chat
def chat_free(user_text,jwt,member_id):
	endpoint = muse_server + '/chat/'
	data = {'user_text':user_text,'member_id':member_id}
	headers = {'content-type':'application/json',
			   'Authorization':'Bearer '+jwt}
	resp = requests.post(endpoint,
		data=json.dumps(data),
		headers=headers)
	return resp.json()		

## pre-made scripted chat
def chat_scripted(user_text,jwt,member_id):
	endpoint = muse_server + '/scripted/'
	data = {'user_text':user_text,'member_id':member_id}
	headers = {'content-type':'application/json',
			   'Authorization':'Bearer '+jwt}
	resp = requests.post(endpoint,
		data=json.dumps(data),
		headers=headers)
	return resp.json()		

## generative model
def chat_generate(context,bot_emotion,jwt,member_id):
	headers = {'Authorization':'Bearer '+jwt}
	context = context[-3:]
	data = {'context':context,'emotion':bot_emotion}
	res = requests.post(muse_server+'/chat/generate/',json=data, headers=headers)
	return res.json()['data']['response']

## retrieval model
def get_candidate_responses(sent,source='1'):
	endpoint = '/chat/engine/retrieve/'
	data = {'text':sent,'source':str(source)}
	response = requests.post(muse_server+endpoint,
		data=json.dumps(data))
	candidates = response.json()['data']['candidates']
	candidates_text = [candidate['text'] for candidate in candidates]
	return candidates

## contextual question retriever
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


# nlp
def comprehend(passage,question):
	data = {'passages':[passage],'questions':[question]}
	res = requests.post(muse_server+'/nlp/machine-comprehension/',json=data)
	return res.json()[0]['best_span_str']

def relevance_filter(context,sent,candidates):
	endpoint = '/nlp/relevance/multi/'
	data = {'context':context,'text1':sent,'candidates':candidates}
	response = requests.post(muse_server+endpoint,
		data=json.dumps(data))
	return response.json()['data']


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

def textual_entailment(premises,hypotheses):
	endpoint = '/nlp/textual-entailment/'
	data = {'premises':premises,'hypotheses':hypotheses}
	response = requests.post(muse_server+endpoint,
		data=json.dumps(data))
	return response.json()

def coreference_resolution(context,utterance):
	endpoint = '/nlp/neuralcoref/'
	data = {"context":context,"utterances":[utterance]}
	response = requests.post(muse_server+endpoint,
		data=json.dumps(data))
	return response.json()['resolved'][0]

def named_entity(text):
	endpoint = '/nlp/namedentity/'
	data = {"text":text}
	response = requests.post(muse_server+endpoint,
		data=json.dumps(data))
	return response.json()['data']['named_entities']

def wordvector(text):
	endpoint = '/nlp/wordvector/'
	data = {"text":text}
	response = requests.post(muse_server+endpoint,
		data=json.dumps(data))
	return response.json()['data']['vector']


# helper functions

def similarity(text1,text2):
	v1 = np.array(wordvector(text1))
	v2 = np.array(wordvector(text2))
	v1_normalized = v1/np.sqrt(v1.dot(v1))
	v2_normalized = v2/np.sqrt(v2.dot(v2))
	cosine_similarity = v1_normalized.dot(v2_normalized)
	return cosine_similarity

def remove_stopwords(text):
	for spchr in string.punctuation:
		text = text.replace(spchr,' ')
	tokens = text.split()
	return ' '.join([token for token in tokens if token.lower() not in stop])

def has_context_cue(text):
	tokens = text.split()
	context_cues = ['it','this','that','those','these'] # etc.
	if any([token in context_cues for token in tokens]):
		return True
	else:
		return False


def argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)

