from utils.loader import load_lines


def part1(data):
    total = 0
    for line in data:
        first_max = line[0]
        second_max = line[1]

        for i in range(1, len(line)):
            if i < len(line) - 1 and line[i] > first_max:
                first_max = line[i]
                second_max = line[i + 1]
            else:
                if line[i] > second_max:
                    second_max = line[i]
        total += int(f"{first_max}{second_max}")
    return total


def part2(data):
    total = 0
    stack_size = 12
    for line in data:
        stack = []
        line_length = len(line)

        for i in range(line_length):
            while (
                stack
                and (line[i] > stack[-1])
                and (((len(stack) - 1) + (line_length - i)) >= stack_size)
            ):
                stack.pop()
            if len(stack) < stack_size:
                stack.append(line[i])
        total += int("".join(stack))
    return total


def solve():
    data = load_lines(3)
    return part1(data), part2(data)
