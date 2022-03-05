from threading import Thread

from rich import print
from rich.prompt import Prompt
from rich.table import Table

from socket import socket, create_connection
from os import environ
import globals

from core import Champion

server = environ.get("SERVER", "localhost")
sock = create_connection((server, 5550))

def print_message(message):
    print(message)

def send_input(promt):
    message = input(promt)
    sock.send(message.encode())

def print_champions(champions):
   champions = format_champions(champions)
   print_available_champs(champions)

def format_champions(champions):
    champions_dict = {}
    for line in champions.split("\n"):
        champ = _parse_champ(line)
        champions_dict[champ.name] = champ
    return champions_dict

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

def _parse_champ(champ_text: str) -> Champion:
    name, rock, paper, scissors = champ_text.split(sep=',')
    return Champion(name, float(rock), float(paper), float(scissors))

def _input(promt):
    send_input(promt)



def _recv():
    while True:
        data = sock.recv(globals.HEADER)
        command, message = data.decode().split("|")
        message = message.strip("#")

        # If special keyword detected, start new thread to handle input
        if command == globals.INPUT:
            Thread(target=_input(message)).start()
        elif command == globals.PRINT_CHAMPS:
            print_champions(message)
        elif command == globals.PRINT:
            print_message(message)

def start():
    _recv()

start()