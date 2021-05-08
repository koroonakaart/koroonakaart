import subprocess  # nosec
import sys
from pathlib import Path

from build.constants import TODAY_DMYHM, NAVBAR_PATH
from build.utils import analyze_memory, save_as_json
from build.utils import analyze_time
from build.utils import logger


def label(text: str):
    length = len(text)
    l = logger.opt(colors=True)
    l.warning("")
    l.warning("<m>/=" + ("=" * length) + "=\\ </m>")
    l.warning("<m>|</m> <b>{text}</b> <m>|</m>", text=text)
    l.warning("<m>\\=" + ("=" * length) + "=/</m>")
    l.warning("")


@analyze_time
@analyze_memory
def main():
    script_name = Path(__file__).name
    for f in sorted(Path("build").glob("generate_*.py")):
        if f.name == script_name:
            continue

        label(f"Running {f.name}")
        subprocess.run([sys.executable, f], check=True)  # nosec

    logger.info("Writing NavBar JSON package")
    final_json = {
        "updatedOn": TODAY_DMYHM,
    }

    # Dump JSON output
    save_as_json(NAVBAR_PATH, final_json)


if __name__ == "__main__":
    main()
