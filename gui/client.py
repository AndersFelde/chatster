import socket
import json
import threading
from time import sleep
from cryptography import fernet
from encryption import Encryption


class Client():
    def __init__(self, gui):
        self.gui = gui

    def connect(self, username="joe", roomId="12346", host="127.0.0.1", port="9001"):
        self.host = host
        self.port = int(port)
        self.key = fernet.Fernet.generate_key()
        print(self.key)
        self.username = username
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.connected = True

            print(self.key)
            self.sock.send(self.key)
            print(self.key)
            print("sendte key")

            self.sock.sendall(Encryption().encryptMsg(self.username, self.key))
            print("sendte username")

            self.sock.sendall(Encryption().encryptMsg(roomId, self.key))
            print(roomId)
            print("sendte roomId")

            msg = self.sock.recv(1024)
            msg = Encryption().decryptMsg(msg, self.key)
            print(msg)

            if msg["msg"] == False:
                self.disconnect()
                return False

            self.clientId, self.roomId = msg["msg"]

            self.thread = threading.Thread(target=self.listen)
            self.thread.start()
            print("Started listening")
            print(self.username, self.roomId, self.clientId)

            return True

        except Exception as e:
            print(e)
            self.disconnect()
            return False

    def sendMsg(self, msg="TEST"):
        try:
            msg = Encryption().encryptMsg(
                msg, self.key)
            self.sock.sendall(msg)

        except Exception as e:
            print(e)
            print("Feil med å sende melding")

    def listen(self):
        sleep(1)
        while True:
            msg = self.sock.recv(1024)
            try:
                msg = Encryption().decryptMsg(msg, self.key)
            except:
                print("Stopped listener")
                break

            if msg["msg"] == "!suicide":
                break

            if msg["clientId"] == self.clientId:
                msg = "You: " + str(msg["msg"])
            else:
                msg = msg["username"] + ": " + msg["msg"]

            self.gui.newMsg(msg)

    def disconnect(self):
        print("lukker sock")
        self.sock.shutdown(socket.SHUT_RDWR)
        # self.sock.send(b"")
        # sender melding til listener
        # self.sock.close()


if __name__ == "__main__":
    print("joe")
