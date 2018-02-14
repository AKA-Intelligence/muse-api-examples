import ipdb
import json
import requests
import getpass

from muse import chat_kt, signin, choose_member, choose_bot_emotion, choose_level, get_candidate_responses, get_contextual_question
from client_util import is_easy


if __name__ == '__main__':
	email = input("email: ")
	password = getpass.getpass("password: ")

	jwt = signin(email,password)
	member_id = choose_member(jwt)
	level = int(choose_level())
	topic = input('topic> ')
	user_utts_hist = []
	used_question_ids = []

	while True:
		user_text = input(' [U] ')
		user_utts_hist.append(user_text)

		chat_res = chat_kt(user_text,jwt,member_id,topic,level)

		text_out = chat_res['data']['text_out']['text']
		suggested_responses = chat_res['data']['suggested_responses']
		bot_emotion = chat_res['data']['emotion']['bot']['emotion']

		print(' [B]' + '(%s) '%bot_emotion + text_out)
		print("You can try saying..")
		for c in suggested_responses[:5]:
			print(' - '+c['text'])
