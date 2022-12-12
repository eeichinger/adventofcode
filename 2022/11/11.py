#!/usr/bin/env python3
import copy
from typing import List, Set, Iterable
import math

monkeys_part1_test = [[
    [79, 98],
    lambda old: old * 19,
    23,
    2,
    3,
    0
], [
    [54, 65, 75, 74],
    lambda old: old + 6,
    19,
    2,
    0,
    0
], [
    [79, 60, 97],
    lambda old: old * old,
    13,
    1,
    3,
    0
], [
    [74],
    lambda old: old + 3,
    17,
    0,
    1,
    0
]]

monkeys_part1 = [
    [
        [96, 60, 68, 91, 83, 57, 85],
        lambda old: old * 2,
        17,
        2,
        5,
        0
    ],
    [
        [75, 78, 68, 81, 73, 99],
        lambda old: old + 3,
        13,
        7,
        4,
        0
    ],
    [
        [69, 86, 67, 55, 96, 69, 94, 85],
        lambda old: old + 6,
        19,
        6,
        5,
        0
    ],
    [
        [88, 75, 74, 98, 80],
        lambda old: old + 5,
        7,
        7,
        1,
        0
    ],
    [
        [82],
        lambda old: old + 8,
        11,
        0,
        2,
        0
    ],
    [
        [72, 92, 92],
        lambda old: old * 5,
        3,
        6,
        3,
        0
    ],
    [
        [74, 61],
        lambda old: old * old,
        2,
        3,
        1,
        0
    ],
    [
        [76, 86, 83, 55],
        lambda old: old + 4,
        5,
        4,
        0,
        0
    ],
]


def take_turn(round_nr: int, monkeys: List, cur_monkey_index: int, kgv: int):
    cur_monkey = monkeys[cur_monkey_index]
    worry_levels = cur_monkey[0]
    op = cur_monkey[1]
    test_val = cur_monkey[2]
    target_monkey_true = cur_monkey[3]
    target_monkey_false = cur_monkey[4]

    cur_monkey[5] += len(worry_levels)  # inspections

    # print("{}: Monkey {}:".format(round_nr, cur_monkey_index))
    for worry_level in worry_levels:
        item = worry_level
        # print("inspecting item {}".format(item))
        worry_level = op(worry_level)
        cur_monkey[0] = cur_monkey[0][1:]
        if (kgv > 0):
            worry_level = worry_level % kgv
        else:
            worry_level //= 3

        if 0 == worry_level % test_val:
            # print(
            #     "{}:    item {} divisible by {}, throwing worry_level {} to monkey {}".format(round_nr, item, test_val,
            #                                                                                   worry_level,
            #                                                                                   target_monkey_true))
            monkeys[target_monkey_true][0].append(worry_level)
        else:
            # print(
            #     "{}:    item {} NOT divisible by {}, throwing worry_level {} to monkey {}".format(round_nr, item,
            #                                                                                       test_val,
            #                                                                                       worry_level,
            #                                                                                       target_monkey_false))
            monkeys[target_monkey_false][0].append(worry_level)


def main1(monkeys: List, total_rounds: int, expected_result: str) -> None:
    kgv = 0
    if total_rounds > 20:
        kgv = math.prod([monkey[2] for monkey in monkeys])
    for rounds in range(0, total_rounds):
        for cur_monkey_index in range(0, len(monkeys)):
            take_turn(rounds, monkeys, cur_monkey_index, kgv)
        if (rounds + 1 in [1, 20, 1000, 2000, 3000, 4000]):
            print("After round {}:".format(rounds + 1))
            for cur_monkey_index in range(0, len(monkeys)):
                print("    Monkey {}: inspections {}".format(cur_monkey_index, monkeys[cur_monkey_index][5]))

    inspections = sorted([cur_monkey[5] for cur_monkey in monkeys])
    top1 = inspections[-1]
    top2 = inspections[-2]
    result = top1 * top2
    print("result: {}, expected:{}".format(result, expected_result))
    assert result == int(expected_result)


def test():
    take_turn(0, monkeys_part1, 0)
    assert monkeys_part1[0][5] == 2


if __name__ == '__main__':
    # test()
    main1(copy.deepcopy(monkeys_part1_test), 20, "10605")
    main1(copy.deepcopy(monkeys_part1_test), 10000, "2713310158")
    main1(copy.deepcopy(monkeys_part1), 20, "56595")
    main1(copy.deepcopy(monkeys_part1), 10000, "15693274740")
    # with open('10-test.txt') as f:
    #     expected = f.readline()
    #     main(f.readlines(), expected)
    # with open('10-data.txt') as f:
    #     expected = f.readline()
    #     main(f.readlines(), expected)

# class Monkey:
#     def __init__(self, monkeys, operation, divisibleby, monkey_index_true, monkey_index_false):
#         self.monkeys = monkeys
#         self.items = []
#         self.operation = operation
#         self.divisibleby = divisibleby
#         self.monkey_index_true = monkey_index_true
#         self.monkey_index_false = monkey_index_false
#
#
#
