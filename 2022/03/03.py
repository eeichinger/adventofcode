#!/usr/bin/python3

from typing import List, Set

ITEM_PRIORITY = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def split_rucksack_compartments(rucksack) -> List[Set]:
    rucksack_size = len(rucksack)
    comp_size = rucksack_size//2
    comp1_set = set(rucksack[:comp_size])
    comp2_set = set(rucksack[comp_size:])
    return [comp1_set, comp2_set]


def find_shared_itemtype(compartments: List[Set]) -> str:
    [comp1set, comp2set] = compartments
    common_el = (comp1set & comp2set).pop()
    return common_el


def determine_itemtype_prio(item: str) -> int:
    prio = ITEM_PRIORITY.index(item)
    return prio


def determine_rucksack_prio(line:str) -> int:
    compartments = split_rucksack_compartments(line.strip())
    itemtype = find_shared_itemtype(compartments)
    prio = determine_itemtype_prio(itemtype)
    # print("itemtype:", itemtype, ", prio:", prio)
    return prio


def calculate_prios_sum(input: List[str]) -> int:
    prios = [determine_rucksack_prio(line) for line in input]
    return sum(prios)


with open('03.txt') as f:
    total_prio = calculate_prios_sum(f)
    print("total_prio:", total_prio)

# print(ord('A'))
# print(ord('a'))
# print(chr(ord('A')-1))
# print(chr(ord('a')-1))
