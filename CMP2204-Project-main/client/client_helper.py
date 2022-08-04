import socket
import threading
import uuid
import json

class ClientHelper:
    def __init__(self, host, port, nickname, useroptions):
        self.host = host
        self.port = port
        self.nickname = nickname
        self.client = None
        self.id = ""
        self.useroptions = useroptions

        self.init()

    def generate_uuid(self):
        return str(uuid.uuid1())

    def init(self):
        self.id = self.generate_uuid()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

    def write(self):
        while True:
            content = f'{self.nickname}: {input("You: ")}'
            messageObj = {"userId": self.id, "message": content, "chatRoom": ""}
            self.client.send(str(messageObj).encode('ascii'))

    def receive(self):
        while True:
            try:
                message = self.client.recv(8192).decode('ascii')
                if message == 'NICK':
                    messageObj = self.prepareMessage()
                    self.client.send(str(messageObj).encode('ascii'))
                else:
                    try:
                        messageObj = self.loadJson(message)
                        print(messageObj["message"])
                    except:
                        print(message)
            except:
                print('Lost connection to the server')
                self.client.close()
                break

    def prepareMessage(self):
        options = {}
        if self.useroptions["user_option"] == '2':
            options = {"userId": self.id, "nickname": self.nickname, "chatRoom": self.useroptions["room"]["id"], "room_name": self.useroptions["room"]["name"], "userOption": self.useroptions}
        elif self.useroptions["user_option"] == '1':
            options = {"userId": self.id, "nickname": self.nickname, "chatRoom": self.useroptions["room"]["id"], "room_name": self.useroptions["room"]["name"], "userOption": self.useroptions}
        elif self.useroptions["user_option"] == '3':
            options = {"userId": self.id, "nickname": self.nickname, "dmId": self.useroptions["dmId"], "userOption": self.useroptions}
        elif self.useroptions["user_option"] == '4':
            options = {"userId": self.id, "nickname": self.nickname, "dmId": self.useroptions["dmId"], "userOption": self.useroptions}
        return options

    def loadJson(self, message):
        new_message = message.replace("'", '"')
        return json.loads(new_message)

    def start(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()