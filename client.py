from threading import Thread
from rich import print
from rich.prompt import Prompt
from rich.table import Table
from socket import create_connection
from os import environ
import globals
from json import loads
from core import Champion


def constrained_input(prompt: str, valid_choices: tuple[str, ...]) -> str:

    '''
    Only allow certain inputs from user.
    Keep asking until a valid input is given.
    '''

    while True:
        
        user_input = input(prompt + f' {valid_choices}: ')
        
        if user_input in valid_choices:
            return user_input
        
        print(f'I do not understand {user_input}. Please try again.')

def send_input(prompt):
    message = Prompt.ask(prompt)
    sock.send(message.encode())

def print_champions(champions):
   champions = globals.format_champions(champions)
   print_available_champs(champions)

def print_available_champs(champions: dict[Champion]) -> None:

    # Create a table containing available champions
    available_champs = Table(title='Available champions')

    # Add the columns Name, probability of rock, probability of paper and
    # probability of scissors
    available_champs.add_column("Name", style="cyan", no_wrap=True)
    available_champs.add_column("prob(:raised_fist-emoji:)", justify="center")
    available_champs.add_column("prob(:raised_hand-emoji:)", justify="center")
    available_champs.add_column("prob(:victory_hand-emoji:)", justify="center")

    # Populate the table
    for champion in champions.values():
        available_champs.add_row(*champion.str_tuple)

    print(available_champs)

def print_match_result(message):

    match_rounds, match_score = message.split(";")
    match_rounds = match_rounds[2:-2].split("', '")

    print_match_summary(match_rounds, match_score)

def print_match_summary(match_rounds, match_score) -> None:

    EMOJI = {
        "Shape.ROCK": ':raised_fist-emoji:',
        "Shape.PAPER": ':raised_hand-emoji:',
        "Shape.SCISSORS": ':victory_hand-emoji:'
    }

    # For each round print a table with the results
    for index, round in enumerate(match_rounds):
        # Create a table containing the results of the round
        round_summary = Table(title=f'Round {index+1}')

        # Add columns for each team
        round_summary.add_column("Red",
                                 style="red",
                                 no_wrap=True)
        round_summary.add_column("Blue",
                                 style="blue",
                                 no_wrap=True)

        # Convert text to dict
        round = loads(round)

        # Populate the table
        for key, value in round.items():
            red, blue = key.split(', ')
            round_summary.add_row(f'{red} {EMOJI[value.split(",")[0]]}',
                                  f'{blue} {EMOJI[value.split(",")[1]]}')
        print(round_summary)
        print('\n')

    # Print the score
    red_score, blue_score = match_score.split(":")
    print(f'Red: {red_score}\n'
          f'Blue: {blue_score}')

    # Print the winner
    if red_score > blue_score:
        print('\n[red]Red victory! :grin:')
    elif red_score < blue_score:
        print('\n[blue]Blue victory! :grin:')
    else:
        print('\nDraw :expressionless:')


def main():

    mode = constrained_input('Singleplayer, or multiplayer?', (globals.SINGLE_PLAYER, globals.MULTI_PLAYER))
    
    global sock
    sock = create_connection((environ.get("SERVER", "localhost"), 5550))
    sock.send(mode.encode())

    while True:
        data = sock.recv(globals.HEADER)
        command, message = data.decode().split("|")
        message = message.strip("#")

        # If special keyword detected, start new thread to handle input
        if command == globals.INPUT:
            send_input(message)
        elif command == globals.PRINT_CHAMPS:
            print_champions(message)
        elif command == globals.PRINT:
            print(message)
        elif command == globals.PRINT_RESULT:
            print_match_result(message)

if __name__ == '__main__':
    main()