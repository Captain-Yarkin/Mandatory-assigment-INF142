from os import environ
from core import Champion

host = environ.get("HOST", "localhost")

INPUT = "INPUT"
PRINT = "PRINT"
PRINT_CHAMPS = "PRINT_CHAMPS"
PRINT_RESULT = "PRINT_RESULT"
DATA = "DATA"

HEADER: int = 512
ADDRESS: tuple[str, int] = (host, 5555)

def format_champions(champions):
    champions_dict = {}
    for line in champions.split("\n"):
        champ = _parse_champ(line)
        champions_dict[champ.name] = champ
    return champions_dict

def _parse_champ(champ_text: str) -> Champion:
    name, rock, paper, scissors = champ_text.split(sep=',')
    return Champion(name, float(rock), float(paper), float(scissors))


'''
PROTOCOL

COMMAND|"Message"

example:
INPUT|"Player 1, select champion: "

PRINT|"Waiting for player 2 to select champion"
'''
