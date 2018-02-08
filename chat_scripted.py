import json
import requests
import getpass

from muse import signin, chat_scripted, choose_member
muse_server = 'https://muse.themusio.com/api'


if __name__ == '__main__':
	email = raw_input("email: ")
	password = getpass.getpass("password: ")

	jwt = signin(email,password)
	member_id = choose_member(jwt)

	while True:
		user_text = raw_input('[U] ')
		chat_resp = chat_scripted(user_text,jwt,member_id)['data']['lines_out']


		for line in chat_resp:
			print '[B]', line['line']