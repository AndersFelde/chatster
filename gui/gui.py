from tkinter import *
from client import Client
import sys


class Gui():
    def __init__(self):
        self.root = Tk()
        self.root.title("Chatster")
        self.client = Client(self)
        self.lastRowInt = 0

        self.content = Frame(self.root)
        self.content.pack()

        self.introGui()

        Button(self.root, text="Quit", command=lambda: self.quit()).pack()

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

    def joinRoom(self, new=False):
        username = self.usernameEntry.get()
        if not new:
            roomId = self.roomIdEntry.get()
        else:
            roomId = 0

        connection = self.client.connect(username=username, roomId=roomId)
        print(connection)
        if connection != False:
            print("Fikk connection")
            self.renderChat()
        else:
            self.errorText.set(f"Fant ikke rom med romId: {roomId}")

    def renderChat(self):
        self.root.title(str(self.client.roomId))

        self.content.destroy()
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
