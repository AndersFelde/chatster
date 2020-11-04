from tkinter import *
import tkinter.ttk as ttk
from client import Client
import sys


class Gui():
    def __init__(self):
        self.root = Tk()
        self.root.title("Chatster")

        self.root.geometry("400x400")

        self.client = Client(self)
        self.client.connect()

        self.lastRowInt = 0

        self.introGui()

        self.root.mainloop()

    def introGui(self):
        self.content = Frame(self.root)
        self.content.pack()

        usernameFrame = Frame(self.content)
        connectionFrame = Frame(self.content)
        joinFrame = Frame(connectionFrame)
        createFrame = Frame(connectionFrame)
        sep = Label(connectionFrame, text="OR")

        usernameFrame.pack(side=TOP, pady=25)
        connectionFrame.pack()

        createFrame.pack(side=RIGHT, padx=20)
        joinFrame.pack(side=LEFT, padx=20)
        sep.pack(fill=Y, side=BOTTOM, pady=40)
        sep.config(font=("Courier", 20))

        ttk.Style().configure("pad.TEntry", padding="5 2 2 2")

        Label(usernameFrame, text="Username").pack(pady=10)
        self.usernameEntry = ttk.Entry(usernameFrame, style="pad.TEntry")
        self.usernameEntry.pack()

        Label(joinFrame, text="RoomId").pack()
        self.roomIdEntry = ttk.Entry(joinFrame, style="pad.TEntry")
        self.roomIdEntry.pack(pady=10)

        Button(joinFrame, text="Join",
               command=self.joinRoom).pack()

        Button(createFrame, text="Create room",
               command=lambda: self.joinRoom(True)).pack()

        self.errorText = StringVar()
        Label(self.content, textvariable=self.errorText).pack()

        Button(self.content, text="Quit",
               command=lambda: self.quit()).pack()

    def joinRoom(self, new=False):
        username = self.usernameEntry.get()
        if not new:
            try:
                roomId = int(self.roomIdEntry.get())
            except:
                self.errorText.set("Skriv et tall du kanskje")
                return
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

        self.msgInput.bind('<Return>', lambda _: self.sendMsg())

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
