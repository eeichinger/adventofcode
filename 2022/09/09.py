#!/usr/bin/env python3

from typing import List, Set, Iterable
import math


def sgn(val: int) -> int:
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return -1


def move(knot: tuple[int, int], x: int, y: int):
    return (knot[0] + x, knot[1] + y)


def move_rope_head_single_step(rope: List[tuple[int, int]], x, y) -> List[tuple[int, int]]:
    new_rope = [move(rope[0], x, y)]
    # print("move head {}, x={}, y={}".format(rope[0], x, y))
    for i in range(0, len(rope) - 1):
        (new_posH, new_posT) = move_single_knot(rope[i], new_rope[i], rope[i + 1])
        new_rope.append(new_posT)
        # print("processed knot[{}]={}, knot[{}]={}".format(i, new_rope[i], i+1, new_rope[i+1]))
    return new_rope


def move_single_knot(old_posH: tuple[int, int], new_posH: tuple[int, int], posT: tuple[int, int]):
    diff = (new_posH[0] - posT[0], new_posH[1] - posT[1])
    # print("diff({}, {})".format(diff[0], diff[1]))
    if (abs(diff[0]) > 1 or abs(diff[1]) > 1):
        # move towards head
        vec = (sgn(diff[0]), sgn(diff[1]))
        # print("head to far way, moving tail vec({}, {})".format(vec[0], vec[1]))
        posT = (posT[0] + vec[0], posT[1] + vec[1])
    # print("posH[{}], posT[{}]".format(new_posH, posT))
    return (new_posH, posT)


def processInstruction(instr: tuple[str, int], rope: List[tuple[int, int]], visitedT: Set[tuple[int, int]]) \
    -> tuple[List[tuple[int, int]], set[tuple[int, int]]]:
    (direction, steps) = instr
    # print("processing dir:{}, steps:{}".format(direction, steps))
    if direction.lower() == "r":
        for step in range(0, steps):
            rope = move_rope_head_single_step(rope, 1, 0)
            # print("tail now at {}".format(rope[-1]))
            visitedT.add(rope[-1])
    elif direction.lower() == "l":
        for step in range(0, steps):
            rope = move_rope_head_single_step(rope, -1, 0)
            # print("tail now at {}".format(rope[-1]))
            visitedT.add(rope[-1])
    elif direction.lower() == "u":
        for step in range(0, steps):
            rope = move_rope_head_single_step(rope, 0, 1)
            # print("tail now at {}".format(rope[-1]))
            visitedT.add(rope[-1])
    elif direction.lower() == "d":
        for step in range(0, steps):
            rope = move_rope_head_single_step(rope, 0, -1)
            # print("tail now at {}".format(rope[-1]))
            visitedT.add(rope[-1])
    else:
        print("cant process {}".format(instr))
        assert False
    return (rope, visitedT)


def main(source: Iterable[str], expected_result: str) -> None:
    (expected_result1, expected_result2) = [int(res) for res in expected_result.split(":")]
    run(source, 2, expected_result1)
    run(source, 10, expected_result2)


def run(source: Iterable[str], rope_length: int, expected_result: str) -> None:
    rope = [(0, 0) for i in range(0, rope_length)]
    visitedT: Set[tuple[int, int]] = set()
    visitedT.add(rope[-1])
    for line in source:
        (direction, stepsStr) = line.split(" ")
        instr = (direction, int(stepsStr))
        (rope, visitedT) = processInstruction(instr, rope, visitedT)

    result = len(visitedT)
    print("visited: {}, expected: {}".format(result, expected_result))
    assert result == expected_result


def test_same_position_move_step_right():
    # test: same position, move right
    rope = move_rope_head_single_step([(0, 0), (0, 0), (0, 0)], 1, 0)
    assert rope[0] == (1, 0)
    assert rope[1] == (0, 0)
    assert rope[2] == (0, 0)
    rope = move_rope_head_single_step([(1, 0), (0, 0), (0, 0)], 1, 0)
    assert rope[0] == (2, 0)
    assert rope[1] == (1, 0)
    assert rope[2] == (0, 0)


def test_oneoff_position_move_step_right():
    rope1 = [(1, 0), (0, 0), (0, 0)]
    rope = move_rope_head_single_step(rope1, 1, 0)
    assert rope[0] == (2, 0)
    assert rope[1] == (1, 0)
    assert rope[2] == (0, 0)

    rope2 = [(1, 1), (0, 0), (0, 0)]
    rope = move_rope_head_single_step(rope2, 1, 0)
    assert rope[0] == (2, 1)
    assert rope[1] == (1, 1)
    assert rope[2] == (0, 0)

    rope3 = [(0, 0), (1, 0), (2, 0)]
    rope = move_rope_head_single_step(rope3, 1, 0)
    assert rope[0] == (1, 0)
    assert rope[1] == (1, 0)
    assert rope[2] == (2, 0)


def test_oneoff_position_move_step_up():
    rope1 = [(3, 1), (2, 0), (1, 0), (0, 0), (0, 0)]
    rope = move_rope_head_single_step(rope1, 0, 1)
    assert rope[0] == (3, 2)
    assert rope[1] == (3, 1)
    assert rope[2] == (2, 1)
    assert rope[3] == (1, 1)
    assert rope[4] == (0, 0)


if __name__ == '__main__':
    # test_same_position_move_step_right()
    # test_oneoff_position_move_step_right()
    # test_oneoff_position_move_step_up()
    with open('09-test.txt') as f:
        expected = f.readline()
        main(f.readlines(), expected)
    with open('09-test2.txt') as f:
        expected = f.readline()
        main(f.readlines(), expected)
    with open('09-data.txt') as f:
        expected = f.readline()
        main(f.readlines(), expected)
