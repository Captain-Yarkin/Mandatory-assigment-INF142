from socket import socket
import globals

sock = socket()
sock.connect(globals.ADDRESS)

champion_list = sock.recv(globals.HEADER)
client_name = sock.recv(globals.HEADER)

# Print champion list and ask to select champ
print(champion_list)
message = input(f"{client_name} select champion: ")

# Check with server if selection is valid
sock.send((message.encode()))

sock.close()