import socket
import threading
from models.client import Client
from constants import *
from utils_msgs import *


def wait_input(client: Client):
    send_msg(client.conn, f'{client.user}')
    while True:
        message = input().strip()
        send_msg(client.conn, message)


def client_receive(client: Client):
    while True:
        msg = receive_msg(client.conn)
        print(msg)
        if(msg == EXIT_MSG):
            return

def start_client():
    user = input('Enter username:    ').strip()
    if not USERNAME_REGEX.match(user):
        print('INVALID USERNAME! Please enter a valid username')
        return 
    client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_conn.connect(ADDR)
    client = Client(conn=client_conn, user=user)
    print('[OK] Server Connection Accepted')
    wait_thread = threading.Thread(target=wait_input, args=(client,))
    receive_thread = threading.Thread(target=client_receive, args=(client,))
    wait_thread.start()
    receive_thread.start()


if __name__ == "__main__":
    print("[STARTING] Client is starting...")
    start_client()
