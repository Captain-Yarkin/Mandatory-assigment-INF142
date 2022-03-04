# This is where the server for the game is going to be
import socket
# Module that allows us to run multiple games at the same time on one server.
import threading


SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)

# Out base bit header for sending and reciving data
HEADER = 64

# Server address in string format
IP = ':'.join(map(str, ADDR))

server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def game(p1_socket: socket.socket, p1_address, p2_socket: socket.socket, p2_address):
    '''
    The actual game code.
    '''
    pass

def listenForConnections():
    '''
    Waits for clients to connect.
    When two clients have connected, a new thread running game() will start.
    Then the server will wait for two more connections and repeat.
    '''
    
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