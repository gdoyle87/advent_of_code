from collections import deque, namedtuple

from utils.loader import load_lines

Machine = namedtuple("Machine", ["diagram_len", "light_diagram", "buttons", "joltage"])


def part1(data):
    total_presses = 0
    for machine in data:
        masks = []
        for button in machine.buttons:
            mask = 0
            for idx in button:
                mask |= 1 << idx
            masks.append(mask)

        starting_state = 0
        seen = {starting_state}
        queue = deque([(starting_state, 0)])

        while queue:
            current_state, steps = queue.popleft()

            if current_state == machine.light_diagram:
                total_presses += steps
                break

            for btn_mask in masks:
                next_state = current_state ^ btn_mask
                if next_state not in seen:
                    seen.add(next_state)
                    queue.append((next_state, steps + 1))

    return total_presses


def build_augmented_matrix(machine):
    n = len(machine.joltage)

    buttons = []
    for i in range(len(machine.buttons)):
        mapped_button = [i] + [0] * n
        for idx in machine.buttons[i]:
            mapped_button[idx + 1] = 1
        buttons.append(mapped_button)

    buttons.append([len(machine.buttons)] + list(machine.joltage))

    num_rows = len(buttons)
    num_cols = len(buttons[0])

    # build a transposed matrix
    matrix = [[0] * num_rows for _ in range(num_cols)]

    # fill the transposed matrix
    for i in range(num_cols):
        for j in range(num_rows):
            matrix[i][j] = buttons[j][i]

    return matrix


def find_smallest_nonzero(matrix, col, start_row):
    smallest_idx = None

    for i in range(start_row, len(matrix)):
        val = abs(matrix[i][col])
        if val == 0:
            continue

        if smallest_idx is None or val < abs(matrix[smallest_idx][col]):
            smallest_idx = i

    return smallest_idx


def find_next_pivot(matrix, start_row, start_col):
    best_row, best_col = None, None
    min = None

    for col in range(start_col, len(matrix[0]) - 1):  # skip the joltage col
        row = find_smallest_nonzero(matrix, col, start_row)

        if row is not None:
            current_val = abs(matrix[row][col])
            if min is None or current_val < min:
                min = current_val
                best_row = row
                best_col = col

    return (best_row, best_col)


def swap_rows(matrix, r1, r2):
    temp = matrix[r1]
    matrix[r1] = matrix[r2]
    matrix[r2] = temp


def swap_cols(matrix, c1, c2):
    for row in matrix:
        row[c1], row[c2] = row[c2], row[c1]


def reduce_row(matrix, target_row, source_row, quotient):
    for i in range(len(matrix[0])):
        matrix[target_row][i] -= quotient * matrix[source_row][i]


def forward_sweep(matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    # We start at row 1 because row 0 is the Index Row (Button IDs)
    curr_row = 1
    curr_col = 0

    while curr_row < num_rows and curr_col < num_cols - 1:
        while True:
            res = find_next_pivot(matrix, curr_row, curr_col)

            if res[0] is None:
                break

            p_row, p_col = res

            # Move the best pivot to the current diagonal position
            swap_rows(matrix, curr_row, p_row)
            swap_cols(matrix, curr_col, p_col)

            # Eliminate values in rows BELOW curr_row
            remainder_created = False
            for i in range(curr_row + 1, num_rows):
                if matrix[i][curr_col] != 0:
                    q = matrix[i][curr_col] // matrix[curr_row][curr_col]
                    if q != 0:
                        reduce_row(matrix, i, curr_row, q)

                    if matrix[i][curr_col] != 0:
                        remainder_created = True

            if not remainder_created:
                break
        curr_row += 1
        curr_col += 1

    return matrix


def backward_sweep(matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    # Work from bottom to top (skipping the index row at 0)
    for r in range(num_rows - 1, 0, -1):
        p_col = -1
        for c in range(num_cols - 1):
            if matrix[r][c] != 0:
                p_col = c
                break

        if p_col == -1:
            continue  # Skip zero rows

        if matrix[r][p_col] < 0:
            for c in range(num_cols):
                matrix[r][c] *= -1

        pivot_val = matrix[r][p_col]
        for above_r in range(1, r):
            if matrix[above_r][p_col] != 0:
                q = matrix[above_r][p_col] // pivot_val
                reduce_row(matrix, above_r, r, q)

    return matrix


def build_hnf_matrix(matrix):
    reduced_matrix = forward_sweep(matrix)
    hnf_matrix = backward_sweep(reduced_matrix)
    return hnf_matrix


def solve_free_vars_after_sweep(hnf_matrix):
    num_rows = len(hnf_matrix)
    num_cols = len(hnf_matrix[0]) - 1

    # Identify which columns are pivots and which are free variables
    pivot_rows = {}  # {col: row}
    free_cols = []

    for c in range(num_cols):
        found_pivot = False
        for r in range(1, num_rows):
            is_leading = True
            for prev_c in range(c):
                if hnf_matrix[r][prev_c] != 0:
                    is_leading = False
                    break

            if is_leading and hnf_matrix[r][c] != 0:
                pivot_rows[c] = r
                found_pivot = True
                break
        if not found_pivot:
            free_cols.append(c)

    # Try small values for free variables to satisfy non-negative constraint
    for val in range(101):  # Searching 0 to 100
        results = {hnf_matrix[0][c]: val for c in free_cols}
        possible = True

        for c, r in pivot_rows.items():
            # Pivot*Var + Sum(Coeff*FreeVar) = Target
            target = hnf_matrix[r][-1]
            sum_frees = sum(
                hnf_matrix[r][fc] * results[hnf_matrix[0][fc]] for fc in free_cols
            )

            coeff = hnf_matrix[r][c]
            remaining = target - sum_frees

            if remaining % coeff != 0 or (remaining // coeff) < 0:
                possible = False
                break
            results[hnf_matrix[0][c]] = remaining // coeff

        if possible:
            return results

    return None


def part2(data):
    total_presses = 0
    machine = data[0]

    for machine in data:
        # NOTE: this adds an index row for tracking after column swapping.
        augmented_matrix = build_augmented_matrix(machine)

        print("\n----- Augmented Matrix -----")
        for row in augmented_matrix:
            print(row)

        print("\n-------- HNF Matrix --------")
        hnf_matrix = build_hnf_matrix(augmented_matrix)
        for row in hnf_matrix:
            print(row)

        results = solve_free_vars_after_sweep(hnf_matrix)
        print(results)
        machine_presses = sum(val for _, val in results.items())
        print(machine_presses)
    return total_presses


def solve():
    data = load_lines(10)
    remove_chars = "{}[]()"
    parsed_data = []
    table = str.maketrans("", "", remove_chars)
    for row in data:
        result = row.translate(table).split()
        raw_light_diagram, *raw_buttons, raw_joltage = result

        diagram_len = len(raw_light_diagram)
        target_int = 0
        for i, char in enumerate(raw_light_diagram):
            if char == "#":
                target_int |= 1 << i

        parsed_buttons = []
        for button in raw_buttons:
            parsed_buttons.append(list(map(int, button.split(","))))

        machine = Machine(
            diagram_len=diagram_len,
            light_diagram=target_int,
            buttons=parsed_buttons,
            joltage=tuple(map(int, raw_joltage.split(","))),
        )
        parsed_data.append(machine)
    return part1(parsed_data), part2(parsed_data)
