from collections import namedtuple

from utils.loader import load_lines

Machine = namedtuple("Machine", ["diagram_len", "light_diagram", "buttons", "joltage"])


def part1(data):
    print(data)


def part2(data):
    pass


def solve():
    data = load_lines(10)
    remove_chars = "{}[]()"
    parsed_data = []
    for row in data:
        # remove brackets
        table = str.maketrans("", "", remove_chars)
        result = row.translate(table).split()

        # unpack the result
        raw_light_diagram, *raw_buttons, raw_joltage = result

        diagram_len = len(raw_light_diagram)

        target_int = 0
        for i, char in enumerate(raw_light_diagram):
            if char == "#":
                target_int |= 1 << i

        button_masks = []
        for btn_str in raw_buttons:
            mask = 0
            indices = map(int, btn_str.split(","))
            for idx in indices:
                mask |= 1 << idx
            button_masks.append(mask)

        machine = Machine(
            diagram_len=diagram_len,
            light_diagram=target_int,
            buttons=button_masks,
            joltage=set(map(int, raw_joltage.split(","))),
        )
        parsed_data.append(machine)
    return part1(parsed_data), part2(parsed_data)
