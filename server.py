import socket
import threading
from typing import Tuple
from constants import *
from models.resources import Resources
import argparse
from symspell.symspell import spell_correct
from utils_msgs import *

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--spell', dest='is_active',
                    help="active spell correction", default=None)
args = parser.parse_args()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []
clients_dict = dict()


def distribute_msg(conn: socket.socket, msg: str):
    for client in clients_dict:
        if clients_dict[client] != conn:
            try:
                send_msg(clients_dict[client], msg)
            except socket.error as e:
                print("Error sending data: %s" % e)


def handle_client(conn: socket.socket, addr: Tuple):

    print(f"[NEW CONNECTION] {addr} connected.")
    username = receive_msg(conn)
    if clients_dict.get(username):
        send_msg(conn, 'Username already exists! Try again')
        conn.close()
        return 
    distribute_msg(conn, f'[{username}] enter in the chat')
    
    clients_dict[username]=conn
    connected = True

    while connected:
        try:
            msg = receive_msg(conn)
            if args.is_active:
                msg = spell_correct(msg, res.spell_model)
            msg = f'<{username}> {msg}'
            print(f"[{addr}] [{msg}]")
            if msg == DISCONNECT_MESSAGE:
                connected = False
            distribute_msg(conn, msg)
        except Exception as e:
            print(e)
            connected = False
    del clients_dict[username]
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
