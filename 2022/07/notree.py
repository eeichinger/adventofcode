#!/usr/bin/env python3

from typing import List, Set, Dict
import re


def is_int(val):
    return val.lstrip("-+").isdigit()


def cd(curdir: List[str], targetdir) -> List[str]:
    if targetdir == '/':
        curdir = []
    elif targetdir == '..':
        curdir.pop()
    else:
        curdir = curdir + [targetdir]
    return curdir


def to_dirpath(curdir: List[str]) -> str:
    dirpath = "/" + "/".join(curdir)
    if len(dirpath) > 1:
        dirpath += "/"
    return dirpath


def to_filepath(curdir: List[str], filename) -> str:
    filepath = curdir + [filename]
    return "/" + "/".join(filepath)


def main(source: List[str]) -> None:
    curdir = []  # current directory parts list, e.g. '/a/e' as [ 'a', 'e' ]
    filesizes = dict()  # dict with key=fq filepath, val=size
    dirset = set()  # set of unique fq dir names

    # customised: first line contains expected size for auto-verification:
    #   expected_size_part1:expected_size_part2
    (expected_size1, expected_size2) = [int(sise) for sise in source[0].split(":")]

    for line in source[1:]:
        argv = line.strip().split(' ')
        if argv[0] == '$' and argv[1] == 'cd':
            # found cd instr, calc new curdir
            curdir = cd(curdir, argv[2])
            dirpath = to_dirpath(curdir)  # convert path fragments to path string with begin&trailing slash
            dirset.add(dirpath)  # record dir name (set auto-dedups names)
        elif is_int(argv[0]):
            # found file, record filesize with full path
            filepath = to_filepath(curdir, argv[1])
            filesizes[filepath] = int(argv[0])
    # print(dirset)
    # print(filesizes)
    total_dir_sizes = dict()
    # calculate total size for each dir
    for adir in dirset:
        # find all files under adir
        dirfilesizes = [val for key, val in filesizes.items() if key.startswith(adir)]
        total_dir_size = sum(dirfilesizes)
        # print("dir: {}, size:{}, files:{}".format(adir, total_dir_size, dirfilesizes))
        total_dir_sizes[adir] = total_dir_size
    # print(total_dir_sizes)

    # part 1
    nodes_smaller_than_100000 = [adirsize for adirsize in total_dir_sizes.values() if adirsize <= 100000]
    total_size_nodes_smaller_than_100000 = sum(nodes_smaller_than_100000)
    print(total_size_nodes_smaller_than_100000)
    assert total_size_nodes_smaller_than_100000 == expected_size1

    # part 2
    total_used_size = total_dir_sizes['/']
    unused_size = 70000000 - total_used_size
    need_to_free = 30000000 - unused_size
    nodes_larger_than_need_to_free = [adirsize for adirsize in total_dir_sizes.values() if adirsize >= need_to_free]
    smallest_dirsize = min(nodes_larger_than_need_to_free)
    print(smallest_dirsize)
    assert smallest_dirsize == expected_size2


if __name__ == '__main__':
    with open('07-test.txt') as f:
        main(f.readlines())
    with open('07-data.txt') as f:
        main(f.readlines())
