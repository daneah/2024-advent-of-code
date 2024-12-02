#!/usr/bin/env -S uv run -q
# /// script
# requires-python = ">=3.12"
# ///
from typing import Generator


def _get_data():
    with open("data.txt") as data_file:
        for line in data_file:
            yield [int(level) for level in line.split()]


def _get_dampened_levels(all_levels: list[int]) -> Generator[list[int], None, None]:
    for index in range(len(all_levels)):
        dampened_levels = all_levels.copy()
        del dampened_levels[index]
        yield dampened_levels


def _is_safe_report(all_levels: list[int], dampen: bool) -> bool:
    levels, next_levels = all_levels[:-1], all_levels[1:]
    comparables = list(zip(levels, next_levels))
    monotonic = all(n > p for p, n in comparables) or all(n < p for p, n in comparables)
    safe_jumps = all(1 <= abs(n - p) <= 3 for p, n in comparables)

    if monotonic and safe_jumps:
        return True
    elif dampen:
        return any(_is_safe_report(dampened_levels, False) for dampened_levels in _get_dampened_levels(all_levels))
    return False


if __name__ == "__main__":
    # Part one
    print(sum(_is_safe_report(row, False) for row in _get_data()))

    # Part two
    print(sum(_is_safe_report(row, True) for row in _get_data()))
