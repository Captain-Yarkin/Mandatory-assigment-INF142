from os import environ

host = environ.get("HOST", "localhost")

HEADER: int = 1024
ADDRESS: tuple[str, int] = (host, 5555)