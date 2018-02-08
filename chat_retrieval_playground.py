from config import muse_server

import requests
import json

import getpass
import random
import os
import string
import numpy as np

from nltk.corpus import stopwords

from muse import signin, choose_member, choose_data_source, get_candidate_responses, \
	relevance_filter , textual_entailment, coreference_resolution, named_entity, \
	wordvector, similarity, remove_stopwords, has_context_cue, argsort


import matplotlib.pyplot as plt


_, console_width = os.popen('stty size', 'r').read().split()
console_width = int(console_width)


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























