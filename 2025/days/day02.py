from utils.loader import load_lines


def check_value(value, k, chunk_length):
    reference = value[:chunk_length]

    for i in range(1, k):
        if value[i * chunk_length : (i + 1) * chunk_length] != reference:
            return
    return value


def part1(data):
    id_ranges = [item for line in data for item in line.split(",")]

    invalid_sum = 0
    for id_range in id_ranges:
        start, end = tuple(id_range.split("-"))

        for i in range(int(start), int(end) + 1):
            value = f"{i}"

            length = len(value)
            if length % 2 != 0:
                continue

            half_length = length // 2
            result = check_value(value, 2, half_length)
            if result:
                invalid_sum += int(value)

    return invalid_sum


def part2(data):
    id_ranges = [item for line in data for item in line.split(",")]

    invalid_sum = 0
    for id_range in id_ranges:
        start, end = tuple(id_range.split("-"))

        for i in range(int(start), int(end) + 1):
            value = f"{i}"
            length = len(value)

            max_k = length

            for j in range(2, max_k + 1):
                if length % j == 0:
                    chunk_length = length // j
                    result = check_value(value, j, chunk_length)
                    if result:
                        invalid_sum += int(result)
                        break
    return invalid_sum


def solve():
    data = load_lines(2)
    return part1(data), part2(data)
