#!/usr/bin/python3

from typing import List, Set


def convert_assignment_string_to_ranges(assigment_str: str) -> List:
    lower_upper_bounds = assigment_str.split('-')
    assigned_sections = range(int(lower_upper_bounds[0]), int(lower_upper_bounds[1])+1)
    return assigned_sections


def group_elements(alist: List, n: int) -> List:
    return [alist[i:i + n] for i in range(0, len(alist), n)]


def determine_total_overlap(ranges: List[range]) -> List:
    sets = [set(r) for r in ranges]
    overlap = set.intersection(*sets)
    return 1 if overlap in sets else 0


def determine_any_overlap(ranges: List[range]) -> List:
    sets = [set(r) for r in ranges]
    overlap = set.intersection(*sets)
    return 1 if len(overlap) > 0 else 0


def main(fname: str):
    with open(fname) as f:
        pair_assigments: List[str] = [line.strip().split(',') for line in f]
    # print(pair_assigments)
    flattened_assigments = [assignment for pair in pair_assigments for assignment in pair]
    # print(flattened_assigments)
    assigned_section_ranges_list = [convert_assignment_string_to_ranges(assignment)
                                    for assignment in flattened_assigments]
    # print(assigned_section_ranges_list)
    grouped_by_pair = group_elements(assigned_section_ranges_list, 2)
    # print(grouped_by_pair)
    total_overlaps = map(determine_total_overlap, grouped_by_pair)
    print("total overlaps:", sum(total_overlaps))
    any_overlaps = map(determine_any_overlap, grouped_by_pair)
    print("any overlaps:", sum(any_overlaps))


if __name__ == '__main__':
    main('04.txt')
