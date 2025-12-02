import socket
import json

class ClientTaches:
    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port

    def envoyer(self, data):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        s.send(json.dumps(data).encode())
        reponse = s.recv(4096).decode()
        s.close()
        return json.loads(reponse)
