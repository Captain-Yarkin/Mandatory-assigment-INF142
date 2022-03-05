from socket import socket, create_connection
from os import environ
import globals

server = environ.get("SERVER", "localhost")
sock = create_connection((server, 5550))

def from_csv(filename: str) -> str:
    champions = ""
    with open(filename, 'r') as f:
        for line in f.readlines():
            champions += line
    return champions


def load_some_champs():
    return from_csv('some_champs.txt')

def send_data():
    message = load_some_champs()
    sock.send(message.encode())

def _recv():
    print("[DATABASE] Ready to receive")
    while True:
        data = sock.recv(globals.HEADER)
        command, _ = data.decode().split("|")

        if command == globals.DATA:
            send_data()

_recv()