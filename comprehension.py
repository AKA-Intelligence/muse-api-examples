import json
import requests
import getpass


from muse import comprehend

if __name__=='__main__':
	while True:
		passage = input('passage> ')
		question = input('question> ')
		print(comprehend(passage,question))
