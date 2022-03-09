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


@dataclass
class Player:
    
    '''
    Combines: socket, player number, player text color and selected champion list.
    This is to reduce the amount of arguments required in various functions.
    '''
    
    sock: socket
    num: int
    color: str
    champs: list[str] = field(default_factory=list[str])


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
                
                player1 = Player(multiplayer_sockets.pop(0), 1, 'red')
                player2 = Player(multiplayer_sockets.pop(0), 2, 'blue')
                Thread(target=game, args=(player1, player2)).start()

        elif mode == globals.SINGLE_PLAYER:

            Thread(target=single_player_game, args=(Player(player_socket, 1, 'red')))
        
        else:

            print('[SERVER] Connection refused. Invalid game mode.')

def accept(sock: socket):
    player_socket, _ = sock.accept()
    print('accepted', player_socket)
    return player_socket

def single_player_game(player: Player):
    # TODO Single player game code.
    pass

def game(player1: Player, player2: Player):

    print("[SERVER] Game Started")

    welcome_message = '''
          'Welcome to [bold yellow]Team Local Tactics[/bold yellow]!'
          'Each player choose a champion each time.'
          '''
    send_data(player1.sock, globals.PRINT, welcome_message)
    send_data(player2.sock, globals.PRINT, welcome_message)

    get_all_user_champions(player1, player2)
    start_match(player1, player2)

def get_all_user_champions(player1: Player, player2: Player):
    '''
    Collects the clients selection of champions.
    '''
    max_player_champion_count = 2

    for _ in range(max_player_champion_count):
        select_champion(player1, player2)
        select_champion(player2, player1)

def select_champion(selecting_player: Player, waiting_player: Player):

    # Receive champions from database
    champions = retrieve_champions()

    send_data(selecting_player.sock, globals.PRINT_CHAMPS, champions)
    send_data(waiting_player.sock, globals.PRINT,
              f"[{waiting_player.color}]Wait for Player {selecting_player.num} to select champion...")

    # Ask player for a champion until valid selection.
    while True:
        send_data(selecting_player.sock, globals.INPUT,
                  f"[{selecting_player.color}]Player {selecting_player.num} select champion")
        selected_champion = recieve_data(selecting_player.sock)

        # Update champion list (So we can update the list while we play)
        champions = retrieve_champions()
        champion_list = [x.split(",")[0] for x in champions.split("\n")]

        if validate_champion(selected_champion, champion_list, selecting_player, waiting_player):
            # Add champion to a team
            selecting_player.champs.append(selected_champion)

            send_data(waiting_player.sock, globals.PRINT,
                      f"[{selecting_player.color}]Player {selecting_player.num} selected {selected_champion}.")
            print(
                f"[SERVER] (Selected champions) Player {selecting_player.num}: {selecting_player.champs}  Player {waiting_player.num}: {waiting_player.champs}")
            break

def validate_champion(selected_champion: str, all_champions: list[str], selecting_player: Player, waiting_player: Player) -> bool:

    '''
    Returns true if the selected champion exists, and is not already part of the selecting or waiting players team.
    If the champion is not available, the function returns false, and sends a message to the player to pick again.
    '''

    # Validate that champion exists
    if selected_champion not in all_champions:
        send_data(selecting_player.sock, globals.PRINT,
                  f"[{selecting_player.color}]The champion {selected_champion} is not available. Try again.")
        return False

    # Check if champion already is on the players team
    elif selected_champion in selecting_player.champs:
        send_data(selecting_player.sock, globals.PRINT,
                  f"[{selecting_player.color}]{selected_champion} is already in your team. Try again.")
        return False

    # Check if champion already is on enemy team
    elif selected_champion in waiting_player.champs:
        send_data(selecting_player.sock, globals.PRINT,
                  f"[{selecting_player.color}]{selected_champion} is in the enemy team. Try again.")
        return False
    return True

def start_match(player1: Player, player2: Player) -> None:
    '''
    Calculate the match results and send the results to the clients
    '''

    # Get champion list from DB and convert to correct format
    champions = retrieve_champions()
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
    send_data(player1.sock, globals.PRINT_RESULT, f"{match_rounds};{match_score}")
    send_data(player2.sock, globals.PRINT_RESULT, f"{match_rounds};{match_score}")


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


def retrieve_champions():
    '''
    Request champions from database
    '''
    # Connect to the database with a socket
    DB = environ.get("DATABASE", "localhost")
    database = create_connection((DB, 5555))

    send_data(database, globals.DATA, "")
    champions = recieve_data(database)
    return champions


if __name__ == '__main__':
    main()
