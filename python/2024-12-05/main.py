#!/usr/bin/env -S uv run -q
# /// script
# requires-python = ">=3.12"
# ///
import contextlib
from collections import defaultdict


def _get_data() -> tuple[dict[int, set[int]], list[list[int]]]:
    rules = defaultdict(set)
    all_pages = []

    with open("data.txt") as data_file:
        while (line := data_file.readline().strip()) != "":
            before, after = line.split("|")
            rules[int(before)].add(int(after))

        while (line := data_file.readline().strip()) != "":
            pages = line.split(",")
            all_pages.append([int(page) for page in pages])

    return rules, all_pages


def _get_invalid_middle_pages(rules: dict[int, set[int]], pages: list[int]) -> int:
    fixed = False
    for before, afters in rules.items():
        for after in afters:
            with contextlib.suppress(ValueError):
                if pages.index(before) > pages.index(after):
                    pages.remove(before)
                    pages.insert(pages.index(after), before)
                    fixed = True
    return pages[len(pages) // 2] if fixed else 0


def _get_valid_middle_pages(rules: dict[int, set[int]], pages: list[int]) -> int:
    for before, afters in rules.items():
        for after in afters:
            with contextlib.suppress(ValueError):
                if pages.index(before) > pages.index(after):
                    return 0
    return pages[len(pages) // 2]


if __name__ == "__main__":
    # Part one
    rules, all_pages = _get_data()
    print(sum(_get_valid_middle_pages(rules, pages) for pages in all_pages))

    # Part two
    rules, all_pages = _get_data()
    print(sum(_get_invalid_middle_pages(rules, pages) for pages in all_pages))
