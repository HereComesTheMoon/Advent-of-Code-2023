

def read(loc):
    with open(loc) as f:
        grid = [line.strip() for line in f.readlines()]
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val == 'S':
                startx = x
                starty = y
                grid[y] = row.replace('S', '.')
    grid = [
        [val == '.' for val in row] for row in grid
    ]
    return grid, (startx, starty)


def double_step(grid, x, y):
    if 2 <= x and grid[y][x-1] and grid[y][x-2]:
        yield (x-2, y)
    if x + 2 < len(grid[0]) and grid[y][x+1] and grid[y][x+2]:
        yield (x+2, y)
    if 2 <= y and grid[y-1][x] and grid[y-2][x]:
        yield (x, y-2)
    if y + 2 < len(grid) and grid[y+1][x] and grid[y+2][x]:
        yield (x, y+2)
    if y + 1 < len(grid) and x + 1 < len(grid[0]) and (grid[y][x+1] or grid[y+1][x]) and grid[y+1][x+1]:
        yield (x+1, y+1)
    if y + 1 < len(grid) and 1 <= x and (grid[y][x-1] or grid[y+1][x]) and grid[y+1][x-1]:
        yield (x-1, y+1)
    if 1 <= y and x + 1 < len(grid[0]) and (grid[y][x+1] or grid[y-1][x]) and grid[y-1][x+1]:
        yield (x+1, y-1)
    if 1 <= y and x + 1 < len(grid[0]) and (grid[y][x-1] or grid[y-1][x]) and grid[y-1][x-1]:
        yield (x-1, y-1)


def double_step_mod(grid, x, y):
    if grid[(y) % len(grid)][(x-1) % len(grid[0])] and grid[(y) % len(grid)][(x-2) % len(grid[0])]:
        yield (x-2, y)
    if grid[(y) % len(grid)][(x+1) % len(grid[0])] and grid[(y) % len(grid)][(x+2) % len(grid[0])]:
        yield (x+2, y)
    if grid[(y-1) % len(grid)][(x) % len(grid[0])] and grid[(y-2) % len(grid)][(x) % len(grid[0])]:
        yield (x, y-2)
    if grid[(y+1) % len(grid)][(x) % len(grid[0])] and grid[(y+2) % len(grid)][(x) % len(grid[0])]:
        yield (x, y+2)
    if (grid[(y) % len(grid)][(x+1) % len(grid[0])] or grid[(y+1) % len(grid)][(x) % len(grid[0])]) and grid[(y+1) % len(grid)][(x+1) % len(grid[0])]:
        yield (x+1, y+1)
    if (grid[(y) % len(grid)][(x-1) % len(grid[0])] or grid[(y+1) % len(grid)][(x) % len(grid[0])]) and grid[(y+1) % len(grid)][(x-1) % len(grid[0])]:
        yield (x-1, y+1)
    if (grid[(y) % len(grid)][(x+1) % len(grid[0])] or grid[(y-1) % len(grid)][(x) % len(grid[0])]) and grid[(y-1) % len(grid)][(x+1) % len(grid[0])]:
        yield (x+1, y-1)
    if (grid[(y) % len(grid)][(x-1) % len(grid[0])] or grid[(y-1) % len(grid)][(x) % len(grid[0])]) and grid[(y-1) % len(grid)][(x-1) % len(grid[0])]:
        yield (x-1, y-1)

def printer(grid, now):
    s = ""
    # for y in range(-10,20):
    for y, row in enumerate(grid):
        for x in range(-10, 15):
    # for y, row in enumerate(grid):
        # for x, val in enumerate(row):
            if (x, y) in now:
                s += "O"
            elif grid[y % len(grid)][x % len(grid[0])]:
                s += "."
            else:
                s += "#"
        s += "\n"
    print(s)
                

def silver(loc):
    grid, (x, y) = read(loc)
    now = { (x, y) }
    seen = set()
    for _ in range(32):
        next = set()
        for (xx, yy) in now:
            for (x, y) in step_wrapper(grid, xx, yy):
                if x < 0 or y < 0:
                    continue
                if (x, y) in now:
                    continue
                if (x, y) in seen:
                    continue
                next.add((x, y))
        seen |= now
        # print(now)
        now = next
        printer(grid, now)
    seen |= now
    return len(seen)


def diffs(seq):
    diff = [seq]
    while True:
        if not any(diff[-1]):
            return diff
        new = []
        for k in range(len(diff[-1]) - 1):
            new.append(diff[-1][k+1] - diff[-1][k])
        diff.append(new)
        

def extrapolate(diff):
    diff[-1].append(0)
    for k in reversed(range(len(diff) - 1)):
        diff[k].append(diff[k][-1] + diff[k+1][-1])
    return diff[0][-1]
        

def gold(loc):
    grid, (x, y) = read(loc)
    # now = { (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1) }
    # seen = { (x, y) }
    # for _ in range(26501364 // 2):
    now = { (x, y) }
    seen = set()
    res = []
    for k in range(500):
        print(k)
        next = set()
        for (xx, yy) in now:
            for (x, y) in double_step_mod(grid, xx, yy):
                if (x, y) in now:
                    continue
                if (x, y) in seen:
                    continue
                next.add((x, y))
        seen |= now
        now = next
        res.append(len(seen))
    seen |= now
    res.append(len(seen))
    return res[-50:]


if __name__ == '__main__':
    input = read(loc)

    # print(silver("input.txt"))
    # diffs = diffs(gold("test.txt"))
    # for row in diffs:
    #     print(row)
    # diffs = diffs([10, 13, 16, 21, 30, 45,])
    # print(extrapolate(diffs))
    # print(diffs)
