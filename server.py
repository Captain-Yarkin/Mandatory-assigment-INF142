# This is where the server for the game is going to be
from socket import socket
# Module that allows us to run multiple games at the same time on one server.
from threading import Thread

HEADER = 1024

# Server address in string format
IP = ':'.join(map(str, ADDR))
sock = socket()
sock.bind(("localhost", 5555))



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
    
    sock.listen()
    
    while True:
        print(f'Connect client to {IP = } to join game of TNT.')
        
        p1_socket, p1_address = sock.accept()
        print('Player 1 connected')
        
        p2_socket, p2_address = sock.accept()
        print('Player 2 connected')
        
        Thread(target = game, args = (p1_socket, p1_address, p2_socket, p2_address)).start()

# this need more work on :)
def read(conn):
  while True:
    data = conn.recv(1024)
    if data:
      sentence = data.decode()
      new_sentence = sentence.upper()
      conn.send(new_sentence.encode())
    else:
      print('closing', conn)
      conn.close()
      break

def accept(sock):
  while True:
    conn, address = sock.accept()
    print('accepted', conn, 'from', address)
    Thread(target=read, args=(conn,)).start()


if __name__ == '__main__':
    listenForConnections()