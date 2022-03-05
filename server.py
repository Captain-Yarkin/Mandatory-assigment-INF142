# This is where the server for the game is going to be
from ast import match_case
from glob import glob
from socket import socket, create_server
# Module that allows us to run multiple games at the same time on one server.
from threading import Thread
from os import environ
from champlistloader import load_some_champs
import globals
from json import dumps

from rich import print


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
    send_data(p1_socket, globals.PRINT, welcome_message)
    send_data(p2_socket, globals.PRINT, welcome_message)

    get_all_user_champions(p1_socket, p2_socket)

def send_data(connection: socket, command, message):
    message = f"{command}|{message}"
    # Fill blank spaces to match headersize
    message += "#" * (globals.HEADER - len(message))
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
        send_data(p1_socket, globals.PRINT, "Waiting for player 2...")
        
        p2_socket = accept(sock)
        send_data(p1_socket, globals.PRINT, "Player 2 found. Starting match.")
        send_data(p2_socket, globals.PRINT, "Players found (2/2). Starting match.")
        
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
    # champions = dumps(temp_champs)
    champions = load_some_champs()
    send_data(selecting_player, globals.PRINT_CHAMPS, champions)
    send_data(waiting_player, globals.PRINT, f"Wait for Player {selecting_player_num} to select champion...")

    # Ask player for a champion until valid selection.
    while True:
        send_data(selecting_player, globals.INPUT, f"Player {selecting_player_num} select champion: ")
        selected_champion = _recv(selecting_player)


        champ_list = [x.split(",")[0] for x in load_some_champs().split("\n")]

        # Validate that champion exists
        if selected_champion not in champ_list:
            send_data(selecting_player, globals.PRINT, f"The champion {selected_champion} is not available. Try again.")

        # Check if champion already is on the players team
        elif (selected_champion in selected_champ_player_1 and selecting_player_num == 1) or (selected_champion in selected_champ_player_2 and selecting_player_num == 2):
            send_data(selecting_player, globals.PRINT, f"{selected_champion} is already in your team. Try again.")
        
        # Check if champion already is on enemy team
        elif (selected_champion in selected_champ_player_2 and selecting_player_num == 1) or (selected_champion in selected_champ_player_1 and selecting_player_num == 2):
            send_data(selecting_player, globals.PRINT, f"{selected_champion} is in the enemy team. Try again.")
        
        # Add champion to a team
        else:
            if selecting_player_num == 1:
                selected_champ_player_1.append(selected_champion)
            else:
                selected_champ_player_2.append(selected_champion)
            send_data(waiting_player, globals.PRINT, f"Player {selecting_player_num} selected {selected_champion}.")
            print(f"[SERVER] (Selected champions) Player 1: {selected_champ_player_1}  Player 2: {selected_champ_player_2}")
            break


def accept(sock: socket):
    player_socket, address = sock.accept()
    print('accepted', player_socket, 'from', address)
    return player_socket


if __name__ == '__main__':
    listenForConnections()