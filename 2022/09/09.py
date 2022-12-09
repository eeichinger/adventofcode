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


def move_rope_head_single_step(rope: List[tuple[int, int]], x: int, y: int) -> List[tuple[int, int]]:
    rope[0] = move(rope[0], x, y)  # move head
    for i in range(0, len(rope) - 1):  # process remaining knots
        rope[i + 1] = move_next_knot(rope[i], rope[i + 1])
    return rope


def move_rope_head_multi_step(rope: List[tuple[int, int]], visitedT: Set[tuple[int, int]],
                              steps: int, x: int, y: int) -> None:
    for step in range(0, steps):
        move_rope_head_single_step(rope, x, y)
        visitedT.add(rope[-1])


def move_next_knot(pos: tuple[int, int], posNext: tuple[int, int]) -> tuple[int, int]:
    diff = (pos[0] - posNext[0], pos[1] - posNext[1])
    if (abs(diff[0]) > 1 or abs(diff[1]) > 1):
        # move towards head if distance>1
        vec = (sgn(diff[0]), sgn(diff[1]))
        posNext = (posNext[0] + vec[0], posNext[1] + vec[1])
    return posNext


def process_instruction(instr: tuple[str, int], rope: List[tuple[int, int]], visitedT: Set[tuple[int, int]]) \
    -> None:
    (direction, steps) = instr
    # print("processing dir:{}, steps:{}".format(direction, steps))
    if direction.lower() == "r":
        move_rope_head_multi_step(rope, visitedT, steps, 1, 0)
    elif direction.lower() == "l":
        move_rope_head_multi_step(rope, visitedT, steps, -1, 0)
    elif direction.lower() == "u":
        move_rope_head_multi_step(rope, visitedT, steps, 0, 1)
    elif direction.lower() == "d":
        move_rope_head_multi_step(rope, visitedT, steps, 0, -1)
    else:
        print("cant process {}".format(instr))
        assert False


def main(source: Iterable[str], expected_result: str) -> None:
    (expected_result1, expected_result2) = [int(res) for res in expected_result.split(":")]
    run(source, 2, expected_result1)
    run(source, 10, expected_result2)


def run(source: Iterable[str], rope_length: int, expected_result: str) -> None:
    rope = [(0, 0) for _ in range(0, rope_length)]
    visitedT: Set[tuple[int, int]] = set()
    visitedT.add(rope[-1])
    for line in source:
        (direction, stepsStr) = line.split(" ")
        instr = (direction, int(stepsStr))
        process_instruction(instr, rope, visitedT)

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
    test_same_position_move_step_right()
    test_oneoff_position_move_step_right()
    test_oneoff_position_move_step_up()

    with open('09-test.txt') as f:
        expected = f.readline()
        main(f.readlines(), expected)
    with open('09-test2.txt') as f:
        expected = f.readline()
        main(f.readlines(), expected)
    with open('09-data.txt') as f:
        expected = f.readline()
        main(f.readlines(), expected)
