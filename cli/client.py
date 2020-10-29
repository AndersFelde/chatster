import socket
import json
import threading
from cryptography import fernet
from encryption import Encryption


class Client():

    def connect(self, username="joe", roomId="12345", host="127.0.0.1", port="9001"):
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

            msg, roomId = self.__joinRoom()

            while msg["msg"] == False:
                print(f"Fant ikke rom med roomId {roomId}")
                msg, roomId = self.__joinRoom()

            self.clientId, self.roomId = msg["msg"]

            print(f"Din klientId: {self.clientId}\nDin romId: {self.roomId}")

            self.thread = threading.Thread(target=self.listen)
            self.thread.start()

        except Exception as e:
            print("Klarte ikke å koble til\n", e)

    def sendMsg(self, msg="TEST"):
        try:
            msg = Encryption().encryptMsg(
                msg, self.key)
            self.sock.sendall(msg)

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

    def __joinRoom(self):
        print("0 betyr nytt rom")
        roomId = int(input("RoomId: "))
        self.sock.sendall(Encryption().encryptMsg(roomId, self.key))

        msg = self.sock.recv(1024)
        msg = Encryption().decryptMsg(msg, self.key)
        return msg, roomId


if __name__ == "__main__":

    c = Client()
    c.connect()
    c.sendMsg()
