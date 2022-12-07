#!/usr/bin/env python3

from typing import List, Set, Dict, Iterable
import re


def main(source: Iterable[str], expected_result: str) -> None:
    # customised: first line contains expected size for auto-verification:
    #   expected_size_part1:expected_size_part2
    (expected_res1, expected_res2) = [res for res in expected_result.split(":")]

    result = 0
    assert expected_res1 == result


if __name__ == '__main__':
    with open('08-test.txt') as f:
        expected = f.readline()
        main(f, expected)
    with open('08-data.txt') as f:
        expected = f.readline()
        main(f, expected)

