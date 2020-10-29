import socket
import json
import threading
from time import sleep
from cryptography import fernet
from encryption import Encryption


class Client():
    def __init__(self, gui):
        self.gui = gui

    def connect(self, host="127.0.0.1", port="9001"):
        self.host = host
        self.port = int(port)
        self.key = fernet.Fernet.generate_key()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.connected = True

        self.sock.send(self.key)

    def joinRoom(self, username="joe", roomId="12346"):
        if self.connected:
            self.username = username
            try:

                self.sock.sendall(Encryption().encryptMsg(
                    self.username, self.key))

                self.sock.sendall(Encryption().encryptMsg(roomId, self.key))

                msg = self.sock.recv(1024)
                msg = Encryption().decryptMsg(msg, self.key)

                if msg["msg"] == False:
                    return False

                self.clientId, self.roomId = msg["msg"]

                return True

            except Exception as e:
                print(e)
                return False
        else:
            print("Not connected")
            return False

    def sendMsg(self, msg="TEST"):
        try:
            msg = Encryption().encryptMsg(
                msg, self.key)
            self.sock.sendall(msg)

        except Exception as e:
            print(e)
            print("Feil med å sende melding")

    def startListener(self):
        self.thread = threading.Thread(target=self.listen)
        self.thread.start()
        print("Started listening")
        print(self.username, self.roomId, self.clientId)

    def listen(self):
        while True:
            msg = self.sock.recv(1024)
            try:
                msg = Encryption().decryptMsg(msg, self.key)
            except:
                print("Stopped listener")
                self.disconnect()
                break

            if msg["clientId"] == self.clientId:
                msg = "You: " + str(msg["msg"])
            else:
                msg = msg["username"] + ": " + msg["msg"]

            self.gui.newMsg(msg)

    def disconnect(self):
        print("lukker sock")
        if self.connected:
            self.connected = False
            self.sock.shutdown(socket.SHUT_RDWR)
        # self.sock.send(b"")
        # sender melding til listener
        # self.sock.close()


if __name__ == "__main__":
    print("joe")
