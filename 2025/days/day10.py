from collections import namedtuple

from utils.loader import load_lines

Machine = namedtuple(
    "Machine", ["starting_state", "light_diagram", "buttons", "joltage"]
)


def part1(data):
    print(data)


def part2(data):
    pass


def solve():
    data = load_lines(10)
    remove_chars = "{}[]()"
    parsed_data = []
    for row in data:
        table = str.maketrans("", "", remove_chars)
        result = row.translate(table).split()
        raw_light_diagram, *raw_buttons, raw_joltage = result
        diagram_len = len(raw_light_diagram)
        button_masks = []
        for btn_str in raw_buttons:
            mask = [0] * diagram_len
            indices = map(int, btn_str.split(","))
            for idx in indices:
                if 0 <= idx < diagram_len:
                    mask[idx] = 1
            button_masks.append(mask)

        machine = Machine(
            starting_state=[0] * diagram_len,
            light_diagram=[0 if char == "." else 1 for char in raw_light_diagram],
            buttons=button_masks,
            joltage=set(map(int, raw_joltage.split(","))),
        )
        parsed_data.append(machine)
    data = parsed_data
    return part1(data), part2(data)
