#!/usr/bin/env python3
import sys
from pathlib import Path

TEMPLATE = """\
from utils.loader import load_lines

def part1(data):
    pass

def part2(data):
    pass

def solve():
    data = load_lines({day})
    return part1(data), part2(data)
"""


def main():
    if len(sys.argv) < 2:
        print("Usage: python new_day.py <day>")
        sys.exit(1)

    day = int(sys.argv[1])
    day_file = Path(__file__).parents[1] / "days" / f"day{day:02}.py"
    input_file = Path(__file__).parents[1] / "inputs" / f"day{day:02}.txt"

    # Create Python file
    if day_file.exists():
        print(f"{day_file} already exists!")
    else:
        day_file.write_text(TEMPLATE.format(day=day))
        print(f"Created {day_file}")

    # Create input file
    if input_file.exists():
        print(f"{input_file} already exists!")
    else:
        input_file.touch()
        print(f"Created {input_file}")


if __name__ == "__main__":
    main()

