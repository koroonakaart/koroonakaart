from pathlib import Path
import subprocess  # nosec
import sys

from build.utils import analyze_memory
from build.utils import analyze_time


@analyze_time
@analyze_memory
def main():
    script_name = Path(__file__).name
    for f in Path("build").glob("generate_*.py"):
        if f.name == script_name:
            continue

        print("")
        print(f" ----- {f.name} -----")
        print("")
        subprocess.run([sys.executable, f], check=True)  # nosec


if __name__ == "__main__":
    main()
