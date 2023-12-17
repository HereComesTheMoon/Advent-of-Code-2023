import sys
from enum import Enum

def read(loc):
    with open(loc) as f:
        return [line.strip() for line in f.readlines()]

class Dir(Enum):
    N = 0
    E = 1
    S = 2
    W = 3

def rec(cave, seen, x, y, dir):
    if y not in range(len(cave)) or x not in range(len(cave[0])):
        return
    if (x, y, dir) in seen:
        return
    seen.add((x, y, dir))
    match cave[y][x], dir:
        case '/', Dir.N:
            rec(cave, seen, x + 1, y, Dir.E)
        case '/', Dir.E:
            rec(cave, seen, x, y - 1, Dir.N)
        case '/', Dir.S:
            rec(cave, seen, x - 1, y, Dir.W)
        case '/', Dir.W:
            rec(cave, seen, x, y + 1, Dir.S)
        case '\\', Dir.S:
            rec(cave, seen, x + 1, y, Dir.E)
        case '\\', Dir.W:
            rec(cave, seen, x, y - 1, Dir.N)
        case '\\', Dir.N:
            rec(cave, seen, x - 1, y, Dir.W)
        case '\\', Dir.E:
            rec(cave, seen, x, y + 1, Dir.S)
        case '-', Dir.N | Dir.S:
            rec(cave, seen, x + 1, y, Dir.E)
            rec(cave, seen, x - 1, y, Dir.W)
        case '|', Dir.E | Dir.W:
            rec(cave, seen, x, y - 1, Dir.N)
            rec(cave, seen, x, y + 1, Dir.S)
        case _, Dir.N:
            rec(cave, seen, x, y - 1, dir)
        case _, Dir.E:
            rec(cave, seen, x + 1, y, dir)
        case _, Dir.S:
            rec(cave, seen, x, y + 1, dir)
        case _, Dir.W:
            rec(cave, seen, x - 1, y, dir)
        case _:
            print("???")


def solve(cave, x, y, dir):
    seen = set()
    rec(cave, seen, x, y, dir)
    seen = { (x, y) for (x, y, _) in seen }
    return len(seen)


def silver(loc):
    cave = read(loc)
    return solve(cave, 0, 0, Dir.E)


def gold(loc):
    cave = read(loc)
    res = 0
    for y in range(len(cave)):
        res = max(res, solve(cave, 0, y, Dir.E))
        res = max(res, solve(cave, len(cave[0]) - 1, y, Dir.W))
    for x in range(len(cave[0])):
        res = max(res, solve(cave, x, 0, Dir.S))
        res = max(res, solve(cave, x, len(cave) - 1, Dir.N))
    return res


def printer(cave, seen):
    seen = { (x, y) for (x, y, _) in seen }
    OKCYAN = '\033[96m'    
    ENDC = '\033[0m'    
    s = ""
    for y in range(len(cave)):
        for x in range(len(cave[0])):
            if (x, y) in seen:
                s += OKCYAN + cave[y][x] + ENDC
            else:
                s += cave[y][x]
        s += "\n"
    print(s)

if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    print(silver("test.txt"))
    print(silver("input.txt"))
    print(gold("test.txt"))
    print(gold("input.txt"))
