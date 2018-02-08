from config import muse_server

import requests
import json

import getpass
import random
import ipdb
import os
import string
import numpy as np

from nltk.corpus import stopwords

import matplotlib.pyplot as plt

stop = set(stopwords.words('english'))

_, console_width = os.popen('stty size', 'r').read().split()
console_width = int(console_width)


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

def get_candidate_responses(sent,source=1):
	endpoint = '/chat/engine/retrieve/'
	data = {'text':sent,'source':str(source)}
	response = requests.post(muse_server+endpoint,
		data=json.dumps(data))
	candidates = response.json()['data']['candidates']
	return candidates

def relevance_filter(context,sent,candidates):
	endpoint = '/nlp/relevance/multi/'
	data = {'context':context,'text1':sent,'candidates':candidates}
	response = requests.post(muse_server+endpoint,
		data=json.dumps(data))
	return response.json()['data']

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



if __name__ == '__main__':
	email = raw_input("email: ")
	password = getpass.getpass("password: ")

	jwt = signin(email,password)
	member_id = choose_member(jwt)
	data_source = choose_data_source()

	chat_hist = []
	user_utt_hist = []
	bot_utt_hist = []

	while True:
		print("USER INPUT")
		user_sent = raw_input(" - ")

		chat_hist.append(user_sent)
		user_utt_hist.append(user_sent)

		# Resolve coreference on user input for turn 2 and higher
		if len(chat_hist) > 2:
			user_sent = coreference_resolution(chat_hist[-3:-1],user_sent)
		print("COREFERENCE RESOLVED USER INPUT ")
		print(' - '+user_sent)

		# Get potential responses (candidates)
		retrieval_res = get_candidate_responses(user_sent,source=data_source)
		candidates = [c['text'] for c in retrieval_res]
		candidates_score = [c['score'] for c in retrieval_res]
		print("CANDIDATE RESPONSES TOP 5 FROM DATA SOURCE "+str(data_source))
		for i in range(5):
			print(' - [C%d] '%(i+1) + candidates[i])

		# use stopword removed last three utterances up to the current user input as context
		# we could use a smarter method to create the context words for this turn, for example:
		# 1. We can build context words list only if the user sentence includes some 'context cue'
		#    words, like 'it','that','this', etc. 
		# 2. We can only use the context words if the similarity of the past context to the current
		#    input is above a certain threshold, say 0.8
		context = remove_stopwords(' '.join(chat_hist[-4:-1]))
		if similarity(context, user_sent) < 0.8 and not has_context_cue(user_sent):
			context = ''

		print("CONTEXT ")
		print(" - " + context)

		# filter the candidates on context relevance
		relevance_filtered = relevance_filter(context,user_sent,candidates)
		relevance_scores = relevance_filtered['scores']
		candidates_relevance_sorted = [candidates[idx] for idx in argsort(relevance_scores)]

		print("RELEVANCE SCORE SORTED CANDIDATES ")
		for i in range(5):
			print(' - [R%d] '%(i+1) + candidates_relevance_sorted[i])

		if len(bot_utt_hist) > 1:
		# contradiction_measure is a matrix of size num_bot_utterance * num_candidates
		# each element in this matrix holds a "contradiction score" for each of the previous 
		# bot utterance compared to each of the candidate responses for the current user input
		# we can weight the candidate similarity score with the average contradiction score 
		# of each candidate over the past bot utterances.
			contradiction_measures = []
			for bot_utt_past in bot_utt_hist[:-1]:
				textual_entailment_res = textual_entailment([bot_utt_past]*len(candidates),candidates)
				contradiction_probs = [e['label_probs'][1] for e in textual_entailment_res]
				contradiction_measures.append(contradiction_probs)
			contradiction_measures = np.array(contradiction_measures)


			contradiction_filtered_best_idx = np.argmax(
				candidates_score * (1 - np.mean(contradiction_measures,0)))

			bot_sent = candidates[contradiction_filtered_best_idx]
		else:
		# for the first couple turns, randomly select responses from top N relevance sorted 
		# candidates. Here, N=5
			bot_sent = random.choice(candidates_relevance_sorted[:5])


		print('FINAL BOT OUTPUT')
		print(' - ' + bot_sent)

		chat_hist.append(bot_sent)
		bot_utt_hist.append(bot_sent)























