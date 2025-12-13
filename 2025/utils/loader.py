from pathlib import Path

# get the path of this file (i.e. <parent>/utils/load_input.py)
# and navigate up a level to get the <parent> folder
PARENT_DIR = Path(__file__).resolve().parents[1]

INPUT_DIR = Path(PARENT_DIR, "inputs")


def load_text(day):
    """
    Load the raw input file as a single string.
    """
    path = Path(INPUT_DIR, f"day{day:02}.txt")
    return path.read_text().rstrip("\n")


def load_lines(day, strip=True):
    """
    Load the input file as a list of strings (one per line).
    strip=True removes trailing newlines and spaces.
    """

    text = load_text(day)
    lines = text.splitlines()

    if strip:
        return [line.strip() for line in lines]
    return lines


def load_grid(day, strip=True):
    lines = load_lines(day, strip=strip)
    return [list(line) for line in lines]
