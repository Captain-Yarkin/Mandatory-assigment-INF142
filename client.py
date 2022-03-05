from threading import Thread
from rich import print
from rich.prompt import Prompt
from rich.table import Table

from socket import socket, create_connection
from os import environ
import globals

server = environ.get("SERVER", "localhost")
sock = create_connection((server, 5550))

def print_message(data):
    message = data.decode()
    print(message)

def send_input():
    message = input()
    sock.send(message.encode())

def _input():
    send_input()

def _recv():
    while True:
        data = sock.recv(globals.HEADER)
        
        # If special keyword, start new thread to handle input
        if data.decode().strip() == globals.INPUT:
                Thread(target=_input).start()
        elif data:
            print_message(data)

def start():
    _recv()

start()