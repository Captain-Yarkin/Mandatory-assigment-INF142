# This is where the server for the game is going to be
from socket import socket, create_server
# Module that allows us to run multiple games at the same time on one server.
from threading import Thread
from os import environ
import globals
from json import dumps

from rich import print
from rich.table import Table


# sock = socket()
# sock.bind(globals.ADDRESS)

host = environ.get("HOST", "localhost")
sock = create_server((host, 5550))


selected_champ_player_1 = []
selected_champ_player_2 = []

temp_champs = {
  "Vian" : "",
  "Dr. Yi" : "",
  "Twist" : "",
  "Guan" : "",
  "Siva" : ""
}

def game(p1_socket: socket, p2_socket: socket):
    '''
    The actual game code.
    '''
    print("[SERVER] Game Started")

    welcome_message = '''
          'Welcome to [bold yellow]Team Local Tactics[/bold yellow]!'
          
          'Each player choose a champion each time.'
          '''
    send_data(p1_socket, welcome_message)
    send_data(p2_socket, welcome_message)

    
    champions = dumps(temp_champs)
    send_data(p1_socket, champions + "\n")

    
    # champion_table = available_champs(champions)

    # send_data(p1_socket, champion_table)
    send_data(p1_socket, "Player 1 select champion: ")
    send_data(p2_socket, "Wait for Player 1 to select champion...")





def send_data(connection: socket, message):
    connection.send(message.encode())

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
        p1_socket.send("Waiting for player 2...".encode())
        
        p2_socket = accept(sock)
        p1_socket.send("Player 2 found. Starting match.".encode())
        p2_socket.send("Players found (2/2). Starting match.".encode())
        
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