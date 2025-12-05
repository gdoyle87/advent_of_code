from utils.loader import load_lines


def split_input(input):
    index = 0
    for i in range(len(input)):
        if input[i] == "":
            index = i
            break
    return (input[:index], input[index + 1 :])


def merge_ranges(ranges):
    intervals = sorted(tuple(map(int, r.split("-"))) for r in ranges)
    merged = []
    for start, end in intervals:
        if not merged or start > merged[-1][1] + 1:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged


def part1(data):
    ranges, values = split_input(data)
    fresh_ids = merge_ranges(ranges)

    values = [int(v) for v in values]
    counter = 0
    for value in values:
        for id_range in fresh_ids:
            if value >= id_range[0] and value <= id_range[1]:
                counter += 1

    return counter


def part2(data):
    ranges, _ = split_input(data)
    fresh_ids = merge_ranges(ranges)

    count_of_fresh_ids = 0
    for id in fresh_ids:
        count = id[1] - id[0] + 1
        count_of_fresh_ids += count

    return count_of_fresh_ids


def solve():
    data = load_lines(5)
    return part1(data), part2(data)
