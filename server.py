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

def handle_client(conn:socket.socket,addr:Tuple):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected: 
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] [{msg}]")
            if msg == DISCONNECT_MESSAGE:
                connected = False
            conn.send("MSG received".encode(FORMAT))
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn , addr = server.accept() # wait for a new connection for the server
        print(type(conn))
        print(type(addr))
        thread = threading.Thread(target=handle_client, args =(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
   

print("[STARTING] Server is starting...")
start()