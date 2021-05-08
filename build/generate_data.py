import multiprocessing
import signal
import subprocess  # nosec
import sys
from argparse import ArgumentParser
from datetime import timedelta
from multiprocessing import Pool
from pathlib import Path
from time import time

from humanize import precisedelta

from build.constants import TODAY_DMYHM, NAVBAR_PATH
from build.utils import analyze_memory, save_as_json
from build.utils import analyze_time
from build.utils import logger

LOGGER = logger


def label(text: str):
    length = len(text)
    log = LOGGER.opt(colors=True)
    log.warning("")
    log.warning("<m>/=" + ("=" * length) + "=\\ </m>")
    log.warning("<m>|</m> <b>{text}</b> <m>|</m>", text=text)
    log.warning("<m>\\=" + ("=" * length) + "=/</m>")
    log.warning("")


def set_logger(logger_):
    global LOGGER
    LOGGER = logger_


def run(f: Path, index: int, total: int, quiet=False):
    msg = f"Running  {index}/{total}: {f.name}"
    if not quiet:
        label(msg)
    else:
        LOGGER.info(msg)

    kwargs = {
        "check": True,
    }

    if quiet:
        kwargs["stdout"] = subprocess.DEVNULL
        kwargs["stderr"] = subprocess.DEVNULL

    start = time()
    subprocess.run([sys.executable, f], **kwargs)  # nosec
    elapsed = time() - start

    LOGGER.debug(
        "Finished {index}/{total}: {name} in {time}",
        index=index,
        total=total,
        name=f.name,
        time=precisedelta(timedelta(seconds=elapsed)),
    )

    LOGGER.complete()


@analyze_time
@analyze_memory
def main():
    ap = ArgumentParser()
    ap.add_argument("--parallel", type=int, default=1)
    opts = ap.parse_args()

    script_name = Path(__file__).name
    scripts = []
    for f in sorted(Path("build").glob("generate_*.py")):
        if f.name == script_name:
            continue
        scripts.append(f)
    total = len(scripts)

    logger.info("Found {total} generators", total=total)

    if opts.parallel == 1:
        for idx, path in enumerate(scripts):
            run(path, idx + 1, total)
    else:
        # Parallelism in Python can sometimes be a bit funky
        # This takes care of sharing a sane logger, and handling Ctrl+C, sometimes
        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        with Pool(opts.parallel, initializer=set_logger, initargs=(logger,)) as pool:
            signal.signal(signal.SIGINT, original_sigint_handler)
            args = [(path, idx + 1, total, True) for idx, path in enumerate(scripts)]

            try:
                res = pool.starmap_async(run, args)
                while True:
                    try:
                        res.get(
                            3
                        )  # Without the timeout this blocking call ignores all signals.
                        pool.close()
                        break
                    except multiprocessing.context.TimeoutError:
                        continue
            except KeyboardInterrupt:
                logger.error("Caught KeyboardInterrupt, terminating workers")
                pool.terminate()

    logger.info("Writing NavBar JSON package")
    final_json = {
        "updatedOn": TODAY_DMYHM,
    }

    # Dump JSON output
    save_as_json(NAVBAR_PATH, final_json)


if __name__ == "__main__":
    main()
    logger.complete()
