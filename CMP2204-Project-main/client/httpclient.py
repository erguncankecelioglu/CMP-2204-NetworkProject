import requests

class HTTPClient():
    def __init__(self, url):
        self.url = url
        self.headers = {'Content-Type': 'application/json'}

    def get_chatrooms(self):
        response = requests.get(self.url + '/get-chatrooms', headers=self.headers)
        return response.json()

    def get_dmRooms(self):
        response = requests.get(self.url + '/get-dmRooms', headers=self.headers)
        return response.json()

