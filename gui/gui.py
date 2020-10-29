from tkinter import *
from client import Client
import sys


class Gui():
    def __init__(self):
        self.root = Tk()
        self.root.title("Chatster")
        self.client = Client(self)
        self.client.connect()

        self.lastRowInt = 0

        self.content = Frame(self.root)
        self.content.pack()

        self.introGui()

        self.root.mainloop()

    def introGui(self):
        Label(self.content, text="Username").grid(row=self.lastRow)
        self.usernameEntry = Entry(self.content)
        self.usernameEntry.grid(row=self.lastRow)

        Label(self.content, text="RoomId").grid(row=self.lastRow)
        self.roomIdEntry = Entry(self.content)
        self.roomIdEntry.grid(row=self.lastRow)

        Button(self.content, text="Join",
               command=self.joinRoom).grid(row=self.lastRow)
        Button(self.content, text="Create room",
               command=lambda: self.joinRoom(True)).grid(row=self.lastRow)

        self.errorText = StringVar()
        Label(self.content, textvariable=self.errorText).grid(row=self.lastRow)

        Button(self.content, text="Quit",
               command=lambda: self.quit()).grid(row=self.lastRow)

    def joinRoom(self, new=False):
        username = self.usernameEntry.get()
        if not new:
            roomId = self.roomIdEntry.get()
        else:
            roomId = 0

        if len(username) == 0 or len(str(roomId)) == 0:
            self.errorText.set("Du må ha noe i begge felt da vettu")
            return

        connection = self.client.joinRoom(username=username, roomId=roomId)
        print(connection)
        if connection != False:
            print("Fikk connection")
            self.renderChat()
            self.client.startListener()
        else:
            self.errorText.set(f"Fant ikke rom med romId: {roomId}")

    def renderChat(self):
        self.content.destroy()

        self.root.title(str(self.client.roomId))

        self.header = Frame(self.root)
        self.header.pack()

        Label(self.header,
              text=f"{self.client.roomId} - {self.client.username}").pack()

        self.content = Frame(self.root)
        self.content.pack()

        self.lastRowInt = 0

        self.chatFrame = Frame(self.content)
        self.chatFrame.pack(side=TOP)

        self.inputFrame = Frame(self.content)
        self.inputFrame.pack(side=BOTTOM)

        self.msgString = StringVar()

        self.msgInput = Entry(self.inputFrame, textvariable=self.msgString)
        self.msgInput.grid(row=0, column=0)

        self.msgBtn = Button(self.inputFrame, text="Send",
                             command=self.sendMsg)
        self.msgBtn.grid(row=0, column=1)

        Button(self.root, text="Quit", command=lambda: self.quit()).pack()

    def sendMsg(self):
        msg = self.msgString.get()
        self.client.sendMsg(msg)
        self.msgString.set("")

    def newMsg(self, msg):
        print(msg)
        Label(self.chatFrame, text=msg).grid(row=self.lastRow)

    def quit(self):
        print("quit")
        if hasattr(self.client, "thread"):
            print("dropper connection")
            self.client.disconnect()
        sys.exit()

    @property
    def lastRow(self):
        self.lastRowInt += 1
        return self.lastRowInt


if __name__ == "__main__":
    Gui()
