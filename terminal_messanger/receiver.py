# Implementation of unloading and displaying messages from the server.
import time
from datetime import datetime

import requests as requests


def print_message(message):  # Data output form, the simplest interface
    dt = datetime.fromtimestamp(message['time'])
    print(dt.strftime('%H:%M:%S'), message['name'])
    print(message['text'])
    print()


after = 0  # initially "after" is equal to 0, and after it is equal to the time of the last message
# (if there is still 0, then there was no sms yet)
while True:
    # we send a request to the server and wait for a list of messages, in 'after' we write down the time of the last sms
    response = requests.get('http://127.0.0.1:5000/messages', params={'after': after})
    messages = response.json()['messages']  # search by key "messages", because on the server the "messages" function
    # returns a dictionary, and in order to get the list we need, we need to insert the key on which it lies
    # returns the list of messages that we need: [{'name': 'abc', 'text': '456'}]

    if messages:  # checking that "messages" are not empty
        for message in messages:  # displaying messages on the screen
            print_message(message)
        after = messages[-1]['time']  # we take the time value from the last sms in "messages" and put it in "after"
    time.sleep(1)  # sleep, so as not to clog the stream (do not spam the server with requests)
