import time
from flask import Flask, request, abort

app = Flask(__name__)
# the database that everyone will access is declared globally for the entire server
# in this example, after the server is closed, the history is erased
db = [
    {
        'name': 'Jack',
        'text': 'Hello',
        'time': 0.1  # we do not use time.time () for bots for the reason that after the server crashes and returns
        # to life, the time is updated, which we do not need
    },
    {
        'name': 'Mary',
        'text': 'Jack',
        'time': 0.2
    }
]


def users():  # function of counting unique (all possible) users
    users_set = []
    for user in db:
        users_set.append(user['name'])
    return len(set(users_set))


def text_count():  # function for counting the total number of messages
    texts = 0
    for text in db:
        if text:
            texts += 1
    return texts


@app.route("/")  # main page
def hello():
    return "Welcome!"


@app.route("/status")  # Status page
def status():
    info = {
        'status': True,  # current server status
        'name': 'Baskage',  # the name of the messenger itself
        'time': time.asctime(),  # current time on the server
        'users': users(),  # call to the function of counting all users
        'sms_counter': text_count()  # call the function of counting all messages on the server at the current moment
    }

    return info  # return for reading via json


@app.route("/send", methods=['POST'])  # the function accepts requests for URL/send and only accepts a POST method
# request (to tell Flask that you cannot request anything with a submit method, only for transmission)
def send():
    data = request.json  # A Flask object that will put information into a "data" variable before starting the "send"
    # function, which is present in our request from the client - sender.py (via the post method)
    # That is, we send data in the sender.py file via "response", and the server in "data = request.json" receives this
    # data and further this data can be controlled
    if not isinstance(data, dict):  # checking for data incompatibility with the dictionary type
        return abort(400)  # return an error (abort the request), abort  is in Flask. That is, the server does not
        # crashes when an error is raised and we handle this situation well with the dictionary.

    if 'name' not in data or 'text' not in data:  # if there are not enough keys
        return abort(400)  # we also throw a 400th error

    # take values by keys for further operations with these values
    name = data['name']
    text = data['text']

    if not isinstance(name, str) or not isinstance(text, str):  # checking that the name and text are both a string
        return abort(400)
    if not 0 < len(name) <= 20:  # name limit, no more than 20 characters
        return abort(400)
    if not 0 < len(text) <= 6000:  # message length restrictions
        return abort(400)

    # if the data has been validated, it goes to the Database
    db.append({
        'name': name,
        'text': text,
        'time': time.time()
    })

    return {}


@app.route("/messages")  # collection of messages
def messages():  # function of returning messages from the server (unloading them)
    try:  # check if "after" is passed validly
        after = float(request.args['after'])  # takes the value of the parameter from the link, what we get will be in
        # str format, needs to be converted to float so that boolean operations can be performed

    except:  # if after is invalid and causes an error, we translate it to 400 so that the server does not crash
        return abort(400)

    filtered_messages = []
    for message in db:
        if message['time'] > after:  # filtering messages by time, to display relevant (new) messages
            filtered_messages.append(message)

    return {
        'messages': filtered_messages[:50]}  # the list cannot be displayed in return, so we put the list into the
    # dictionary.
    # We load up to 50 messages at a time so as not to load the server


if __name__ == '__main__':
    app.run()  # server start
