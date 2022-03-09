from __future__ import annotations
import random

# This is where the server for the game is going to be
from socket import socket, create_server, create_connection
# Module that allows us to run multiple games at the same time on one server.
from threading import Thread
from os import environ
from typing import NoReturn
import globals

from json import dumps
from core import Match, Team
from rich import print

from dataclasses import dataclass, field

SOCK = create_server((environ.get("HOST", "localhost"), 5550))
NEUTRAL_COLOR = "white"
PLAYER1_COLOR = 'red'
PLAYER2_COLOR = 'blue'



class Player:
    
    '''
    Combines: socket, player number, player text color and selected champion list.
    This is to reduce the amount of arguments required in various functions.
    '''
    
    def __init__(self, sock: socket, num: int):
        self.sock = sock
        self.num = num
        self.color = PLAYER1_COLOR if num == 1 else PLAYER2_COLOR
        self.champs: list[str] = []
    
    def print(self, message: str) -> None:
        send_data(self.sock, globals.PRINT, message)
    
    def print_champs(self, champs: str) -> None:
        send_data(self.sock, globals.PRINT_CHAMPS, champs)
    
    def print_result(self, result: str) -> None:
        send_data(self.sock, globals.PRINT_RESULT, result)
    
    def select_champion(self, waiting_player: Player) -> None:
        # Receive champions from database
        champions = retrieve_champion_names_string()

        self.print_champs(champions)
        waiting_player.print(
            f"[{waiting_player.color}]Wait for Player {self.num} to select champion..."
        )

        # Ask player for a champion until valid selection.
        while True:
            
            send_data(self.sock, globals.INPUT, f"[{self.color}]Player {self.num} select champion")
            selected_champion = recieve_data(self.sock)
            
            # Update champion list (So we can update the list while we play)
            champion_list = retrieve_champion_names_list()

            if validate_champion(selected_champion, champion_list, self, waiting_player):
                # Add champion to a team
                self.champs.append(selected_champion)

                waiting_player.print(f"[{self.color}]Player {self.num} selected {selected_champion}.")

                print(
                    f"[SERVER] (Selected champions) Player {self.num}: {self.champs}  Player {waiting_player.num}: {waiting_player.champs}"
                )
                
                break

class Ai(Player):
    def __init__(self):
        super().__init__(None, 2)
    
    def print(self, message: str) -> None:
        pass
    
    def print_champs(self, champs: str) -> None:
        pass
    
    def print_result(self, result: str) -> None:
        pass
    
    def select_champion(self, waiting_player: Player) -> None:
        champion_list = retrieve_champion_names_list()
        remaining_champions = [champ for champ in champion_list if champ not in (self.champs + waiting_player.champs)]
        selected_champion = random.choice(remaining_champions)
        self.champs.append(selected_champion)
        
        waiting_player.print(f"[{self.color}]Player {self.num} selected {selected_champion}.")

def validate_champion(selected_champion: str, all_champions: list[str], selecting_player: Player, waiting_player: Player) -> bool:

    '''
    Returns true if the selected champion exists, and is not already part of the selecting or waiting players team.
    If the champion is not available, the function returns false, and sends a message to the player to pick again.
    '''

    # Validate that champion exists
    if selected_champion not in all_champions:
        selecting_player.print(f"[{selecting_player.color}]The champion {selected_champion} is not available. Try again.")
        return False

    # Check if champion already is on the players team
    elif selected_champion in selecting_player.champs:
        selecting_player.print(f"[{selecting_player.color}]{selected_champion} is already in your team. Try again.")
        return False

    # Check if champion already is on enemy team
    elif selected_champion in waiting_player.champs:
        selecting_player.print(f"[{selecting_player.color}]{selected_champion} is in the enemy team. Try again.")
        return False
    return True

