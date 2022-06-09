import socket 
import threading
from models.client import Client

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = '127.0.1.1'
ADDR = (SERVER,PORT)


def send_msg(conn:socket.socket,msg:str):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def wait_msg(client:Client):
    send_msg(client.conn, f'{client.user} enter in the chat')
    while True:
        message = input().strip() 
        message = f'<{client.user}> {message}'
        send_msg(client.conn, message)

def receive_msg(client:Client):
    while True:
        try:
            serverSentence = client.conn.recv(2048)
            serverSentence = serverSentence.decode('utf-8')
            print(serverSentence)
        except socket.error as e:
            print("Error receiving data: %s" % e)

def start_client():
    user =input('Enter username:    ')
    client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_conn.connect(ADDR)
    client = Client(conn=client_conn,user=user)
    print('[OK] Server Connection Accepted')
    wait_thread = threading.Thread(target=wait_msg, args =(client,))
    receive_thread = threading.Thread(target=receive_msg, args =(client,))
    wait_thread.start()
    receive_thread.start()


if __name__ == "__main__":
    print("[STARTING] Client is starting...")
    start_client()

