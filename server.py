import socket
import threading
import json
from cryptography import fernet
from encryption import Encryption
from serverConnection import serverConnection
from room import Room


class Server:
    def __init__(self, host="127.0.0.1", port="9001", listenInt=5):
        self.host = host
        self.port = int(port)
        self.listenInt = listenInt
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectedClients = {}
        self.rooms = {}

    def run(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.listenInt)
        while True:
            # try:
            conn, addr = self.sock.accept()
            print("Got connection from: ", addr)

            key = conn.recv(1024)

            username = Encryption().decryptMsg(conn.recv(1024), key)["msg"]

            roomId = Encryption().decryptMsg(conn.recv(1024), key)["msg"]
            print(str(addr) + "Valgte rom id: " + str(roomId))

            print(self.rooms)

            if roomId in self.rooms:
                room = self.rooms[roomId]
            else:
                room = Room()
                self.rooms[room.roomId] = room
                print("Fant ikke rom, ny id: " + str(room.roomId))

            newCon = threading.Thread(
                target=serverConnection, args=(conn, addr, key, room, username))
            newCon.start()

            # except Exception as e:
            #     print("Connection error:")
            #     print(e)

        self.sock.close()


if __name__ == "__main__":
    s = Server()
    s.run()
