import json
import requests
import getpass


from muse import comprehend

if __name__=='__main__':
	while True:
		passage = raw_input('passage> ')
		question = raw_input('question> ')
		print(comprehend(passage,question))