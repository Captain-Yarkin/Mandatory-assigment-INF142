import socket

IP_AND_PORT = input('Enter IP: ')
IP, PORT = IP_AND_PORT.split(sep=':')
PORT = int(PORT)

SERVER_ADDR = (IP, PORT)


sock = socket()
server_address = ("localhost", 5555)
sock.connect(server_address)
sentence = input("Input lowercase sentence: ")
sock.send(sentence.encode())
new_sentence = sock.recv(1024).decode()
print(f"From Server: {new_sentence}")
sock.close()