import json
import os.path
import sys

from helpers import NpEncoder


def save_as_json(destination, data):
    with open(destination, "w", encoding="utf-8") as f:
        output = json.dumps(data, cls=NpEncoder, ensure_ascii=False).replace("NaN", "null")
        f.write(output)


def read_json_from_file(path):
    log_status(f"Reading {path}")
    if not os.path.isfile(path):
        raise Exception(f"{path} not found")

    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data


def log_status(message):
    print(message, file=sys.stderr)
