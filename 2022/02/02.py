#!/usr/bin/python3

scoremap = {
    "A X": [3, 1],
    "A Y": [6, 2],
    "A Z": [0, 3],
    "B X": [0, 1],
    "B Y": [3, 2],
    "B Z": [6, 3],
    "C X": [6, 1],
    "C Y": [0, 2],
    "C Z": [3, 3],
}

outcomemap = {
    "A X": [0, 3],
    "A Y": [3, 1],
    "A Z": [6, 2],
    "B X": [0, 1],
    "B Y": [3, 2],
    "B Z": [6, 3],
    "C X": [0, 2],
    "C Y": [3, 3],
    "C Z": [6, 1],
}


def playgame(f, map):
    totalscore = 0
    for line in f:
        move = line.strip()
        outcome = map[move]
        score = sum(outcome)
        # print(move, ":", score)
        totalscore += score
    print("total:", totalscore)


with open('02.txt') as f:
    playgame(f, scoremap)
with open('02.txt') as f:
    playgame(f, outcomemap)
