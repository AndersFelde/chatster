from client import Client
from time import sleep

clients = []
for _ in range(10):
    c = Client()
    c.connect()
    c.sendMsg()
    clients.append(c)
    sleep(2)

sleep(10)

for client in clients:
    client.disconnect()

    
