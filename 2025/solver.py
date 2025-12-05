import argparse
import importlib


def run_day(day: int, silent_missing=False):
    """Import days.dayXX and run its solve() function."""
    module_name = f"days.day{day:02}"
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        if not silent_missing:
            print(f"Module {module_name} not found!")
        return

    print(f"--- Day {day} ---")
    p1, p2 = module.solve()
    print("Part 1:", p1)
    print("Part 2:", p2)
    print()


def run_all_days():
    """Run all day modules sequentially."""
    for day in range(1, 26):
        run_day(day, silent_missing=True)


def main():
    parser = argparse.ArgumentParser(description="Run Advent of Code solutions.")
    parser.add_argument(
        "day",
        nargs="?",
        type=int,
        help="Day number to run (1-25). Leave empty to run all days.",
    )

    args = parser.parse_args()

    if args.day is None:
        run_all_days()
    else:
        run_day(args.day)


if __name__ == "__main__":
    main()
