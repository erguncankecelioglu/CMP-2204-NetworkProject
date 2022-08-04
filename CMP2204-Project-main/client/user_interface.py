import random
import uuid

class UserInterface():
    def __init__(self, http_client):
        self.http_client = http_client
        self.chat_rooms = http_client.get_chatrooms()["chatRooms"]
        self.dmRooms = http_client.get_dmRooms()["dmRooms"]
        self.name = None
        self.room = None
        self.user_option = None

    def generate_random_id(self):
        upperCaseLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lowerCaseLetters = "abcdefghijklmnopqrstuvwxyz"
        numbers = "0123456789"
        specialCharacters = "!@#$%^&*()_+"

        pool = [upperCaseLetters, lowerCaseLetters, numbers, specialCharacters]

        random_id = ""
        for i in range(0, 10):
            pool_random_index = random.randint(0, len(pool)-1)
            randomCase_index = random.randint(0, len(pool[pool_random_index])-1)
            random_id += pool[pool_random_index][randomCase_index]

        return random_id

    def enter_name(self):
        self.name = input("Enter your nickname: ")

    def join_or_create(self):
        print("Welcome to the chat!, please choose an option:")
        print("1. Join a chat room")
        print("2. Create a chat room")
        print("3. Create a direct message")
        print("4. Join a direct message")
        self.user_option = input("Choose an option: ")

    def create_room(self):
        print("==========CREATE A CHAT ROOM==========")
        room_name = input("Enter the name of your chat room: ")
        self.room = {"id": str(uuid.uuid1()), "name": room_name}

    def create_dm(self):
        print("==========CREATE A DM==========")
        return self.generate_random_id()

    def list_rooms(self):
        self.chat_rooms = self.http_client.get_chatrooms()["chatRooms"]
        print("==========CHAT ROOMS==========")
        for id in range (len(self.chat_rooms)):
            print(f"{id+1} - {self.chat_rooms[id]['name']}")

        print("==================================")

    def list_dmRooms(self):
        self.dmRooms = self.http_client.get_dmRooms()["dmRooms"]
        print("==========DIRECT MESSAGES==========")
        for id in range (len(self.dmRooms)):
            print(f"{id+1} - {self.dmRooms[id]['dmId']}")

        print("==================================")

    def join_dm_room(self):
        print("==========JOIN A DM==========")
        self.list_dmRooms()
        dm_id = input("Enter the id of your direct message: ")
        self.id = self.dmRooms[int(dm_id)-1]["dmId"]
    
    def join_room(self):
        print("==========JOIN A CHAT ROOM==========")
        self.list_rooms()
        room_id = input("Enter the id of your chat room: ")
        self.room = self.chat_rooms[int(room_id)-1]

    def interface(self):
        self.enter_name()
        self.join_or_create()
        if self.user_option == "1":
            self.join_room()
            return {"name": self.name, "room": self.room, "user_option": self.user_option}
        elif self.user_option == "2":
            self.create_room()
            return {"name": self.name, "room": self.room, "user_option": self.user_option}
        elif self.user_option == "3":
            return {"name": self.name, "dmId": self.create_dm(), "user_option": self.user_option}
        elif self.user_option == "4":
            self.join_dm_room()
            return {"name": self.name, "dmId": self.id, "user_option": self.user_option}
        else:
            print("Invalid option...")  
