from config import muse_server
import getpass

import numpy as np

import requests
import json

from muse import signin, get_candidate_responses, choose_member, choose_data_source, post_chatlog, analyze_intent

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
			print(' - '+candidate['text'])
		
		
