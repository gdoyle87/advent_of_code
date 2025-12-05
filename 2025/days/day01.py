from utils.loader import load_lines

MIN_DIAL = 0
MAX_DIAL = 99
OFFSET = 100
DIAL_START = 50


def part1(data):
    dial_position = DIAL_START
    counter = 0

    for row in data:
        if row and len(row) > 1:
            value = row
            direction = -1 if value[0].lower() == "l" else 1
            length = int(value[1:])

            while length > 0:
                dial_position += 1 * direction

                if dial_position > MAX_DIAL:
                    dial_position -= OFFSET
                elif dial_position < MIN_DIAL:
                    dial_position += OFFSET

                length -= 1
            if dial_position == 0:
                counter += 1
    return counter


def part2(data):
    dial_position = DIAL_START
    counter = 0

    for row in data:
        if row and len(row) > 1:
            value = row
            direction = -1 if value[0].lower() == "l" else 1
            length = int(value[1:])

            while length > 0:
                dial_position += 1 * direction

                if dial_position > MAX_DIAL:
                    dial_position -= OFFSET
                elif dial_position < MIN_DIAL:
                    dial_position += OFFSET

                length -= 1

                if dial_position == 0:
                    counter += 1
    return counter


def solve():
    data = load_lines(day=1)
    return part1(data), part2(data)
