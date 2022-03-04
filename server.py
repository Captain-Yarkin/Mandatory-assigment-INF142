import socket
import threading

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)

IP = ':'.join(map(str, ADDR))

server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def game(p1_socket: socket.socket, p1_address, p2_socket: socket.socket, p2_address):
    pass

def listenForConnections():
    
    server.listen()
    
    while True:
        print(f'Connect client to {IP = } to join game of TNT.')
        
        p1_socket, p1_address = server.accept()
        print('Player 1 connected')
        
        p2_socket, p2_address = server.accept()
        print('Player 2 connected')
        
        threading.Thread(target = game, args = (p1_socket, p1_address, p2_socket, p2_address)).start()

if __name__ == '__main__':
    listenForConnections()