from constants import *
import socket


def send_msg(conn: socket.socket, msg: str):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


def receive_msg(conn: socket.socket) -> str:
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
    return msg
