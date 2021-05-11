# Data transfer is carried out via a URL, in case of a different location of the server and the sender.
import requests as requests

name = input('Enter your name: ')  # entering the sender's name once

while True:  # the message sending loop runs non-stop
    # json, which we send from the client to the server
    data = {'name': name,
            'text': input('>>> ')}  # the text of the message that the user enters through the console

    response = requests.post('http://127.0.0.1:5000/send',  json=data)  # sending data to URL/send,
    # /send - accepts messages

