import getpass
import requests
import random
import json

from muse import argsort, signin, get_candidate_responses, choose_data_source, \
	relevance_filter, choose_member

muse_server = 'https://muse.themusio.com/api'


if __name__ == '__main__':
	email = input("email: ")
	password = getpass.getpass("password: ")

	access_token = signin(email,password)
	member_id = choose_member(access_token)
	data_source = choose_data_source()

	count = 0
	text_out_2 = input("Type a seed sentence > ")
	while count < 7:


		candidates_1 = get_candidate_responses(text_out_2,data_source)
		relevance_filter_res = relevance_filter('',text_out_2, [c['text'] for c in candidates_1])
		best_1  = relevance_filter_res['best']
		scores_1 = relevance_filter_res['scores']
		scores_argsort_1 = argsort(scores_1)
		text_out_1 = candidates_1[random.choice(scores_argsort_1[-5:])]['text']


		candidates_2 = get_candidate_responses(text_out_1,data_source)
		relevance_filter_res = relevance_filter('',text_out_1, [c['text'] for c in candidates_2])
		best_2  = relevance_filter_res['best']
		scores_2 = relevance_filter_res['scores']
		scores_argsort_2 = argsort(scores_2)
		text_out_2 = candidates_2[random.choice(scores_argsort_2[-5:])]['text']


		print('bot1', text_out_1)
		print('bot2', text_out_2)
		count += 1
