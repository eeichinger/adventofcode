#!/usr/bin/python3

from typing import List, Set, Dict
import re


def take_until(condition, iterable):
    for item in iterable:
        if condition(item):
            return
        yield item


def parse_stack_spec_line(line: str, stack_dict: dict):
    text = (" "+line).replace("    ", " [_]").strip().replace("[", "").replace("]", "")
    specs = text.split(' ')
    for index, entry in enumerate(specs):
        stack_dict[index] = ([entry] if entry != '_' else []) + (stack_dict[index] if index in stack_dict else [])


def parse_stack_spec(file: List) -> Dict:
    pattern = re.compile("(\\s\\d\\s)+")  # read until spec up to stackindex line
    stack_dict = dict()
    for line in take_until(lambda l: pattern.match(l), file):
        parse_stack_spec_line(line.rstrip(), stack_dict)
    # print(stack_dict)
    return stack_dict


def parse_move_instructions(ix, line):
    # "move <count> from <ix_from> to <ix_to>"
    # print("move parse: ", line)
    m = re.match("move (?P<count>\\d+)+ from (?P<ix_from>\\d+)+ to (?P<ix_to>\\d+)+", line)
    count = int(m.group("count"))
    ix_from = int(m.group("ix_from"))-1  # 0-based
    ix_to = int(m.group("ix_to"))-1  # 0-based
    # print("count: ", count, ", from:", ix_from, ", to:", ix_to)
    return [ix, count, ix_from, ix_to]


def print_stacks(stack_dict):
    for ix, stack in stack_dict.items():
        print("{}:{}".format(ix, "".join(stack)))


def execute_move(move_spec: List, stack_dict: Dict):
    [ix, count, ix_from, ix_to] = move_spec
    from_stack = stack_dict[ix_from]
    to_stack = stack_dict[ix_to]
    target_count_from = len(from_stack) - count
    target_count_to = len(to_stack) + count
    # print("{}: executing move count:{} from {}({}) to {}".format(ix, count, ix_from, len(from_stack), ix_to))
    assert count <= len(from_stack)
#    to_stack = to_stack + list(reversed(from_stack[(-count):]))  # version for old cratemover 9000: move one-by-one
    to_stack = to_stack + list(from_stack[(-count):])  # version for cratemover 9001: dont reverse!
    from_stack = from_stack[:(-count)]
    stack_dict[ix_from] = from_stack
    stack_dict[ix_to] = to_stack
    assert len(from_stack) == target_count_from
    assert len(to_stack) == target_count_to


def main(file: List[str]):
    stack_dict = parse_stack_spec(file)
    # print("start:")
    # print_stacks(stack_dict)

    next(file)  # skip empty line between stack and move specs

    for ix, line in enumerate(file):
        move_spec = parse_move_instructions(ix, line.strip())
        execute_move(move_spec, stack_dict)
        # print_stacks(stack_dict)

    top_elems = [(stack_dict[ix].pop() if len(stack_dict[ix]) > 0 else '') for ix in range(0, len(stack_dict))]
    print("".join(top_elems))


if __name__ == '__main__':
    with open('05.txt') as f:
        main(f)
