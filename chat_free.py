import json
import requests
import getpass

from muse import chat_free, signin, choose_member, choose_bot_emotion



if __name__ == '__main__':
	email = input("email: ")
	password = getpass.getpass("password: ")

	jwt = signin(email,password)
	member_id = choose_member(jwt)

	while True:
		user_text = input('[U] ')
		chat_resp = chat_free(user_text,jwt,member_id)['data']['text_out']['text']

		print('[B]', chat_resp)
