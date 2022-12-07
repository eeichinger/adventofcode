#!/usr/bin/env python3

from typing import List, Set, Dict, Iterable
import re


def cd(curdir: List[str], targetdir) -> List[str]:
    if targetdir == '/':
        return []
    elif targetdir == '..':
        return curdir[:-1]
    return curdir + [targetdir]


def ensure_dir_initialized(total_dir_sizes: Dict[tuple, int], curdir: List[str]):
    dirpath = tuple(curdir)
    if dirpath not in total_dir_sizes:
        total_dir_sizes[dirpath] = 0


def update_total_size_recursive(total_dir_sizes: dict[tuple, int], curdir: List[str], size: int):
    total_dir_sizes[tuple(curdir)] += size
    if curdir:
        # update parent size if not already root
        update_total_size_recursive(total_dir_sizes, curdir[:-1], size)


def main(source: Iterable[str], expected_result: str) -> None:
    # customised: first line contains expected size for auto-verification:
    #   expected_size_part1:expected_size_part2
    (expected_size1, expected_size2) = [int(size) for size in expected_result.split(":")]

    curdir = []  # current directory parts list, e.g. '/a/e' as [ 'a', 'e' ]
    total_dir_sizes = dict()

    for line in source:
        argv = line.strip().split(' ')
        if argv[0] == '$' and argv[1] == 'cd':
            # found cd instr, calc new curdir
            curdir = cd(curdir, argv[2])
            ensure_dir_initialized(total_dir_sizes, curdir)
        elif argv[0].isdigit():
            # found file, add filesize in all dirs up the hierarchy
            update_total_size_recursive(total_dir_sizes, curdir, int(argv[0]))

    # part 1
    nodes_smaller_than_100000 = [adirsize for adirsize in total_dir_sizes.values() if adirsize <= 100000]
    total_size_nodes_smaller_than_100000 = sum(nodes_smaller_than_100000)
    print(total_size_nodes_smaller_than_100000)
    assert total_size_nodes_smaller_than_100000 == expected_size1

    # part 2
    total_used_size = total_dir_sizes[()]
    unused_size = 70000000 - total_used_size
    need_to_free = 30000000 - unused_size
    nodes_larger_than_need_to_free = [adirsize for adirsize in total_dir_sizes.values() if adirsize >= need_to_free]
    smallest_dirsize = min(nodes_larger_than_need_to_free)
    print(smallest_dirsize)
    assert smallest_dirsize == expected_size2


if __name__ == '__main__':
    with open('07-test.txt') as f:
        expected = f.readline()
        main(f, expected)
    with open('07-data.txt') as f:
        expected = f.readline()
        main(f, expected)
