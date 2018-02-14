from config import muse_server
import getpass

import numpy as np
from tqdm import tqdm
import requests
import json

from muse import signin, get_candidate_responses, choose_member, choose_data_source, post_chatlog, analyze_intent
from client_util import is_easy

if __name__ == '__main__':
	email = input("email: ")
	password = getpass.getpass("password: ")

	access_token = signin(email,password)
	member_id = choose_member(access_token)
	data_source = choose_data_source()
	lvl = -1

	with open('starter_sents_level_by_kt_words_leeway.txt','r') as fin:
		lines = fin.read().split('\n')
		sents_in = []
		levels_in = []
		for line in lines:
			_,l,s = line.split('\t')
			sents_in.append(s)
			levels_in.append(l)

	with open('starter_sents_kt_test_res_data_source_%s_lvl_%d.txt'%(str(data_source),lvl),'w') as fout:

		for s,l in tqdm(zip(sents_in,levels_in)):
			text_in = s
			candidates = get_candidate_responses(text_in,source=data_source)
			easy_candidates = []
			for candidate in candidates:
				if is_easy(candidate['text'],lvl):
					easy_candidates.append(candidate)

			outline = '\t'.join([l, text_in] + [c['text'] for c in easy_candidates[:5]])+'\n'
			fout.write(outline)		
		
