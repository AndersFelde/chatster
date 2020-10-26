import random


class Room():
    def __init__(self):
        self.clients = {}
        self.roomId = random.randint(10000, 99999)

    def addClient(self, client):
        clientId = random.randint(1000, 9999)
        self.clients[clientId] = client
        print(f"Klienter i rom {self.roomId} : {self.clients}")
        return clientId

    def removeClient(self, clientId):
        del self.clients[clientId]
        if len(self.clients) == 0:
            print(f"siste klient forlot {self.roomId}")
            del self

    def newMsg(self, msg, username=None, clientId=None):
        print(str(self.roomId) + ": " + str(msg))
        for idClient in self.clients:
            self.clients[idClient].sendMsg(
                msg, username=username, clientId=clientId)
