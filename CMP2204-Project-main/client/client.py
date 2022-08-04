from client_helper import ClientHelper
from httpclient import HTTPClient
from user_interface import UserInterface

http_client = HTTPClient('http://localhost:5000')

chat_rooms = http_client.get_chatrooms()
dm_rooms = http_client.get_dmRooms()

interface = UserInterface(http_client)
user_interface = interface.interface()

host = 'localhost'
port = 5001

client = ClientHelper(host, port, user_interface["name"], user_interface)

client.start()