from config import muse_server

import requests
import json

def signin(email,password):
	endpoint = '/auth/signin/'
	data = {'email':email,'password':password}
	response = requests.post(muse_server+endpoint,
		data=json.dumps(data))
	if response.status_code == 200:
		return response.json()['access_token']


