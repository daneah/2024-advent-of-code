#!/usr/bin/env -S uv run -q
# /// script
# requires-python = ">=3.12"
# ///
import re


MUL = re.compile(r"^mul\((\d+),(\d+)\)")
DO = re.compile(r"^do\(\)")
DONT = re.compile(r"^don't\(\)")


def _calc(expression: str, consider_enablers: bool = False) -> int:
    total = 0
    enabled = True

    while expression:
        if match := MUL.match(expression):
            if enabled or not consider_enablers:
                total += int(match.group(1)) * int(match.group(2))
                expression = expression[match.end():]
            else:
                expression = expression[1:]
        elif match := DO.match(expression):
            enabled = True
            expression = expression[match.end():]
        elif match := DONT.match(expression):
            enabled = False
            expression = expression[match.end():]
        else:
            expression = expression[1:]

    return total


def _get_data() -> str:
    with open("data.txt") as data_file:
        return data_file.read().replace("\n", "")


if __name__ == "__main__":
    # Part one
    print(_calc(_get_data()))

    # Part two
    print(_calc(_get_data(), True))