def main() -> NoReturn:
    
    '''
    Infinitely waits for clients to connect.
    Clients will already have specified whether they want to play a single- or multiplayer game before connecting to the server.
    If the player wants to play a multiplayer game, the socket is stored in a list while the server waits for another player to connect in multiplayer mode.
    When two clients have connected, a new thread running game() will start, and the server can wait for more clients to connect.
    If the player chooses single player mode, a thread running single_player_game() will start, and the server can wait for more clients.
    '''

    SOCK.listen()
    print("Server is running...")

    multiplayer_sockets: list[socket] = []

    while True:
        player_socket = accept(SOCK)

        # Get the the mode of play from client.
        mode = player_socket.recv(1).decode()

        if mode == globals.MULTI_PLAYER:
            
            multiplayer_sockets.append(player_socket)
            num_players = len(multiplayer_sockets)

            if num_players == 1:
            
                send_data(player_socket, globals.PRINT,
                  f"[{NEUTRAL_COLOR}]Waiting for player 2...")
            
            elif num_players == 2:
            
                for sock in multiplayer_sockets:
                    send_data(sock, globals.PRINT,
                      f"[{NEUTRAL_COLOR}]Players found (2/2). Starting match.")
                
                player1 = Player(multiplayer_sockets.pop(0), 1)
                player2 = Player(multiplayer_sockets.pop(0), 2)
                Thread(target=game, args=(player1, player2)).start()

        elif mode == globals.SINGLE_PLAYER:

            Thread(target=game, args=(Player(player_socket, 1), Ai())).start()
        
        else:

            print('[SERVER] Connection refused. Invalid game mode.')

def accept(sock: socket):
    player_socket, _ = sock.accept()
    print('accepted', player_socket)
    return player_socket

def game(player1: Player, player2: Player):

    print("[SERVER] Game Started")

    welcome_message = '''
          'Welcome to [bold yellow]Team Local Tactics[/bold yellow]!'
          'Each player choose a champion each time.'
          '''
    player1.print(welcome_message)
    player2.print(welcome_message)

    get_all_user_champions(player1, player2)
    start_match(player1, player2)

def get_all_user_champions(player1: Player, player2: Player):
    '''
    Collects the clients selection of champions.
    '''
    max_player_champion_count = 2

    for _ in range(max_player_champion_count):
        player1.select_champion(waiting_player = player2)
        player2.select_champion(waiting_player = player1)


def start_match(player1: Player, player2: Player) -> None:
    '''
    Calculate the match results and send the results to the clients
    '''

    # Get champion list from DB and convert to correct format
    champions = retrieve_champion_names_string()
    champions = globals.format_champions(champions)

    # Calculate match results
    match = Match(
        Team([champions[name] for name in player1.champs]),
        Team([champions[name] for name in player2.champs])
    )
    match.play()

    # Convert match results to string that can be sent to clients
    match_rounds = []
    for round in match.rounds:
        match_result = {}
        for key in round:
            match_result[key] = f"{round.get(key).red},{round.get(key).blue}"
        match_result = dumps(match_result)
        match_rounds.append(match_result)
    match_score = f"{match._red_score}:{match._blue_score}"

    # Send results to clients
    result_message = f"{match_rounds};{match_score}"
    player1.print_result(result_message)
    player2.print_result(result_message)


def send_data(connection: socket, command: str, message: str) -> None:
    message = f"{command}|{message}"
    # Apply padding to fill rest of header
    message += "#" * (globals.HEADER - len(message))
    connection.send(message.encode())


def recieve_data(conn: socket) -> str:
    '''
    Handle receiving of data from clients.
    Listens for messages, decodes them and returns the message.
    '''
    while True:
        data = conn.recv(globals.HEADER)
        if data:
            sentence = data.decode()
            return sentence


def retrieve_champion_names_string() -> str:
    '''
    Request champions from database
    '''
    # Connect to the database with a socket
    DB = environ.get("DATABASE", "localhost")
    database = create_connection((DB, 5555))

    send_data(database, globals.DATA, "")
    champions = recieve_data(database)
    return champions

def retrieve_champion_names_list() -> list[str]:
    return [x.split(",")[0] for x in retrieve_champion_names_string().split("\n")]

if __name__ == '__main__':
    main()
