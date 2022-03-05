def from_csv(filename: str) -> str:
    champions = ""
    with open(filename, 'r') as f:
        for line in f.readlines():
            champions += line
    return champions


def load_some_champs():
    return from_csv('some_champs.txt')
