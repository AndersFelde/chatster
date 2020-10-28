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
        self.rooms = {}

    def run(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.listenInt)
        while True:
            # try:
            conn, addr = self.sock.accept()
            print("Got connection from: ", addr)

            newCon = threading.Thread(
                target=self.handleConnection, args=(conn, addr))
            newCon.start()

        self.sock.close()

    def handleConnection(self, conn, addr):
        try:
            key = conn.recv(1024)
            print("fikk key")
            print(key)
            username = Encryption().decryptMsg(conn.recv(1024), key)["msg"]
            print("fikk username")
            print(username)

            roomId = int(Encryption().decryptMsg(conn.recv(1024), key)["msg"])
            print("fikk roomid")
            print(roomId)
            print(self.rooms)

            if roomId == 0:
                room = Room(self)
                roomId = room.roomId
                self.rooms[roomId] = room
                print("lagde rom")
            elif roomId not in self.rooms:
                print("finner ikke rom")
                conn.sendall(Encryption().encryptMsg(False, key))
                print("sendte false")
                return

            room = self.rooms[roomId]

            newCon = threading.Thread(
                target=serverConnection, args=(conn, addr, key, room, username))
            newCon.start()
        except Exception as e:
            print(e)
            print("Det skjedde en feil, klient forlot mest sannsynlig")
            return

    def delRoom(self, roomId):
        if roomId in self.rooms:
            del self.rooms[roomId]


if __name__ == "__main__":
    s = Server()
    s.run()
