import json
import os.path

from helpers import NpEncoder
from loguru import logger


def save_as_json(destination, data):
    logger.info("Writing data to {dst}", dst=destination)
    with open(destination, "w", encoding="utf-8") as f:
        output = json.dumps(data, cls=NpEncoder, ensure_ascii=False).replace(
            "NaN", "null"
        )
        f.write(output)


def read_json_from_file(path):
    logger.info("Reading data from {path}", path=path)
    if not os.path.isfile(path):
        logger.debug("{path} not found", path=path)
        return {}

    with open(path) as f:
        data = json.load(f)
    return data
