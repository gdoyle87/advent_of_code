from utils.loader import load_lines


def check_neighbours(array, x, y, min_x, min_y, max_x, max_y):
    if array[x][y] != "@":
        return False
    counter = 0
    for i in [x - 1, x, x + 1]:
        if i < min_x or i >= max_x:
            continue
        for j in [y - 1, y, y + 1]:
            if j < min_y or j >= max_y:
                continue
            if i == x and j == y:
                continue
            if array[i][j] == "@":
                counter += 1
    return counter < 4


def get_count(array):
    max_x = len(array[0])
    max_y = len(array)
    total = 0
    for i in range(max_x):
        for j in range(max_y):
            result = check_neighbours(array, i, j, 0, 0, max_x, max_y)
            if result:
                total += 1
    return total


def display_array(array, max_x, max_y):
    for i in range(max_x):
        for j in range(max_y):
            print(array[i][j], end="")
        print()
    return


def part1(data):
    array = [list(line) for line in data]
    return get_count(array)


def part2(data):
    array = [list(line) for line in data]
    max_x = len(array[0])
    max_y = len(array)
    total = get_count(array)

    result = 0
    while total > 0:
        copy = array.copy()
        for i in range(max_x):
            for j in range(max_y):
                check_result = check_neighbours(array, i, j, 0, 0, max_x, max_y)
                if check_result:
                    result += 1
                    copy[i][j] = "."
        array = copy
        total = get_count(array)

    # display_array(array, max_x, max_y)
    return result


def solve():
    data = load_lines(4)
    return part1(data), part2(data)
