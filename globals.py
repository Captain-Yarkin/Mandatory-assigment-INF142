from os import environ

host = environ.get("HOST", "localhost")

INPUT = "INPUT"

HEADER: int = 512
ADDRESS: tuple[str, int] = (host, 5555)