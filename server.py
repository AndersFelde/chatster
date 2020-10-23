import socket
import threading
import json


class Server:
    def __init__(self, host="127.0.0.1", port="9001", listenInt=5):
        self.host = host
        self.port = int(port)
        self.listenInt = listenInt
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectedClients = {}

    def newClient(self, conn, addr):
        while True:
            msg = conn.recv(1024).decode("utf-8")

            if len(msg) == 0:
                break

            if len(msg) > 0:
                try:
                    msg = json.loads(msg)
                    print(f'{addr}: {str(msg)}')

                    if msg["msg"].lower() == "stop":
                        print("Stoppet server")
                        self.sock.close()
                        break

                    conn.sendall(json.dumps(msg).encode("utf-8"))
                except Exception as e:
                    print(e)
                    break

        conn.close()
        print(f"{addr} stoppet")
        del self.connectedClients[threading.current_thread().ident]
        print(self.connectedClients)

    def run(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.listenInt)
        while True:
            # try:
            conn, addr = self.sock.accept()
            print("Got connection from: ", addr)
            newCon = threading.Thread(target=self.newClient, args=(conn, addr))
            newCon.start()
            self.connectedClients[newCon.ident] = newCon
            print(self.connectedClients)

            # except Exception as e:
            #     print("Connection error:")
            #     print(e)

        self.sock.close()


if __name__ == "__main__":
    s = Server()
    s.run()
