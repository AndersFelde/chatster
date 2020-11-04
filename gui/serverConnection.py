from encryption import Encryption
import threading


class serverConnection():
    def __init__(self, conn, adr, key, room, username):
        self.conn = conn
        self.adr = adr
        self.key = key
        self.room = room
        self.username = username

        self.clientId = self.room.addClient(self)
        self.sendMsg([self.clientId, self.room.roomId])
        self.room.newMsg(self.username + " joined",
                         username=self.username, senderId=self.clientId)

        self.listen()

    def listen(self):
        while True:
            msg = self.conn.recv(1024)

            if len(msg) == 0:
                self.room.newMsg(self.username + " left", username=self.username, senderId=self.clientId)
                self.room.removeClient(self.clientId)
                break

            if len(msg) > 0:
                try:
                    msg = Encryption().decryptMsg(msg, self.key)

                    self.room.newMsg(
                        msg["msg"], username=self.username, senderId=self.clientId)

                except Exception as e:
                    print(e)
                    break

        self.conn.close()
        print(f"{str(self.adr)} stoppet")

    def sendMsg(self, msg, username=None, senderId=None, color=None):
        if username == None and senderId == None:
            username = self.username
            senderId = self.clientId

        msg = Encryption().encryptMsg(msg, self.key, username=username,
                                      senderId=senderId, color=color)
        self.conn.sendall(msg)
