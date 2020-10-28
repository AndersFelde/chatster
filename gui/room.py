import random


class Room():
    def __init__(self, server):
        self.clients = {}
        self.roomId = random.randint(10000, 99999)
        self.server = server

    def addClient(self, client):
        clientId = random.randint(1000, 9999)
        self.clients[clientId] = client
        print(f"Klienter i rom {self.roomId} : {self.clients}")
        return clientId

    def removeClient(self, clientId):
        del self.clients[clientId]
        if len(self.clients) == 0:
            print(f"siste klient forlot {self.roomId}")
            self.server.delRoom(self.roomId)
            del self

    def newMsg(self, msg, username=None, senderId=None):
        for clientId in self.clients:
            self.clients[clientId].sendMsg(
                msg, username=username, senderId=senderId)
