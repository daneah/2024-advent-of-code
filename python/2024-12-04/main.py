#!/usr/bin/env -S uv run -q
# /// script
# requires-python = ">=3.12"
# ///
from typing import Generator

XMAS_PATTERNS = [
    [["X", "M", "A", "S"]],
    [["S", "A", "M", "X"]],
    [["X"], ["M"], ["A"], ["S"]],
    [["S"], ["A"], ["M"], ["X"]],
    [["X", ".", ".", "."],
     [".", "M", ".", "."],
     [".", ".", "A", "."],
     [".", ".", ".", "S"]],
    [["S", ".", ".", "."],
     [".", "A", ".", "."],
     [".", ".", "M", "."],
     [".", ".", ".", "X"]],
    [[".", ".", ".", "X"],
     [".", ".", "M", "."],
     [".", "A", ".", "."],
     ["S", ".", ".", "."]],
    [[".", ".", ".", "S"],
     [".", ".", "A", "."],
     [".", "M", ".", "."],
     ["X", ".", ".", "."]],
]

X_MAS_PATTERNS = [
    [["M", ".", "S"],
     [".", "A", "."],
     ["M", ".", "S"]],
    [["S", ".", "M"],
     [".", "A", "."],
     ["S", ".", "M"]],
    [["M", ".", "M"],
     [".", "A", "."],
     ["S", ".", "S"]],
    [["S", ".", "S"],
     [".", "A", "."],
     ["M", ".", "M"]],
]

def _get_data() -> list[list[str]]:
    with open("data.txt") as data_file:
        return [list(line) for line in data_file.readlines()]


def _get_sub_grids(grid: list[list[str]], width: int, height: int) -> Generator[list[list[str]], None, None]:
    for h in range(0, len(grid) - height + 1):
        for w in range(0, len(grid[0]) - width + 1):
            subgrid = [row[w:w + width] for row in grid[h:h + height]]
            yield subgrid


def _compare_grids(one: list[list[str]], two: list[list[str]]) -> bool:
    for grid_one_row, grid_two_row in zip(one, two):
        for item_one, item_two in zip(grid_one_row, grid_two_row):
            if item_one != item_two and item_one != ".":
                return False
    return True

def _find_xmas_count(grid: list[list[str]], x_mas: bool = False) -> int:
    total = 0
    patterns = X_MAS_PATTERNS if x_mas else XMAS_PATTERNS

    for pattern in patterns:
        for sub_grid in _get_sub_grids(grid, len(pattern[0]), len(pattern)):
            if _compare_grids(pattern, sub_grid):
                total += 1

    return total


if __name__ == "__main__":
    # Part one
    print(_find_xmas_count(_get_data()))

    # Part two
    print(_find_xmas_count(_get_data(), x_mas=True))
