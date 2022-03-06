# This is where the server for the game is going to be
from socket import socket, create_server
# Module that allows us to run multiple games at the same time on one server.
from threading import Thread
from os import environ
import globals

from json import dumps
from core import Match, Team
from rich import print

host = environ.get("HOST", "localhost")
sock = create_server((host, 5550))

selected_champ_player_1 = []
selected_champ_player_2 = []

neutral_color = "white"
player1_color = "red"
player2_color = "blue"

database = None

def game(player1: socket, player2: socket):

    print("[SERVER] Game Started")

    welcome_message = '''
          'Welcome to [bold yellow]Team Local Tactics[/bold yellow]!'
          'Each player choose a champion each time.'
          '''
    send_data(player1, globals.PRINT, welcome_message)
    send_data(player2, globals.PRINT, welcome_message)

    get_all_user_champions(player1, player2)
    start_match(player1, player2)


def start_match(player1, player2):
    '''
    Calculate the match results and send the results to the clients
    '''

    # Get champion list from DB and convert to correct format
    champions = retrieve_champions()
    champions = globals.format_champions(champions)

    # Calculate match results
    match = Match(
        Team([champions[name] for name in selected_champ_player_1]),
        Team([champions[name] for name in selected_champ_player_2])
    )
    match.play()

    # Convert match results to string that can be sent to clients
    match_rounds = []
    for round in match.rounds:
        print(f"{round}  ::: {type(round)}")
        match_result = {}    
        for key in round:
            match_result[key] = f"{round.get(key).red},{round.get(key).blue}"
        match_result = dumps(match_result)
        match_rounds.append(match_result)
    match_score = f"{match._red_score}:{match._blue_score}"

    # Send results to clients
    send_data(player1, globals.PRINT_RESULT, f"{match_rounds};{match_score}")
    send_data(player2, globals.PRINT_RESULT, f"{match_rounds};{match_score}")


def send_data(connection: socket, command, message):
    message = f"{command}|{message}"
    # Apply padding to fill rest of header
    message += "#" * (globals.HEADER - len(message))
    connection.send(message.encode())


def listenForConnections():
    global database
    '''
    Waits for clients to connect.
    When two clients have connected, a new thread running game() will start.
    Then the server will wait for two more connections and repeat.
    '''

    sock.listen()
    print("Server is running...")
    
    while True:
        database = accept(sock)
        
        p1_socket = accept(sock)
        send_data(p1_socket, globals.PRINT, f"[{neutral_color}]Waiting for player 2...")
        
        p2_socket = accept(sock)
        send_data(p1_socket, globals.PRINT, f"[{neutral_color}]Player 2 found. Starting match.")
        send_data(p2_socket, globals.PRINT, f"[{neutral_color}]Players found (2/2). Starting match.")
        
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
            return sentence

def get_all_user_champions(player1, player2):
    '''
    Collects the clients selection of champions.
    '''
    max_player_champion_count = 2

    for _ in range(max_player_champion_count):
        select_champion(player1, player2, 1)
        select_champion(player2, player1, 2)

def retrieve_champions():
    '''
    Request champions from database
    '''
    send_data(database, globals.DATA, "")
    champions = _recv(database)
    return champions

def select_champion(selecting_player, waiting_player, selecting_player_num):

    # Set colors of messages
    if selecting_player_num == 1:
        selecting_color = player1_color
        waiting_color = player2_color
    else:
        selecting_color = player2_color
        waiting_color = player1_color
    
    # Receive champions from database
    champions = retrieve_champions()

    send_data(selecting_player, globals.PRINT_CHAMPS, champions)
    send_data(waiting_player, globals.PRINT, f"[{waiting_color}]Wait for Player {selecting_player_num} to select champion...")

    # Ask player for a champion until valid selection.
    while True:
        send_data(selecting_player, globals.INPUT, f"[{selecting_color}]Player {selecting_player_num} select champion")
        selected_champion = _recv(selecting_player)

        # Update champion list (So we can update the list while we play)
        champions = retrieve_champions()
        champion_list = [x.split(",")[0] for x in champions.split("\n")]

        if validate_champion(selected_champion, champion_list, selecting_player, selecting_player_num, selecting_color):
            # Add champion to a team
            if selecting_player_num == 1:
                selected_champ_player_1.append(selected_champion)
            else:
                selected_champ_player_2.append(selected_champion)
            send_data(waiting_player, globals.PRINT, f"[{selecting_color}]Player {selecting_player_num} selected {selected_champion}.")
            print(f"[SERVER] (Selected champions) Player 1: {selected_champ_player_1}  Player 2: {selected_champ_player_2}")
            break

def validate_champion(champion, champion_list, player, player_num ,color):
    # Validate that champion exists
    if champion not in champion_list:
        send_data(player, globals.PRINT, f"[{color}]The champion {champion} is not available. Try again.")
        return False

    # Check if champion already is on the players team
    elif (champion in selected_champ_player_1 and player_num == 1) or (champion in selected_champ_player_2 and player_num == 2):
        send_data(player, globals.PRINT, f"[{color}]{champion} is already in your team. Try again.")
        return False
        
    # Check if champion already is on enemy team
    elif (champion in selected_champ_player_2 and player_num == 1) or (champion in selected_champ_player_1 and player_num == 2):
        send_data(player, globals.PRINT, f"[{color}]{champion} is in the enemy team. Try again.")
        return False
    return True


def accept(sock: socket):
    player_socket, _ = sock.accept()
    print('accepted', player_socket)
    return player_socket


if __name__ == '__main__':
    listenForConnections()