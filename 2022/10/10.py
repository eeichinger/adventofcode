#!/usr/bin/env python3

from typing import List, Set, Iterable
import math


def main(source: Iterable[str], expected_result: str) -> None:
    (expected_result1, expected_result2) = [int(res) for res in expected_result.split(":")]
    # 20, 60, 100, 140, 180, 220

    X = 1
    cycle = 0
    signals = [X]
    instructions = [line.strip().split() for line in source]
    for instr in instructions:
        if instr[0] == "noop":
            cycle += 1
            signals.append(X)
        elif instr[0] == "addx":
            signals.append(X)
            signals.append(X)
            cycle += 2
            X += int(instr[1])
        print("signals[{}]={}".format(cycle, X))

    strengths = [c*signals[c] for c in [20, 60, 100, 140, 180, 220]]
    total = sum(strengths)
    print("result: {}, expected:{}".format(total, expected_result1))
    assert total == expected_result1


if __name__ == '__main__':
    with open('10-test.txt') as f:
        expected = f.readline()
        main(f.readlines(), expected)
    with open('10-data.txt') as f:
        expected = f.readline()
        main(f.readlines(), expected)
