from utils.loader import load_grid


def part1(data):
    height = len(data)
    width = len(data[0])
    start_column = data[0].index("S")

    total_splits = 0

    # Initialize the BeamArray table
    BeamArray = [[0 for _ in range(width)] for _ in range(height)]

    # Add a beam for S
    BeamArray[0][start_column] = 1

    for row in range(1, height - 1):
        for col in range(width):
            beams_arriving = BeamArray[row - 1][col]

            # if there is no beam here, skip to next
            if beams_arriving == 0:
                continue

            field_value = data[row][col]

            # if this is NOT a splitter, continue the beam down
            if field_value == ".":
                BeamArray[row][col] = 1

            # if this is a splitter
            elif field_value == "^":
                # increment splits
                total_splits += 1

                # bounds checks (only update if in bounds)
                if (col - 1) >= 0:
                    BeamArray[row][col - 1] = 1
                if (col + 1) < width:
                    BeamArray[row][col + 1] = 1

    return total_splits


def part2(data):
    height = len(data)
    width = len(data[0])
    start_column = data[0].index("S")

    total_splits = 0

    # Initialize the BeamArray table
    BeamArray = [[0 for _ in range(width)] for _ in range(height)]

    # Add a beam for S
    BeamArray[0][start_column] = 1

    for row in range(1, height):
        for col in range(width):
            beams_arriving = BeamArray[row - 1][col]

            # if there is no beam here, skip to next
            if beams_arriving == 0:
                continue

            field_value = data[row][col]

            # if this is NOT a splitter, continue the beam down
            if field_value == ".":
                BeamArray[row][col] += beams_arriving

            # if this is a splitter
            elif field_value == "^":
                # increment splits
                total_splits += beams_arriving

                # bounds checks (only update if in bounds)
                if (col - 1) >= 0:
                    BeamArray[row][col - 1] += beams_arriving
                if (col + 1) < width:
                    BeamArray[row][col + 1] += beams_arriving

    return sum(BeamArray[-1])


def solve():
    data = load_grid(7)
    return part1(data), part2(data)
