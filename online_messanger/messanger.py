# Messenger launch file. Connecting functions to the graphical interface.
import requests
import clientui
from datetime import datetime
from PyQt6 import QtWidgets, QtCore


class Messanger(QtWidgets.QMainWindow, clientui.Ui_MainWindow):  # we create a class and inherit from "QMainWindow",
    # which stores all window properties, and "Ui_MainWindow" of our interface file
    # (isolated the code from the design so as not to lose code)
    def __init__(self, server_url):  # when initializing the object, we accept the link where the server will be located
        super().__init__()
        self.setupUi(self)
        self.server_url = server_url  # save url

        self.pushButton.pressed.connect(self.send_message)  # configuring the send message button
        self.after = 0  # set "after" to the beginning of the conversation
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)  # we use a timer to send a get request to the server every second
        self.timer.start(1000)

    # Data output form and connection to the data output field, which was drawn in the interface
    def print_message(self, message):
        dt = datetime.fromtimestamp(message['time'])
        dt_str = dt.strftime('%H:%M:%S')
        self.textBrowser.append(dt_str + ' ' + message['name'])  # instead print -> textBrowser - adds new data to the
        # end of existing data. The old ones rise, the new ones come from below
        self.textBrowser.append(message['text'])
        self.textBrowser.append('')

    # takes the variable "after" and looks for new messages on the server, the server checks if there are any fresh
    # messages (so that "after" is more than what we send to the server), inside the program we receive our messages
    # from the server (if there are ), print messages and update the "after" variable (if new messages were received)
    def get_messages(self):
        try:
            # we send a request to the server and wait for a list of messages
            response = requests.get(self.server_url + '/messages', params={'after': self.after})  # we write down the
            # time of the last message
        except:
            return  # in case of error, just exit this function
        messages = response.json()['messages']  # search by key "messages", because on the server the "messages"
        # function returns a dictionary, and to get the desired list, we need to insert the key on which it lies
        if messages:  # checking that messages is not empty
            for message in messages:  # we go through the messages and display each of them on the screen
                self.print_message(message)
            self.after = messages[-1]['time']  # we take the time value from the last message in "messages"
            # and put it in "after"

    def send_message(self):
        # json, which we send from the client to the server,
        data = {'name': self.lineEdit.text(),  # takes the name from the field(lineEdit in the interface)
                'text': self.textEdit.toPlainText()}  # the text of the message that the user enters into "textEdit"
        # is sent to the "toPlainText" function, and it translates everything to one line
        try:  # in case of server shutdown during sending
            response = requests.post(self.server_url + '/send', json=data)  # /send accepts different sms,
            # sending data to /send
        except:  # In case of loss of connection with the server
            self.textBrowser.append('Server is not available')
            self.textBrowser.append('')
            return  # we do "return", because the entered text does not need to be cleared
        if response.status_code != 200:  # if the server did not accept our message because we tried
            # to send invalid data to it
            self.textBrowser.append('Validation error')  # you can describe in more detail what
            # is connected with (name, text ..)
            self.textBrowser.append('')
            return

        self.textEdit.clear()  # clearing the input field after sending the message so that no text remains.
        # If sending is successful, the text will be removed.


app = QtWidgets.QApplication([])  # создание объекта интерфейса
window = Messanger(server_url='https://5097fd556c75.ngrok.io')  # creating a messenger object with sending a global
# link that the user can follow, in this example the site ngrok.com was used to create such a link
window.show()  # Showing our Messanger
app.exec()  # starts the main GUI event loop. The main loop waiting for user actions (events)
# and receives events and dispatches them to objects.
