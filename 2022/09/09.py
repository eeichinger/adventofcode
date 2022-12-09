#!/usr/bin/env python3

from typing import List, Set, Iterable


def move(knot: tuple[int, int], x: int, y: int):
    return (knot[0] + x, knot[1] + y)


def move_rope_head_single_step(rope: List[tuple[int, int]], x, y) -> List[tuple[int, int]]:
    for i in range(0, len(rope) - 1):
        (new_posH, new_posT) = move_single_knot(rope[i], move(rope[i], x, y), rope[i + 1])
        rope[i] = new_posH
        rope[i + 1] = new_posT
    return rope


def move_single_knot(old_posH: tuple[int, int], new_posH: tuple[int, int], posT: tuple[int, int]):
    if not (abs(new_posH[0] - posT[0]) <= 1 and abs(new_posH[1] - posT[1]) <= 1):
        posT = old_posH
    # print("posH[{}], posT[{}]".format(new_posH, posT))
    return (new_posH, posT)


def processInstruction(instr: tuple[str, int], rope: List[tuple[int, int]], visitedT: Set[tuple[int, int]]) \
    -> tuple[List[tuple[int, int]], set[tuple[int, int]]]:
    (direction, steps) = instr
    # print("processing dir:{}, steps:{}".format(direction, steps))
    if direction.lower() == "r":
        for step in range(0, steps):
            rope = move_rope_head_single_step(rope, 1, 0)
            visitedT.add(rope[-1])
    elif direction.lower() == "l":
        for step in range(0, steps):
            rope = move_rope_head_single_step(rope, -1, 0)
            visitedT.add(rope[-1])
    elif direction.lower() == "u":
        for step in range(0, steps):
            rope = move_rope_head_single_step(rope, 0, 1)
            visitedT.add(rope[-1])
    elif direction.lower() == "d":
        for step in range(0, steps):
            rope = move_rope_head_single_step(rope, 0, -1)
            visitedT.add(rope[-1])
    else:
        print("cant process {}".format(instr))
        assert False
    return (rope, visitedT)


def main(source: Iterable[str], expected_result: str) -> None:
    (expected_result1, expected_result2) = [int(res) for res in expected_result.split(":")]

    rope = [(0, 0) for i in range(0, 2)]
    visitedT: Set[tuple[int, int]] = set()
    visitedT.add(rope[-1])
    for line in source:
        (direction, stepsStr) = line.split(" ")
        instr = (direction, int(stepsStr))
        (rope, visitedT) = processInstruction(instr, rope, visitedT)

    result1 = len(visitedT)
    print("visited: {}, expected: {}".format(result1, expected_result1))
    assert result1 == expected_result1


def test_same_position_move_step_right():
    # test: same position, move right
    rope1 = [(0, 0), (0, 0)]
    rope = move_rope_head_single_step(rope1, 1, 0)
    assert rope[0] == (1, 0)
    assert rope[-1] == (0, 0)


def test_oneoff_position_move_step_right():
    rope1 = [(1, 0), (0, 0)]
    rope = move_rope_head_single_step(rope1, 1, 0)
    assert rope[0] == (2, 0)
    assert rope[-1] == (1, 0)

    rope2 = [(1, 1), (0, 0)]
    rope = move_rope_head_single_step(rope2, 1, 0)
    assert rope[0] == (2, 1)
    assert rope[-1] == (1, 1)

    rope3 = [(0, 0), (1, 0)]
    rope = move_rope_head_single_step(rope3, 1, 0)
    assert rope[0] == (1, 0)
    assert rope[-1] == (1, 0)


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
