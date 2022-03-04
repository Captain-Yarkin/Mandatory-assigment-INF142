# This is where the server for the game is going to be
import socket

# This is the "public ip" that makes it possible to connect to the internet
SERVER_PUBLIC_IP = "localhost"
# Out base bit header for sending and reciving data
HEADER = 64
# Chosen port
PORT = 5555
# Addrese from where the data will be comming from
ADDRESE = (SERVER_PUBLIC_IP, PORT)

# TCP protocol that bind with the addresse
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESE)



