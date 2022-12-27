import socket
from _thread import *

class ClientUser:
    def __init__(self, name, addr, connection):
        self.name = name
        self.address = addr
        self.connection = connection


def recieve_data(ClientMultiSocket):
    while True:
        res = ClientMultiSocket.recv(1024)
        if res:
            print(res.decode('utf-8'))

if __name__ == "__main__": 
    clientName = input("Insert Screen Name: ")

    ClientMultiSocket = socket.socket()
    host = '127.0.0.1'
    port = 3000

    print("Waiting for connection response")
    try:
        ClientMultiSocket.connect((host, port))
        print("connected")
    except socket.error as e:
        print(str(e))

    ClientMultiSocket.send(str.encode(clientName))
    
    start_new_thread(recieve_data, (ClientMultiSocket, ))

    while True:
        Input = input("") 
        ClientMultiSocket.send(str.encode(Input))
        

    ClientMultiSocket.close()


