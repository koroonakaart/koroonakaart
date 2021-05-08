import json
import os.path
import sys
import tracemalloc
from datetime import timedelta
from functools import wraps
from time import time
from typing import Any
from typing import Callable

from humanize import naturalsize
from humanize import precisedelta
from loguru import logger

from build.helpers import NpEncoder

_ACTIVE_ANALYSES = 0
_DEBUG_MEMORY = True

logger.remove()
logger.add(sys.stderr, enqueue=True)


def save_as_json(destination, data):
    logger.debug("Writing {dst}", dst=destination)
    with open(destination, "w", encoding="utf-8", newline="\n") as f:
        output = json.dumps(
            data, cls=NpEncoder, ensure_ascii=False, indent=2, sort_keys=True
        ).replace("NaN", "null")
        f.write(output)


def read_json_from_file(path):
    logger.debug("Reading {path}", path=path)
    if not os.path.isfile(path):
        raise Exception(f"{path} not found")

    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data


# Wrapper to analyze time used by any function
def analyze_time(fn: Callable[..., Any]):
    @wraps(fn)
    def _wrap(*args, **kwargs):
        start = time()
        result = fn(*args, **kwargs)

        elapsed = time() - start
        logger.debug(
            "{name} took {time}",
            name=fn.__name__,
            time=precisedelta(timedelta(seconds=elapsed)),
        )

        return result

    return _wrap


# Wrapper to analyze memory usage of any function
def analyze_memory(fn: Callable[..., Any]):
    @wraps(fn)
    def _wrap(*args, **kwargs):
        global _ACTIVE_ANALYSES

        if _DEBUG_MEMORY:
            if _ACTIVE_ANALYSES == 0:
                tracemalloc.start()
            _ACTIVE_ANALYSES += 1

        result = fn(*args, **kwargs)

        if _DEBUG_MEMORY:
            _, peak = tracemalloc.get_traced_memory()

            _ACTIVE_ANALYSES -= 1
            if _ACTIVE_ANALYSES == 0:
                tracemalloc.stop()

            logger.debug(
                "{name} peak memory usage {peak}",
                name=fn.__name__,
                peak=naturalsize(peak, binary=True),
            )

        return result

    return _wrap
