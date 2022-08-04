import socket
import threading
import json

class ServerHelper:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.chat_rooms = [] #? {"id": "", name: "", users: []}
        self.clients = [] #? {client: "", userId: ""}
        self.users = [] #? {"userId": "", "nickname": "", client: ""}
        self.server = None
        self.dms = [] #? {"users": [], "dmId": ""}

        self.init()

    def init(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

    def dmBroadcast(self, message, userId, dmId):
        receiver = ""
        for dm in self.dms:
            if dm["dmId"] == dmId:
                for user in dm["users"]:
                    if user["userId"] != userId:
                        receiver = user["userId"]
                        break

        client = self.getDmClient(receiver)
        if client:
            client.send(message)

    #! ? message = {userId: "", message: ""}
    def broadcast(self, message, roomId, userId):
        clients = self.getClients(roomId, userId)
        for client in clients:
            client.send(message)

    def get_chat_room(self, id):
        for chat_room in self.chat_rooms:
            if chat_room["id"] == id:
                return chat_room
        return None

    def handle(self, client, ids, userId, userOption):
        while True:
            try:
                message = client.recv(1024)
                if userOption == "1" or userOption == "2":
                    self.broadcast(message, ids, userId)
                elif userOption == "3" or userOption == "4":
                    self.dmBroadcast(message, userId, ids)
            except Exception as e:
                print(e)
                break

    def receive(self):
        while True:
            client, addr = self.server.accept()
            print(f'Connected with {addr}')

            client.send('NICK'.encode('ascii'))

            user = client.recv(8192).decode('ascii')
            user = self.loadJson(user)
            if user["userOption"]["user_option"] == "1" or user["userOption"]["user_option"] == "2":
                self.setChatRoom(user["chatRoom"], user, user["room_name"])
                self.clients.append({"client": client, "chatRoom": user["chatRoom"], "userId": user["userId"]})
                print(f'Nickname is {user["nickname"]}')
                self.broadcast(f'{user["nickname"]} joined the chat'.encode('ascii'), user["chatRoom"], user["userId"])
                client.send('Connected to the server.'.encode('ascii'))
                thread = threading.Thread(target=self.handle, args=(client,user["chatRoom"], user["userId"], user["userOption"]["user_option"], ))
                thread.start()
            elif user["userOption"]["user_option"] == "3" or user["userOption"]["user_option"] == "4":
                if user["userOption"]["user_option"] == "3":
                    self.dms.append({"users": [user], "dmId": user["dmId"]})
                    self.clients.append({"client": client, "userId": user["userId"]})
                    client.send(f'Connected to the server. \nYour DM Id: {user["dmId"]}'.encode('ascii'))
                    thread = threading.Thread(target=self.handle, args=(client,user["dmId"], user["userId"], user["userOption"]["user_option"], ))
                    thread.start()
                else:
                    set_result = self.setDmRoom(user, user["dmId"])
                    if set_result:
                        self.clients.append({"client": client, "userId": user["userId"]})
                        client.send(f'Connected to the server. \nYour DM Id: {user["dmId"]}'.encode('ascii'))
                        thread = threading.Thread(target=self.handle, args=(client,user["dmId"], user["userId"], user["userOption"]["user_option"], ))
                        thread.start()

    def getClients(self, roomId, userId):
        clients = []
        for client in self.clients:
            if client["chatRoom"] in roomId and client["userId"] != userId:
                clients.append(client["client"])

        return clients
    
    def getDmClient(self, userId):
        for client in self.clients:
            if client["userId"] == userId:
                return client["client"]
        return None

    def setChatRoom(self, roomId, user, roomName):
        checkRoom = self.checkRoomIsExist(roomId)
        if checkRoom:
            for room in self.chat_rooms:
                if room["id"] == roomId:
                    room["users"].append(user)
        else:
            self.chat_rooms.append({"id": roomId, "name": roomName, "users": [user]})

    def setDmRoom(self, user, dmId):
        for dm in self.dms:
            if dm["dmId"] == dmId and len(dm["users"]) < 2:
                dm["users"].append(user)
                return True
        return False

    def checkRoomIsExist(self, roomId):
        for room in self.chat_rooms:
            if room["id"] == roomId:
                return True
        return False

    def loadJson(self, message):
        new_message = message.replace("'", '"')
        return json.loads(new_message)

    def start(self):
        print('Server is listening on port ' + str(self.port))
        self.receive()