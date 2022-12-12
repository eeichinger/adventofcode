#!/usr/bin/env python3
import copy
from typing import List, Set, Iterable
import math

from collections import deque


# A queue node used in BFS
class Node:
    # (x, y) represents coordinates of a cell in the matrix
    # maintain a parent node for the printing path
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent

    def __repr__(self):
        return str((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


# Below lists detail all four possible movements from a cell
allowed_movements = [(1, 0), (-1, 0), (0, 1), (0, -1)]


# Utility function to find path from source to destination
def getPath(node, path=[]):
    if node:
        getPath(node.parent, path)
        path.append(node)


# Find the shortest route in a matrix from source cell to destination cell
def findPath(matrix, start_x=0, start_y=0, end_x=0, end_y=0):
    # base case
    if not matrix or not len(matrix):
        return

    # matrix size for bounds-checking
    N_x = len(matrix[0])
    N_y = len(matrix)

    # create a queue and enqueue the first node
    q = deque()
    src = Node(start_x, start_y)
    q.append(src)

    # set to check if the matrix cell is visited before or not
    visited = set()

    next_key = (src.x, src.y)
    visited.add(next_key)

    # loop till queue is empty
    while q:

        # dequeue node and process it
        curr = q.popleft()
        # value of the current cell
        curr_height = matrix[curr.y][curr.x]
        # print("current node ({},{},{}), queuesize={}".format(curr.x, curr.y, curr_height, len(q)))
        # return if the destination is found
        if curr.x == end_x and curr.y == end_y:
            # print("REACHED END ({},{},{})".format(curr.x, curr.y, curr_height))
            path = []
            getPath(curr, path)
            return path

        # check all four possible movements from the current cell
        # and recur for each valid movement
        for allowed_movement in allowed_movements:
            # get next position coordinates using the value of the current cell
            next_x = curr.x + allowed_movement[0]
            next_y = curr.y + allowed_movement[1]

            # bounds-checking
            if not ((0 <= next_x < N_x) and (0 <= next_y < N_y)):
                continue
            # check if it is possible to go to the next position
            # from the current position
            next_height = matrix[next_y][next_x]
            next_key = (next_x, next_y)
            # print("    checking node ({},{},{})".format(next_x, next_y, next_height))
            if next_height - curr_height > 1:
                continue
            if (next_key in visited):
                # print("    --> already seen")
                continue

            # construct the next cell node
            next = Node(next_x, next_y, curr)
            # enqueue it and mark it as visited
            # print("    --> found candidate ({},{},{})".format(next_x, next_y, next_height))
            q.append(next)
            visited.add(next_key)

    # return None if the path is not possible
    return


heights_index = "abcdefghijklmnopqrstuvwxyz"


def main(source: List[str], expected_result: str) -> None:
    matrix: List[List[int]] = []
    start_x = -1
    start_y = -1
    end_x = -1
    end_y = -1
    for line in source:
        if ('S' in line):
            start_x = line.index('S')
            start_y = len(matrix)
            line = line.replace('S', 'a')
        if ('E' in line):
            end_x = line.index('E')
            end_y = len(matrix)
            line = line.replace('E', 'z')

        heights_str = line.strip()
        print(heights_str)
        heights = [heights_index.index(h) for h in heights_str]
        matrix.append(heights)

    print("found start at ({}, {})".format(start_x, start_y))
    print("found end at ({}, {})".format(end_x, end_y))
    all_start_positions = {(start_x, start_y)}
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if (matrix[y][x] == 0):
                all_start_positions.add((x, y))

    results = []
    result1 = -1
    for start_pos in all_start_positions:
        path = findPath(matrix, start_pos[0], start_pos[1], end_x, end_y)
        if not path:
            continue
        result = len(path) - 1
        if (start_pos == (start_x, start_y)):
            result1 = result
        results.append((start_pos, len(path) - 1))

    result2 = min([start_pos[1] for start_pos in results])

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
