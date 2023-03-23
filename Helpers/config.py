import os
import sys
import json


def read_config():
    if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/../config.json"):
        sys.exit("'config.json' not found! Please add it and try again.")
    else:
        with open(f"{os.path.realpath(os.path.dirname(__file__))}/../config.json") as file:
            config = json.load(file)

    return config
