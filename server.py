from ast import For
import socket
import threading 
from typing import Tuple

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER,PORT)
print(SERVER)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []
def distribute_msg(conn:socket.socket,msg:str):
    for client in clients:
        if client != conn:
            try:
                client.send(msg.encode(FORMAT))
            except socket.error as e:
                print("Error sending data: %s" % e)
def handle_client(conn:socket.socket,addr:Tuple):
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append(conn)
    connected = True
    while connected: 
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] [{msg}]")
            if msg == DISCONNECT_MESSAGE:
                connected = False
            distribute_msg(conn,msg)
     
    conn.close()

def start_server():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn , addr = server.accept() # wait for a new connection for the server
        distribute_msg(conn,'enter in the chat')
        thread = threading.Thread(target=handle_client, args =(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
   
if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    start_server()