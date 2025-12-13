import numpy as np
import pandas as pd
from utils.loader import load_text

operation_map = {
    "+": np.sum,
    "*": np.prod,
}


def part1(data, op_codes):
    df = pd.DataFrame(data)

    df = df[0].str.split(expand=True)
    df = df.apply(pd.to_numeric)  # covert the values in df to numeric

    # Use dict comprehension to apply operations using the function pointers in
    # the "operation_map" global and passing it a column from the data frame.
    totals = {col: operation_map[op_codes[col]](df[col]) for col in df.columns}
    return sum(totals.values())


def part2(data, op_codes):
    # calculate the width of columns assuming fixed width
    data = [list(s) for s in data]
    df = pd.DataFrame(data)
    df_str = df.T.astype(str)
    concat = df_str.agg("".join, axis=1).str.strip().to_list()

    blocks = []
    current_block = []

    for item in concat:
        if item == "":
            if current_block:
                blocks.append(current_block)
                current_block = []
        else:
            current_block.append(int(item))
    if current_block:
        blocks.append(current_block)

    total = 0
    for i in range(len(blocks)):
        total += operation_map[op_codes[i]](blocks[i])

    return total


def solve():
    raw_data = load_text(6)
    # convert list of lists to a DataFrame; columns are auto-numbered (0, 1, 2, …)
    split_data = raw_data.split("\n")
    data, op_codes = split_data[:-1], split_data[-1].split()
    return part1(data, op_codes), part2(data, op_codes)
