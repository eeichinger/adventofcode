#!/usr/bin/env python3

from typing import List, Set, Dict, Iterable
import re
import numpy as np


def main(source: Iterable[str], expected_result: str) -> None:
    # customised: first line contains expected size for auto-verification:
    #   expected_size_part1:expected_size_part2
    (expected_res1, expected_res2) = [int(res) for res in expected_result.split(":")]
    result = 0

    data = [[int(num) for num in list(line.strip())] for line in source]
    matrix = np.array(data)
    print(matrix)
    (rows, cols) = matrix.shape
    scenic_scores = np.zeros_like(matrix)
    visible = cols * 2 + (rows - 2) * 2
    for row_num in range(1, rows - 1):
        for col_num in range(1, cols - 1):
            viz_matrix = matrix - matrix[row_num, col_num]
            left = np.flip(viz_matrix[row_num, ...][:col_num])
            right = viz_matrix[row_num, ...][col_num + 1:]
            up = np.flip(viz_matrix[..., col_num][:row_num])
            down = viz_matrix[..., col_num][row_num + 1:]
            if 0 > max(left) \
                or 0 > max(right) \
                or 0 > max(up) \
                or 0 > max(down):
                visible += 1
                # print("\n[{}, {}] is visible in\n{}\nleft:{}\nright:{}\nup:{}\ndown:{}".format(row_num, col_num,
                #                                                                                viz_matrix,
                #                                                                                left,
                #                                                                                right,
                #                                                                                up,
                #                                                                                down)
                #       )
            scenic_scores[row_num, col_num] = calc_scenic_score_total(left, right, up, down)

    result = visible
    print("result: {}, expected: {}".format(result, expected_res1))
    assert expected_res1 == result

    scenic_score = np.max(scenic_scores)
    print("scenic_score: {}, expected: {}".format(scenic_score, expected_res2))
    assert expected_res2 == scenic_score


def calc_scenic_score_total(left, right, up, down):
    ss_l = calc_scenic_score(left)
    ss_r = calc_scenic_score(right)
    ss_u = calc_scenic_score(up)
    ss_d = calc_scenic_score(down)
    ss = ss_l * ss_r * ss_u * ss_d
    # print("scenic scores: {}*{}*{}*{}={}".format(ss_l, ss_r, ss_u, ss_d, ss))
    return ss


def calc_scenic_score(treeline: np.ndarray):
    view_distances = ((treeline >= 0).nonzero())[0]
    ss = 1 + np.min(view_distances, initial=treeline.size-1)
    return ss


if __name__ == '__main__':
    # score = calc_scenic_score(np.array([-2, -2]))
    # assert score == 2
    # score = calc_scenic_score(np.array([-2, 0, -2]))
    # assert score == 2
    with open('08-test.txt') as f:
        expected = f.readline()
        main(f, expected)
    with open('08-data.txt') as f:
        expected = f.readline()
        main(f, expected)
