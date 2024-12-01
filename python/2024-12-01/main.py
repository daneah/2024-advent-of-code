#!/usr/bin/env -S uv run -q
# /// script
# requires-python = ">=3.12"
# ///
from collections import Counter
from csv import reader
from typing import Generator


def _int_reader(csv_reader):
    for row in csv_reader:
        yield [int(cell) for cell in row]


def _get_data() -> Generator[list[int], None, None]:
    with open("data.csv") as data_file:
        for row in _int_reader(reader(data_file)):
            yield row


if __name__ == "__main__":
    data = _get_data()
    list_one, list_two = zip(*data)

    # Part one
    comparable_data = zip(sorted(list_one), sorted(list_two))
    print(sum(abs(list_one_item - list_two_item) for list_one_item, list_two_item in comparable_data))

    # Part two
    frequencies = Counter(list_two)
    print(sum(location_id * frequencies[location_id] for location_id in list_one))
