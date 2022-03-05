# This is where the server for the game is going to be
from socket import socket, create_server
# Module that allows us to run multiple games at the same time on one server.
from threading import Thread
from os import environ
import globals
from json import dumps

from rich import print
from rich.table import Table

host = environ.get("HOST", "localhost")
sock = create_server((host, 5550))

selected_champ_player_1 = []
selected_champ_player_2 = []

# TODO Replace this dict with DB
temp_champs = {
  "Vian" : "",
  "Dr. Yi" : "",
  "Twist" : "",
  "Guan" : "",
  "Siva" : ""
}

def game(p1_socket: socket, p2_socket: socket):

    print("[SERVER] Game Started")

    welcome_message = '''
          'Welcome to [bold yellow]Team Local Tactics[/bold yellow]!'
          
          'Each player choose a champion each time.'
          '''
    send_data(p1_socket, welcome_message)
    send_data(p2_socket, welcome_message)

    get_all_user_champions(p1_socket, p2_socket)

def send_data(connection: socket, message):
    
    # Fill blank spaces to match headersize
    message += " " * (globals.HEADER - len(message))
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

def _recv(conn):
  '''
  Handle receiving of data from clients.
  Listens for messages, decodes them and returns the message.
  '''
  while True:
    data = conn.recv(globals.HEADER)
    if data:
      sentence = data.decode()
      print(f"[SERVER] {sentence}")
      return sentence

def get_all_user_champions(player1, player2):
    '''
    Collects the clients selection of champions.
    '''
    max_player_champion_count = 2

    for _ in range(max_player_champion_count):
        select_champion(player1, player2, 1)
        select_champion(player2, player1, 2)

def select_champion(selecting_player, waiting_player, selecting_player_num):
    champions = dumps(temp_champs)
    send_data(selecting_player, champions + "\n")
    send_data(waiting_player, f"Wait for Player {selecting_player_num} to select champion...")

    # Ask player for a champion until valid selection.
    while True:
        send_data(selecting_player, f"Player {selecting_player_num} select champion: ")
        send_data(selecting_player, globals.INPUT)

        userSelection = _recv(selecting_player)

        # Validate selection
        if validateChampion(userSelection):
            if selecting_player_num == 1:
                selected_champ_player_1.append(userSelection)
            else:
                selected_champ_player_2.append(userSelection)
            print(f"[SERVER] (Selected champions) Player 1: {selected_champ_player_1}  Player 2: {selected_champ_player_2}")
            send_data(waiting_player, f"Player {selecting_player_num} selected {userSelection}.")
            break
        else:
            send_data(selecting_player, "Invalid selection. Please try again.")
            continue
        

def validateChampion(selectedChamp):
    # Check if champion exists in DB
    if selectedChamp in temp_champs:
        # Check if not previusly selected by any of the players
        if selectedChamp not in selected_champ_player_1 and selectedChamp not in selected_champ_player_2:
            return True

    return False

def accept(sock: socket):
    player_socket, address = sock.accept()
    print('accepted', player_socket, 'from', address)
    return player_socket


if __name__ == '__main__':
    listenForConnections()