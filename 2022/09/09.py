#!/usr/bin/env python3

from typing import List, Set, Dict, Iterable
import re


def move_step_right(posH: tuple[int, int], posT: tuple[int, int], visitedT: Set[tuple[int, int]]):
    return move_step(posH, (posH[0] + 1, posH[1]), posT, visitedT)


def move_step_left(posH: tuple[int, int], posT: tuple[int, int], visitedT: Set[tuple[int, int]]):
    return move_step(posH, (posH[0] - 1, posH[1]), posT, visitedT)


def move_step_up(posH: tuple[int, int], posT: tuple[int, int], visitedT: Set[tuple[int, int]]):
    return move_step(posH, (posH[0], posH[1] + 1), posT, visitedT)


def move_step_down(posH: tuple[int, int], posT: tuple[int, int], visitedT: Set[tuple[int, int]]):
    return move_step(posH, (posH[0], posH[1] - 1), posT, visitedT)


def move_step(old_posH: tuple[int, int], new_posH: tuple[int, int], posT: tuple[int, int],
              visitedT: Set[tuple[int, int]]):
    if not(abs(new_posH[0] - posT[0]) <= 1 and abs(new_posH[1] - posT[1]) <= 1):
        posT = old_posH
    return (new_posH, posT, visitedT)


def processInstruction(instr: tuple[str, int], posH: tuple[int, int], posT: tuple[int, int],
                       visitedT: Set[tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int], set[tuple[int, int]]]:
    (direction, steps) = instr
    if direction.lower() == "r":
        for step in range(0, steps):
            (posH, posT, visitedT) = move_step_right(posH, posT, visitedT)
            visitedT.add(posT)
    elif direction.lower() == "l":
        for step in range(0, steps):
            (posH, posT, visitedT) = move_step_left(posH, posT, visitedT)
            visitedT.add(posT)
    elif direction.lower() == "u":
        for step in range(0, steps):
            (posH, posT, visitedT) = move_step_up(posH, posT, visitedT)
            visitedT.add(posT)
    elif direction.lower() == "d":
        for step in range(0, steps):
            (posH, posT, visitedT) = move_step_down(posH, posT, visitedT)
            visitedT.add(posT)
    else:
        print("cant process {}".format(instr))
        assert False
    return (posH, posT, visitedT)


def main(source: Iterable[str], expected_result: str) -> None:
    (expected_result1, expected_result2) = [int(res) for res in expected_result.split(":")]

    posH: tuple[int, int] = (0, 0)
    posT: tuple[int, int] = (0, 0)
    visitedT: Set[tuple[int, int]] = set()
    visitedT.add(posT)
    for line in source:
        (direction, stepsStr) = line.split(" ")
        instr = (direction, int(stepsStr))
        (posH, posT, visitedT) = processInstruction(instr, posH, posT, visitedT)

    result1 = len(visitedT)
    print("visited: {}, expected: {}".format(result1, expected_result1))
    assert result1 == expected_result1


def test_same_position_move_step_right():
    # test: same position, move right
    (newH, newT, visitedT) = move_step_right((0, 0), (0, 0), set())
    assert newH == (1, 0)
    assert newT == (0, 0)
    assert (0, 0) in visitedT


def test_oneoff_position_move_step_right():
    (newH, newT, visitedT) = move_step_right((1, 0), (0, 0), set())
    assert newH == (2, 0)
    assert newT == (1, 0)
    assert (1, 0) in visitedT

    (newH, newT, visitedT) = move_step_right((1, 1), (0, 0), set())
    assert newH == (2, 1)
    assert newT == (1, 1)
    assert (1, 1) in visitedT

    (newH, newT, visitedT) = move_step_right((0, 0), (1, 0), set())
    assert newH == (1, 0)
    assert newT == (1, 0)
    assert (1, 0) in visitedT


if __name__ == '__main__':
    # test_same_position_move_step_right()
    # test_oneoff_position_move_step_right()

    with open('09-test.txt') as f:
        expected = f.readline()
        main(f, expected)
    with open('09-test2.txt') as f:
        expected = f.readline()
        main(f, expected)
    with open('09-data.txt') as f:
        expected = f.readline()
        main(f, expected)
