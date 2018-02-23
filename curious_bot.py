import requests
import json
import getpass

muse_server = 'https://muse.themusio.com/api'

from muse import signin, get_contextual_question


if __name__ == "__main__":
	email = input("email: ")
	password = getpass.getpass("password: ")

	jwt = signin(email,password)

	used_question_ids = []
	while True:
		user_sent = input("What would you like me to ask you about? > ")
		question, question_id = get_contextual_question(user_sent, used_question_ids, jwt)
		used_question_ids.append(question_id)
		print(question)
