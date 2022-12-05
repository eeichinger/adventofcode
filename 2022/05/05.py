#!/usr/bin/python3

from typing import List, Set, Dict
import re


def take_while(condition, iterable):
    for item in iterable:
        if not condition(item):
            return
        yield item


def parse_stack_spec_line(line: str, stack_dict: dict):
    # pick chars at each 4th position
    crates = [line[ix + 1] for ix in range(0, len(line), 4)]
    for index, crate in enumerate(crates):
        # insert crate at bottom of stack indicated by its index (empty '' crates result in empty list!)
        stack_dict[index] = list(crate.strip()) + (stack_dict[index] if index in stack_dict else [])


def parse_stack_spec(file: List[str], stack_dict: Dict[int, List[str]]):
    for line in take_while(lambda l: '[' in l, file):
        parse_stack_spec_line(line.rstrip(), stack_dict)


def parse_move_instructions(ix, line):
    # parse moving instruction lines
    # "move <count> from <ix_from> to <ix_to>"
    m = re.match("move (?P<count>\\d+)+ from (?P<ix_from>\\d+)+ to (?P<ix_to>\\d+)+", line)
    # return 0-based indices
    return [ix, int(m.group("count")), int(m.group("ix_from")) - 1, int(m.group("ix_to")) - 1]


def debug_print_stacks(stack_dict):
    for ix, stack in stack_dict.items():
        print("{}:{}".format(ix, "".join(stack)))


def execute_move(move_spec: List, is_crater9001: bool, stack_dict: Dict):
    [ix, count, ix_from, ix_to] = move_spec
    from_stack = stack_dict[ix_from]
    to_stack = stack_dict[ix_to]
    # print("move {}: executing count:{} from {}({}) to {}".format(ix, count, ix_from, len(from_stack), ix_to))
    crates_to_move = from_stack[-count:]
    if not is_crater9001:
        crates_to_move.reverse()  # version for old cratemover 9000: move one-by-one results in reverse order
    stack_dict[ix_to] = to_stack + list(crates_to_move)
    stack_dict[ix_from] = from_stack[:-count]


def move_crates(move_instructions: List, is_crater9001: bool, stack_dict: Dict):
    for ix, line in move_instructions:
        move_spec = parse_move_instructions(ix, line.strip())
        execute_move(move_spec, is_crater9001, stack_dict)
        # print_stacks(stack_dict)


def main(file: List[str], is_crater9001: bool, expected_result: str):
    stack_dict = dict()
    parse_stack_spec(file, stack_dict)
    # debug_print_stacks(stack_dict)

    next(file)  # skip empty line between stack and move specs

    move_crates(enumerate(file), is_crater9001, stack_dict)

    top_elems = [(stack_dict[ix].pop() if len(stack_dict[ix]) > 0 else '') for ix in range(0, len(stack_dict))]
    result = "".join(top_elems)
    print(result)
    assert result == expected_result


if __name__ == '__main__':
    source = ['05.txt', 'RTGWZTHLD', 'STHGRZZFR']
    # source = ['05-test.txt', 'CMZ']
    with open(source[0]) as f:
        main(f, False, source[1])
    with open(source[0]) as f:
        main(f, True, source[2])
