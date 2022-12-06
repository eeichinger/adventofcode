#!/usr/bin/python3

from typing import List, Set, Dict


def detect_message(input: str, marker_size: int, expected_result: int):
    result = 0
    buffer = []
    marker = ['not processed yet']
    for ch in input:
        buffer.append(ch)
        marker = buffer[-marker_size:]
        if len(set(marker)) == marker_size:
            result = len(buffer)
            break

    print("result: {}, expected_result:{}, marker:{}, buffer:{}"
          .format(result, expected_result, "".join(marker), "".join(buffer)[:100]))
    assert result == expected_result


def main(source: List):
    for line in source:
        [input, marker_size, expected_result] = line.split(':')
        detect_message(input, int(marker_size), int(expected_result))


if __name__ == '__main__':
    with open('06-data-1.txt') as f:
        main(f)
    with open('06-data-2.txt') as f:
        main(f)
