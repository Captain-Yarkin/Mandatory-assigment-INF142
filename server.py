# This is where the server for the game is going to be
from socket import socket
# Module that allows us to run multiple games at the same time on one server.
from threading import Thread
import globals

sock = socket()
sock.bind(globals.ADDRESS)

selected_champ_player_1 = []
selected_champ_player_2 = []

def game(p1_socket: socket, p2_socket: socket):
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
    print("Server is running...")
    
    while True:
        
        p1_socket = accept(sock)
        
        p2_socket = accept(sock)
        
        Thread(target = game, args = (p1_socket, p2_socket)).start()

# this need more work on :)
def read(conn):
  while True:
    data = conn.recv(globals.HEADER)
    if data:
      sentence = data.decode()
      new_sentence = sentence.upper()
      conn.send(new_sentence.encode())
    else:
      print('closing', conn)
      conn.close()
      break

def accept(sock: socket):
    player_socket, address = sock.accept()
    print('accepted', player_socket, 'from', address)
    return player_socket


if __name__ == '__main__':
    listenForConnections()