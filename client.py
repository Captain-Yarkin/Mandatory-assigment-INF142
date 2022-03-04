import socket

IP_AND_PORT = input('Enter IP: ')
IP, PORT = IP_AND_PORT.split(sep=':')
PORT = int(PORT)

SERVER_ADDR = (IP, PORT)
