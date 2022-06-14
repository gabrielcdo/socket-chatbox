import socket

class Client():
  def __init__(self, conn:socket.socket, user:str):
    self.conn = conn
    self.user = user

