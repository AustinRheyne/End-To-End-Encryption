import socket
import os
from _thread import *
from client import ClientUser

ServerSideSocket = socket.socket()
host = "127.0.0.1"
port = 3000
ThreadCount = 0
Clients = []

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print("Socket is listening...")
ServerSideSocket.listen(5)

def serverCommand():
    while True:
        command = input()
        if command == "client count":
            print(ThreadCount)
            print(Clients)

def multi_threaded_client(connection, addr, localUser):
    connection.sendall(str.encode(f'// Connected to server {host}:{port} // \n'))

    while True:
        try:
            data = connection.recv(2048)
            message = f"{localUser.name}: {data.decode('utf-8')}"

            if not data:
                print(f"NO DATA FROM {localUser.name}")
                disconnect(connection, addr, localUser.name)
                break
            
            send_to_other_clients(localUser, message)
        except error as e:
            print(e)
            print(f"ERROR FROM {localUser.name}")
            disconnect(connection, addr, localUser.name)
            break

    connection.close()

def disconnect(connection, addr, name):
    global ThreadCount
    print(addr[0] + ':' + str(addr[1]) + "-"+ name +" Disconnected!")
    ThreadCount -= 1

    # Remove client from our list of connections
    for client in Clients:
        if client.address == addr[1]:
            Clients.remove(client)
            break

def send_to_other_clients(localUser, message):
    for client in Clients:
        if client.address != localUser.address:
            client.connection.send(str.encode(message))

    

start_new_thread(serverCommand, ())

while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    

    # Nessecary to set up the client list and keep track of connections
    clientName = Client.recv(2048).decode('utf-8')
    print("Client connected - " + clientName + ". Connection - " + str(address[0]) + ":" + str(address[1]))
    localUser = ClientUser(clientName, address[1], Client)
    Clients.append(localUser)
    ThreadCount += 1

    start_new_thread(multi_threaded_client, (Client, address, localUser))
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()