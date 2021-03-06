import json
import requests
import getpass

from muse import signin, chat_scripted_kt, choose_member


if __name__ == '__main__':
    email = input("email: ")
    password = getpass.getpass("password: ")

    jwt = signin(email,password)
    member_id = choose_member(jwt)
    story_id = input('choose story id options are: horse, school_boy, dog, pizza, dinner, kite, puppy> ')

    while True:
        user_text = input('[U] ')
        chat_resp = chat_scripted_kt(user_text,jwt,member_id,story_id)

        for line in chat_resp['data']['lines_out']:
            print('[B]', line['line'])
        print("YOUR CHOICES ARE:")
        for c in chat_resp['data']['choices']:
            print(' - %s'%c)
