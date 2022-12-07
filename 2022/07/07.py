#!/usr/bin/env python3

from typing import List, Set, Dict
from anytree import AnyNode, Resolver, ChildResolverError, RenderTree, PostOrderIter
import re


def is_int(val):
    return val.lstrip("-+").isdigit()


def find_child_node_by_id(curnode: AnyNode, node_id: str):
    r = Resolver("id")
    try:
        child = r.get(curnode, node_id)
        return child
    except ChildResolverError:
        return None


def add_node_to_parent(curnode: AnyNode, node_id: str, isdir: bool, size: int):
    return AnyNode(id=node_id, parent=curnode, isdir=isdir, size=size)


def cli_exec(curdir: AnyNode, argv: List[str]):
    # print("cli_exec")
    assert argv[0] == '$'
    cmd = argv[1]
    # print("cli_exec cmd:{}, val:{}".format(cmd, val))
    if cmd == 'ls':
        # print("cli_exec ls")
        return curdir
    if cmd == 'cd':
        val = argv[2]
        if val == "/":
            # print("cli_exec cd /")
            return curdir.root
        if val == '..':
            # print("cli_exec cd ..")
            return curdir.parent
        # normal subdir
        # print("cli_exec cd ./" + val)
        subdir = find_child_node_by_id(curdir, val)
        if not subdir:
            # print("cli_exec cd ./{}: adding new child".format(val))
            subdir = add_node_to_parent(curdir, val, True, 0)
        return subdir
    assert False


def take_while(condition, iterable):
    for item in iterable:
        if not condition(item):
            return
        yield item


def take_until(condition, iterable):
    for item in iterable:
        if condition(item):
            return
        yield item


def calc_dirsize(curdir: AnyNode):
    childsizes = [calc_dirsize(subdir) for subdir in curdir.children]
    return curdir.size + sum(childsizes)


def main(source: List[str]) -> None:
    rootdir = AnyNode(id='/', size=0, isdir=True)
    curdir = rootdir
    # customised: first line contains expected size for auto-verification
    expected_size = int(source[0])
    for line in source[1:]:
        parts = line.strip().split(' ')
        # print("processing: " + line)
        if parts[0] == '$':
            curdir = cli_exec(curdir, parts)
        if is_int(parts[0]):
            add_node_to_parent(curdir, parts[1], False, int(parts[0]))
    total_dir_sizes = [(adir.id, calc_dirsize(adir)) for adir in PostOrderIter(rootdir) if adir.isdir]
    nodes_smaller_than_100000 = [adir[1] for adir in total_dir_sizes if adir[1] <= 100000]
    total_size_nodes_smaller_than_100000 = sum(nodes_smaller_than_100000)
    # print(RenderTree(rootdir))
    print(total_size_nodes_smaller_than_100000)
    assert total_size_nodes_smaller_than_100000 == expected_size


if __name__ == '__main__':
    with open('07-test.txt') as f:
        main(f.readlines())
    with open('07-data.txt') as f:
        main(f.readlines())
