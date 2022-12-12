#!/usr/bin/env python3
import copy
from typing import List, Set, Iterable, Type, Deque
import math
from dataclasses import dataclass
from collections import deque


@dataclass(frozen=True, slots=True)
class Point:
    x: int
    y: int

    @staticmethod
    def of_tuple(other: tuple[int, int]):
        return Point(other[0], other[1])

    @staticmethod
    def of_xy(x: int, y: int):
        return Point(x, y)

    def add(self, other: 'Point'):
        return Point(self.x + other.x, self.y + other.y)


# A queue node used in BFS
@dataclass(frozen=True, slots=True)
class Node:
    _coords: Point
    parent: 'Node' = None

    @property
    def x(self) -> int:
        return self._coords.x

    @property
    def y(self) -> int:
        return self._coords.y

    @property
    def key(self) -> Point:
        return self._coords

    def is_match(self, other: Point):
        return self._coords == other

    def add(self, other: Point):
        return Node(self._coords.add(other))


# Below lists detail all four possible movements from a cell
allowed_movements = [(1, 0), (-1, 0), (0, 1), (0, -1)]


# Utility function to find path from source to destination
def getPath(node, path=()):
    if node:
        path = getPath(node.parent, path)
        path.append(node)
    return path


# Find the shortest route in a matrix from source cell to destination cell
def findPath(matrix, start_pos: Point = Point(0, 0), end_pos: Point = Point(0, 0)):
    # base case
    if not matrix or not len(matrix):
        return

    # matrix size for bounds-checking
    N = Point(len(matrix[0]), len(matrix))

    # create a queue and enqueue the first node
    q: Deque[Node] = deque()
    src = Node(start_pos)
    q.append(src)

    # set to check if the matrix cell is visited before or not
    visited_coords = {src.key}

    # loop till queue is empty
    while q:

        # dequeue node and process it
        curr = q.popleft()
        # value of the current cell
        curr_height = matrix[curr.y][curr.x]
        # print("current node ({},{},{}), queuesize={}".format(curr.x, curr.y, curr_height, len(q)))
        # return if the destination is found
        # if curr.x == end[0] and curr.y == end[1]:
        if curr.is_match(end_pos):
            # print("REACHED END ({},{},{})".format(curr.x, curr.y, curr_height))
            path = []
            getPath(curr, path)
            return path

        # check all four possible movements from the current cell
        # and recur for each valid movement
        for allowed_movement in allowed_movements:
            # get next position coordinates using the value of the current cell
            candidate_coords = Point(curr.x + allowed_movement[0], curr.y + allowed_movement[1])

            # bounds-checking
            if not ((0 <= candidate_coords.x < N.x) and (0 <= candidate_coords.y < N.y)):
                continue
            # check if it is possible to go to the next position
            # from the current position
            next_height = matrix[candidate_coords.y][candidate_coords.x]
            # print("    checking node ({},{},{})".format(next_x, next_y, next_height))
            if next_height - curr_height > 1:
                continue
            if (candidate_coords in visited_coords):
                # print("    --> already seen")
                continue

            # enqueue it and mark it as visited
            # print("    --> found candidate ({},{},{})".format(next_x, next_y, next_height))
            q.append(Node(candidate_coords, curr))
            visited_coords.add(candidate_coords)

    # return None if the path is not possible
    return


def parse_heightmap(source: List[str]) -> tuple[List[List[int]], Point, Point]:
    matrix: List[List[int]] = []
    start_pos: Point = Point(-1, -1)
    end_pos: Point = Point(-1, -1)
    for line in source:
        if ('S' in line):
            start_pos = Point(line.index('S'), len(matrix))
            line = line.replace('S', 'a')
        if ('E' in line):
            end_pos = Point(line.index('E'), len(matrix))
            line = line.replace('E', 'z')

        heights_str = line.strip()
        print(heights_str)
        heights = [(ord(h) - ord('a')) for h in heights_str]
        matrix.append(heights)
    return matrix, start_pos, end_pos


def main(source: List[str], expected_result: str) -> None:
    (matrix, start_pos, end_pos) = parse_heightmap(source)

    print("found start at {}".format(start_pos))
    print("found end at {}".format(end_pos))
    all_start_positions: Set[Point] = {start_pos}
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if (matrix[y][x] == 0):
                all_start_positions.add(Point(x, y))

    results = []
    result1 = -1
    for start in all_start_positions:
        path = findPath(matrix, start, end_pos)
        if not path:
            continue
        result = len(path) - 1
        if (start == start_pos):
            result1 = result
        results.append((start, len(path) - 1))

    result2 = min([start[1] for start in results])

    (expected_result1, expected_result2) = expected_result.split(":")
    print("result1: {}, expected1:{}".format(result1, expected_result1))
    assert result1 == int(expected_result1)
    print("result2: {}, expected2:{}".format(result2, expected_result2))
    assert result2 == int(expected_result2)


if __name__ == '__main__':
    # test()
    with open('12-test.txt') as f:
        expected = f.readline()
        main(f.readlines(), expected)
    with open('12-data.txt') as f:
        expected = f.readline()
        main(f.readlines(), expected)
