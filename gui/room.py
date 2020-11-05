import random


class Room():
    def __init__(self, server):
        self.clients = {}
        self.roomId = random.randint(10000, 99999)
        self.server = server
        self.colorPallete = ["#264653", "#2a9d8f",
                             "#e9c46a", "#f4a261", "#e76f51"]
        self.colorInt = 0

    def addClient(self, client):
        clientId = random.randint(1000, 9999)
        self.clients[clientId] = {"client": client, "color": self.nextColor}
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
            self.clients[clientId]["client"].sendMsg(
                msg, username=username, senderId=senderId, color=self.clients[senderId]["color"])

    @property
    def nextColor(self):
        self.colorInt += 1
        if self.colorInt < len(self.colorPallete):
            return self.colorPallete[self.colorInt]
        else:
            self.colorInt = 0
            return self.colorPallete[self.colorInt]
