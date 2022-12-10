#!/usr/bin/env python3

from typing import List, Set, Iterable
import math


def inc_cycle(screen: List[List[str]], signals: List[int], cur_reg: int):
    signals.append(cur_reg)
    screen_width = len(screen[0])
    cur_cycle = len(signals) - 1
    cur_line = cur_cycle // screen_width
    cur_linepos = cur_cycle % screen_width
    print("screen[{}][{}]".format(cur_line, cur_linepos))
    if cur_reg - 1 <= cur_linepos <= cur_reg + 1:
        screen[cur_line][cur_linepos] = '#'
    return len(signals)


def main(source: Iterable[str], expected_result: str, expected_screen: List[str]) -> None:
    X = 1
    signals = []
    screen = []
    for h in range(0, len(expected_screen)):
        screen_line = ['.' for _ in range(0, len(expected_screen[0]))]
        screen.append(screen_line)

    instructions = [line.strip().split() for line in source]
    for instr in instructions:
        if instr[0] == "noop":
            inc_cycle(screen, signals, X)
        elif instr[0] == "addx":
            inc_cycle(screen, signals, X)
            inc_cycle(screen, signals, X)
            X += int(instr[1])
        print("signals[{}]={}".format(len(signals), X))

    strengths = [c * signals[c - 1] for c in [20, 60, 100, 140, 180, 220]]
    total = sum(strengths)
    print("result: {}, expected:{}".format(total, expected_result))
    assert total == int(expected_result)

    display = []
    for screen_line in screen:
        display_line = "".join(screen_line)
        display.append(display_line)
        print(display_line)
    assert expected_screen == display


SCREEN_HEIGHT = 6
SCREEN_WIDTH = 40

if __name__ == '__main__':
    with open('10-test.txt') as f:
        expected = f.readline()
        expected_screen = [f.readline().strip() for _ in range(0, SCREEN_HEIGHT)]
        main(f.readlines(), expected, expected_screen)
    with open('10-data.txt') as f:
        expected = f.readline()
        expected_screen = [f.readline().strip() for _ in range(0, SCREEN_HEIGHT)]
        main(f.readlines(), expected, expected_screen)
