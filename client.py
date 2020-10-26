import socket
import json
import threading
from cryptography import fernet
from encryption import Encryption


class Client():

    def connect(self, host="127.0.0.1", port="9001"):
        self.host = host
        self.port = int(port)
        self.key = fernet.Fernet.generate_key()
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.connected = True

            self.sock.sendall(self.key)

            self.username = str(input("Username: "))
            self.sock.sendall(Encryption().encryptMsg(self.username, self.key))

            roomId = int(input("RoomId: "))
            self.sock.sendall(Encryption().encryptMsg(roomId, self.key))

            msg = self.sock.recv(1024)
            self.clientId, self.roomId = list(
                Encryption().decryptMsg(msg, self.key)["msg"])
            print(self.clientId, self.roomId)

            self.thread = threading.Thread(target=self.listen)
            self.thread.start()

        except Exception as e:
            print("Klarte ikke å koble til\n", e)

    def sendMsg(self, msg="TEST"):
        try:
            msg = Encryption().encryptMsg(
                msg, self.key, username=self.username, clientId=self.clientId)
            self.sock.sendall(msg)

            # response = self.sock.recv(1024)
            # response = Encryption().decryptMsg(response, self.key)
            # print(response)
        except Exception as e:
            print(e)
            print("Feil med å sende melding")

    def listen(self):
        while True:
            msg = self.sock.recv(1024)
            msg = Encryption().decryptMsg(msg, self.key)
            if msg["clientId"] == self.clientId:
                print("You: " + str(msg["msg"]))
            else:
                print(msg["username"] + ": " + msg["msg"])

    def disconnect(self):
        self.sock.close()


if __name__ == "__main__":

    c = Client()
    c.connect()
    c.sendMsg()
