#!/usr/bin/python3

from typing import List, Set

ITEM_PRIORITY = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def split_rucksack_compartments(rucksack) -> List[Set]:
    N = 2  # number of evenly sized compartments
    rucksack_size = len(rucksack)
    comp_size = rucksack_size // N
    compartments = [rucksack[i:i + comp_size] for i in range(0, len(rucksack), comp_size)]
    return compartments


def find_shared_itemtype(compartments: List[str]) -> str:
    sets = [set(compartment) for compartment in compartments]
    return set.intersection(*sets).pop()


def determine_itemtype_prio(item: str) -> int:
    prio = ITEM_PRIORITY.index(item)
    return prio


def determine_rucksack_prio(rucksack: str) -> int:
    compartments = split_rucksack_compartments(rucksack)
    itemtype = find_shared_itemtype(compartments)
    prio = determine_itemtype_prio(itemtype)
    return prio


def calculate_prio_total(rucksacks: List[str]) -> int:
    prios = [determine_rucksack_prio(rucksack) for rucksack in rucksacks]
    prios_total = sum(prios)
    return prios_total


def calculate_badge_prio_total(rucksacks) -> int:
    N = 3  # group size
    grouped_rucksacks = [rucksacks[i:i + N] for i in range(0, len(rucksacks), N)]
    badges = [find_shared_itemtype(group) for group in grouped_rucksacks]
    badge_prios = [determine_itemtype_prio(badge) for badge in badges]
    total_badge_prios = sum(badge_prios)
    return total_badge_prios


def main(fname: str):
    with open(fname) as f:
        rucksacks: List[str] = [line.strip() for line in f]

    total_prio = calculate_prio_total(rucksacks)
    print("total_prio:", total_prio)

    total_badge_prio = calculate_badge_prio_total(rucksacks)
    print("total_badge_prio:", total_badge_prio)


if __name__ == '__main__':
    main('03.txt')
