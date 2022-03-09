import globals
# # from server import accept
from rich import print
from os import environ
from socket import socket, create_server

DB = environ.get("DATABASE", "localhost")
sock = create_server((DB, 5555))

def from_csv(filename: str) -> str:
    champions = ""
    with open(filename, 'r') as f:
        for line in f.readlines():
            champions += line
    return champions

def load_some_champs():
    return from_csv('some_champs.txt')

def send_data(server: socket):
    message = load_some_champs()
    server.send(message.encode())

def _recv(conn: socket):
    print("[DATABASE] Ready to receive")
    while True:
        data = conn.recv(globals.HEADER)
        command, _ = data.decode().split("|")

        if command == globals.DATA:
            send_data(conn)
            conn.close()
            break
    
    # Listen for new connection
    establish_connection()
            

def establish_connection():
    server, _ = socket.accept(sock)
    print(f"[DATABASE] Connected: {server}")
    _recv(server)
    

def start():
    sock.listen()
    print("[DATABASE] Running...")
    establish_connection()


start()