from server_helper import ServerHelper
from httpserver import HTTPServer
import threading

SOCKET_PORT = 5001
SOCKET_HOST = 'localhost'
HTTP_PORT = 5000
HTTP_HOST = 'localhost'

server = ServerHelper(SOCKET_HOST, SOCKET_PORT)
http_server = HTTPServer(HTTP_HOST, HTTP_PORT, server)

socket_thread = threading.Thread(target=server.start)
socket_thread.start()

http_socket = threading.Thread(target=http_server.start)
http_socket.start()