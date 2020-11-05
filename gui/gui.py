from tkinter import *
import tkinter.ttk as ttk
from client import Client
from scrollableFrame import ScrollableFrame
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

        self.roomIdEntry.bind('<Return>', lambda _: self.joinRoom())

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
        self.header.grid(row=0)

        Label(self.header,
              text=f"{self.client.roomId} - {self.client.username}").pack()

        # self.content = Frame(self.root, bg="blue")
        # self.content.grid(row=1, column=0, sticky="ew")
        self.lastRowInt = 0

        # self.chatContentFrame = Frame(self.root)
        # self.chatContentFrame.grid(row=1, sticky="ew")
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.chatFrame = Frame(self.root, bg="blue")
        self.chatFrame.grid(row=1, column=0, sticky="NEWS", padx=10, pady=10)

        canvas = Canvas(self.chatFrame, bg="yellow")
        scrollbar = ttk.Scrollbar(
            self.chatFrame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # ttk.Label(self.scrollable_frame, text="Sample scrolling label").pack()

        print("Scrollable la til")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # self.scrollbar = Scrollbar(
        #     self.root, orient="vertical", command=self.chatCanvas.yview)
        # self.scrollbar.grid(row=1, column=1, sticky="ns")
        # self.chatCanvas.configure(yscrollcommand=self.scrollbar.set)

        # self.root.bind(
        #     "<Configure>",
        #     lambda e: self.chatCanvas.configure(
        #         scrollregion=self.chatCanvas.bbox("all")
        #     )
        # )

        # self.chatFrame = Frame(self.chatCanvas)

        # self.chatFrame.grid_columnconfigure(0, weight=1)

        # self.chatCanvas.create_window(
        #     (0, 0), window=self.chatFrame, anchor="nw", tags="frame")

        # self.chatCanvas.bind("<Configure>", self.onCanvasConfigure)

        # self.chatCanvas.config(scrollregion=self.chatCanvas.bbox("all"))

        self.inputFrame = Frame(self.root)
        self.inputFrame.grid(row=2, column=0)

        self.msgString = StringVar()

        self.msgInput = Entry(self.inputFrame, textvariable=self.msgString)
        self.msgInput.pack(side=LEFT)

        self.msgInput.bind('<Return>', lambda _: self.sendMsg())

        self.msgBtn = Button(self.inputFrame, text="Send",
                             command=self.sendMsg)
        self.msgBtn.pack(side=RIGHT)

        Button(self.root, text="Quit", command=lambda: self.quit()).grid(row=3)

    def sendMsg(self):
        msg = self.msgString.get()
        self.client.sendMsg(msg)
        self.msgString.set("")

    def newMsg(self, msg, client=False, color="#000000"):
        if client:
            sticky = "SE"
        else:
            sticky = "SW"

        Label(self.scrollable_frame, text=msg, bg=color).grid(
            row=self.lastRow, column=0, sticky=sticky, pady=5)
        print("la til i scrollable")

        print(msg)

    def quit(self):
        print("quit")
        if hasattr(self.client, "thread"):
            print("dropper connection")
            self.client.disconnect()
        sys.exit()

    @ property
    def lastRow(self):
        self.lastRowInt += 1
        return self.lastRowInt


if __name__ == "__main__":
    Gui()
