import json
import requests
import getpass
import random

from muse_util import muse_server, signin, choose_member

def argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)

def get_candidate_responses(sent,access_token):
    endpoint = "/chat/engine/retrieve/default/"
    data = {"text":sent}
    headers = {"Authorization":"Bearer "+access_token}
    response = requests.post(muse_server+endpoint,
                             data=json.dumps(data),
                             headers=headers)
    candidates = response.json()["data"]["candidates"]
    candidates_text = [candidate["text"] for candidate in candidates]
    return candidates_text

def filter_responses(sent,candidates,access_token):
    endpoint = "/nlp/relevance/multi/"
    data = {"text1":sent,"candidates":candidates}
    headers = {"Authorization":"Bearer "+access_token}
    response = requests.post(muse_server+endpoint,
                             data=json.dumps(data),
                             headers=headers)
    best_response = response.json()["data"]["best"]
    candidate_scores = response.json()["data"]["scores"]
    return best_response, candidate_scores

def main():
    max_turns = 10
    email = raw_input("email: ")
    password = getpass.getpass("password: ")
    access_token = signin(email,password)
    member_id = choose_member(access_token)
    count = 0
    text_out_2 = raw_input("Type a seed sentence > ")
    
    while count < max_turns:
        candidates_1 = get_candidate_responses(text_out_2,access_token)
        best_1, scores_1 = filter_responses(text_out_2,candidates_1,access_token)
        scores_argsort_1 = argsort(scores_1)
        text_out_1 = candidates_1[random.choice(scores_argsort_1[-5:])]

        candidates_2 = get_candidate_responses(text_out_1,access_token)
        best_2, scores_2 = filter_responses(text_out_1,candidates_2,access_token)
        scores_argsort_2 = argsort(scores_2)
        text_out_2 = candidates_2[random.choice(scores_argsort_2[-5:])]

        print "[BOT1]", text_out_1
        print "[BOT2]", text_out_2
        count += 1

if __name__ == "__main__":
    main()