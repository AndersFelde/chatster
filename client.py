import socket
import json


class Client():

    def connect(self, host="127.0.0.1", port="9001"):
        self.host = host
        self.port = int(port)
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.connected = True
        except Exception as e:
            print("Klarte ikke å koble til\n", e)

    def sendMsg(self, msg="TEST"):
        msgDict = json.dumps({
            "msg": msg,
            "code": 321
        })
        try:
            self.sock.sendall(msgDict.encode("utf-8"))
            response = json.loads(self.sock.recv(1024).decode("utf-8"))
            print(response)
        except Exception as e:
            print(e)
            print("Feil med å sende melding")

    def disconnect(self):
        self.sock.close()


if __name__ == "__main__":

    c = Client()
    c.connect()
    c.sendMsg()
