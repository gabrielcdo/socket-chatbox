import re

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = '127.0.1.1'
ADDR = (SERVER, PORT)
USERNAME_REGEX = re.compile('^[A-Za-z][A-Za-z0-9_]{2,12}')
EXIT_MSG = 'Username already exists! Try again'