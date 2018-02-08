import json
import requests
import getpass

muse_server = 'https://muse.themusio.com/api'

def comprehend(passage,question):
	data = {'passages':[passage],'questions':[question]}
	res = requests.post(muse_server+'/nlp/machine-comprehension/',json=data)
	print("answer: "+res.json()[0]['best_span_str'])

if __name__=='__main__':
	while True:
		passage = raw_input('passage> ')
		question = raw_input('question> ')
		comprehend(passage,question)