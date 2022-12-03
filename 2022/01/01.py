#!/usr/bin/python3

def striplines(it):
    for line in f:
        yield line.strip()


def partialsums(it):
    summ = 0
    for line in it:
        if not line:
            yield summ
            summ = 0
        else:
            summ += int(line)
    yield summ


with open('01.txt') as f:
    cleanedlines = [l for l in striplines(f)]
    caloriesperelve = [n for n in partialsums(cleanedlines)]
    print(max(caloriesperelve))
    sortedcaloriesperelve = sorted(caloriesperelve, reverse=True)
    top3 = sortedcaloriesperelve[:3]
    print(sum(top3))