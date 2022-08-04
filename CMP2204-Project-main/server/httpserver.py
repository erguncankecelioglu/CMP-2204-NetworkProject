from flask import Flask
import json

app = Flask(__name__)

class HTTPServer():
    def __init__(self, host, port, server):
        self.host = host
        self.port = port
        self.server = server

        self.init()

    def init(self):
        self.chat_rooms()

    def start(self):
        app.run(host=self.host, port=self.port)

    def stop(self):
        pass

    def chirp(self, payload, status):
        resp = app.response_class(
            response=json.dumps(payload),
            status=status,
            mimetype="application/json",
        )
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Headers"] = "*"
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["X-Frame-Options"] = "SAMEORIGIN"
        resp.headers["X-XSS-Protection"] = "1"

        return resp

    def get_chatrooms(self):
        response = {}
        response["chatRooms"] = self.server.chat_rooms
        return self.chirp(response, 200)

    def get_dmRooms(self):
        response = {}
        response["dmRooms"] = self.server.dms
        return self.chirp(response, 200)

    def chat_rooms(self):
        app.add_url_rule("/get-chatrooms", view_func=self.get_chatrooms)
        app.add_url_rule("/get-dmRooms", view_func=self.get_dmRooms)