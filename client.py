from socket import socket

# IP_AND_PORT = input('Enter IP: ')
# IP, PORT = IP_AND_PORT.split(sep=':')
# PORT = int(PORT)

# SERVER_ADDR = (IP, PORT)

HEADER = 1024

sock = socket()
server_address = ("localhost", 5555)
sock.connect(server_address)

champion_list = sock.recv(HEADER)
client_name = sock.recv(HEADER)

# Print champion list and ask to select champ
print(champion_list)
message = input(f"{client_name} select champion: ")

# Check with server if selection is valid
sock.send((message.encode()))

sock.close()