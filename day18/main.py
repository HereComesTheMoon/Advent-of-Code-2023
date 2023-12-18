import sys


R = (1,0)
D = (0,1)
L = (-1, 0)
U = (0, -1)

def read(loc):
    with open(loc) as f:
        data = [x.strip().split() for x in f.readlines()]
        res = []

        dirkey = {
            'R': R,
            'D': D,
            'L': L,
            'U': U,
        }

        for [dir, count, color] in data:
            res.append(
                (dirkey[dir], int(count), int(color[2:len(color)-1], 16))
            )
        return res


def get_sizes(inp):
    x, y = 0, 0
    maxx = 0
    minx = 0
    maxy = 0
    miny = 0
    for (dx, dy), steps, _ in inp:
        x += steps * dx
        y += steps * dy
        maxx = max(maxx, x)
        minx = min(minx, x)
        maxy = max(maxy, y)
        miny = min(miny, y)
    # print(f"{maxx=}")
    # print(f"{minx=}")
    # print(f"{maxy=}")
    # print(f"{miny=}")
    return ((minx, maxx), (miny, maxy))

def draw_board(inp):
    (minx, maxx), (miny, maxy) = get_sizes(inp)
    x = - minx
    y = - miny
    xx = maxx - minx + 1
    yy = maxy - miny + 1
    grid = [ [False] * xx for _ in range(yy) ]
    grid[y][x] = True
    for (dx, dy), steps, _ in inp:
        for _ in range(steps):
            x += dx
            y += dy
            # print(f"{x=}, {y=}. {len(grid)=}, {len(grid[0])=}")
            grid[y][x] = True

    # s = ""
    # for row in grid:
    #     for x in row:
    #         s += "#" if x else "."
    #     s += "\n"
    return grid

def find_interior(grid):
    for y in range(1, len(grid) - 1):
        x = grid[y].index(True)
        if grid[y][x+1]:
            continue
        return x + 1, y

def rec(grid, x, y):
    grid[y][x] = True
    for dx, dy in [R, D, L, U]:
        if grid[y + dy][x + dx]:
            continue
        rec(grid, x + dx, y + dy)

def count(grid):
    return sum(sum(row) for row in grid)

def silver(loc):
    inp = read(loc)
    grid = draw_board(inp)
    number_edges = count(grid)
    x, y = find_interior(grid)
    rec(grid, x, y)
    total = count(grid)
    print(f"{number_edges=}, {total=}")
    return total


if __name__ == '__main__':
    # inp = read("input.txt")
    sys.setrecursionlimit(100000)
    silver("test.txt")
    silver("input.txt")
        

