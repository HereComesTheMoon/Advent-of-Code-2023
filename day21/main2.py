from itertools import product


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


def printer(grid, now, just_one=True):
    s = ""
    if just_one:
        yit, xit = range(len(grid)), range(len(grid[0]))
    else:
        yit, xit = range(-10, 20), range(-10, 15)

    for y in yit:
        for x in xit:
            if (x, y) in now:
                s += "\033[93mO\x1b[0m"
            elif grid[y % len(grid)][x % len(grid[0])]:
                s += "."
            else:
                s += "#\x1b[0m"
        s += "\n"
    print(s)

def step(grid, now):
    new = set()
    for (x, y) in now:
        for xx, yy in [(x+1,y), (x-1,y), (x, y+1), (x, y-1)]:
            if grid[yy % len(grid)][xx % len(grid[0])]:
                new.add((xx, yy))
    return new


def get_full_sector(grid, x, y):
    now = { (x+1, y),(x-1, y),(x, y+1),(x, y-1), }
    k = 1

    def trim(grid, now):
        return { (x, y) for x, y in now if 0 <= y < len(grid) and 0 <= x < len(grid[0]) }
       
    while True:
        next = step(grid, step(grid, now))
        k += 2
        # printer(grid, now)
        if trim(grid, next) == trim(grid, now):
            break
        now = next

    return k, len(trim(grid, next))
    
def gold(loc, steps):
    grid, (x, y) = read(loc)
    assert len(grid) == len(grid[0])

    period = len(grid)
    mod = steps % period

    steps_until, weight_full_sector = get_full_sector(grid, x, y)
    print(f"A full sector has {weight_full_sector} steps. It takes {steps_until} steps to fill a sector, starting from the center. All four corners are reached last, and at the same time!")

    now = {(x,y)}
    for k in range(mod):
        now = step(grid, now)
    fulls = [0, 1, 5, 13, 25]
    x = 1
    fulls.extend(x := x + 4*i for i in range(1, 10))
    print(fulls)
    for k in range(10):
        print(f"{k=}: After {k*period+mod=} steps, we have a total of {len(now)} steps.")
        print(f"Of these, {fulls[k] * weight_full_sector=} should be coming from full sectors, leaving a total of {len(now)-fulls[k]*weight_full_sector}.")
        for _ in range(period):
            now = step(grid, now)
    print("Width of the grid: ", n)

# Thank you Wolfram Alpha
def interpolate(x):
    return 14881 * x * x - 14821 * x + 3682


if __name__ == '__main__':
    print("SOLUTION:")
    vals = [3742, 33564, 93148, 182494, 301602]
    for k, val in enumerate(vals, 1):
        print(interpolate(k))
        assert interpolate(k) == val
    print(interpolate(((26501365 - 65) // 131) + 1))
    gold("input.txt", 26501365)

    print(26501365)
    print(26501365 % 131)
    print((26501365 - 65) // 131)


# Equation: After 131 steps we have one full sector, and four triangles reaching exactly into and touching for new centers
# We also have exactly four 



# .......
# ...x...
# ..xxx..
# .xxxxx.
# ..xxx..
# ...x...
# .......


# k=0: After k*period+mod=65 steps, we have a total of 3742 steps.
# Of these, fulls[k] * weight_full_sector=0 should be coming from full sectors, leaving a total of 3742.
# k=1: After k*period+mod=196 steps, we have a total of 33564 steps.
# Of these, fulls[k] * weight_full_sector=7407 should be coming from full sectors, leaving a total of 26157.
# k=2: After k*period+mod=327 steps, we have a total of 93148 steps.
# Of these, fulls[k] * weight_full_sector=37035 should be coming from full sectors, leaving a total of 56113.
# k=3: After k*period+mod=458 steps, we have a total of 182494 steps.



