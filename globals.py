from os import environ
from champlistloader import load_some_champs

host = environ.get("HOST", "localhost")

INPUT = "INPUT"
PRINT = "PRINT"
PRINT_CHAMPS = "PRINT_CHAMPS"

HEADER: int = 512
ADDRESS: tuple[str, int] = (host, 5555)


'''
PROTOCOL

COMMAND|"Message"

example:
INPUT|"Player 1, select champion: "

PRINT|"Waiting for player 2 to select champion"
'''
