import json
import requests
import getpass

from muse import signin, choose_member, choose_bot_emotion, chat_generate

if __name__ == '__main__':
	email = input("email: ")
	password = getpass.getpass("password: ")

	jwt = signin(email,password)
	member_id = choose_member(jwt)
	bot_emotion = choose_bot_emotion()

	chat_hist = []

	while True:
		user_text = input('[U] ')

		chat_hist = chat_hist + [user_text]

		resp_generative = chat_generate(
			context=chat_hist,
			bot_emotion=bot_emotion,
			jwt=jwt,
			member_id=member_id)

		chat_hist = chat_hist + [resp_generative]

		print('[B]', resp_generative)
