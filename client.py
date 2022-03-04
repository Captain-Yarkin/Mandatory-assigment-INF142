from rich import print
from rich.prompt import Prompt
from rich.table import Table

from socket import socket, create_connection
from os import environ
import globals

# sock = socket()
# sock.connect(globals.ADDRESS)

server = environ.get("SERVER", "localhost")
sock = create_connection((server, 5550))

def read():
    while True:
        data = sock.recv(globals.HEADER)
        if data:
            message = data.decode()
            print(message)

read()

champion_list = sock.recv(globals.HEADER)
client_name = sock.recv(globals.HEADER)

# Print champion list and ask to select champ
print(champion_list)
message = input(f"{client_name} select champion: ")

# Check with server if selection is valid
sock.send((message.encode()))

sock.close()