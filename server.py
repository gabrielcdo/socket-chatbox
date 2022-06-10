import socket
import threading
from typing import Tuple
from constants import *
from models.resources import Resources
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--spell', dest='is_active',
                    help="active spell correction", default=None)
args = parser.parse_args()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []


def send_msg(conn: socket.socket, msg: str):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


def distribute_msg(conn: socket.socket, msg: str):
    for client in clients:
        if client != conn:
            try:
                send_msg(client, msg)
            except socket.error as e:
                print("Error sending data: %s" % e)


def handle_client(conn: socket.socket, addr: Tuple):
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
            distribute_msg(conn, msg)
    conn.close()


def start_server():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()  # wait for a new connection for the server
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")


if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    if args.is_active:
        print('[LOADING] Model is loading...')
        res = Resources()
    start_server()
