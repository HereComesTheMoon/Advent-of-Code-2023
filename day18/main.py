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
                (dirkey[dir], int(count))
            )
        return res

def read_gold(loc):
    with open(loc) as f:
        data = [x.strip().split() for x in f.readlines()]
        res = []

        dirkey = {
            '0': R,
            '1': D,
            '2': L,
            '3': U,
        }

        for [_, _, color] in data:
            res.append(
                (dirkey[color[-2]], int(color[2:len(color)-2], 16))
            )
        print(res)
        return res


def get_sizes(inp):
    x, y = 0, 0
    maxx = 0
    minx = 0
    maxy = 0
    miny = 0
    for (dx, dy), steps in inp:
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
    for (dx, dy), steps in inp:
        for _ in range(steps):
            x += dx
            y += dy
            # print(f"{x=}, {y=}. {len(grid)=}, {len(grid[0])=}")
            grid[y][x] = True

    s = ""
    for row in grid:
        for x in row:
            s += "#" if x else "."
        s += "\n"
    print(s)
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

def slice(inp):
    (minx, maxx), (miny, maxy) = get_sizes(inp)
    x = - minx
    y = - miny
    xx = maxx - minx + 1
    yy = maxy - miny + 1
    nums = [[] for _ in range(yy)]
    for ((dx, dy), steps) in inp:
        # print((dx, dy), steps)
        if dy == 0:
            nums[y].append(tuple(sorted([x, x + dx * steps])))
            x += steps * dx
            continue
        for k in range(y + dy, y + dy * (steps), dy):
            nums[k].append((x,x))
        y += dy * steps
    return nums

def count_length_border(inp):
    return sum(steps for _, steps in inp)
        
def integrate(nums):
    res = 0
    for slice in nums:
        slice.sort()
        print(slice)
        while 2 <= len(slice):
            _, b = slice.pop()
            a, _ = slice.pop()
            print(f"{a=}, {b=}. Adding {b - a - 1}")
            res += b - a - 1
    return res
    

def silver(loc):
    inp = read(loc)
    grid = draw_board(inp)
    number_edges = count(grid)
    x, y = find_interior(grid)
    rec(grid, x, y)
    total = count(grid)
    print(f"{number_edges=}, {total=}")
    return total

def gold(inp):
    len_perimeter = count_length_border(inp)
    nums = slice(inp)
    volume = integrate(nums)
    print(f"{len_perimeter=}")
    print(f"{volume=}")
    return len_perimeter + volume
    

if __name__ == '__main__':
    # inp = read("input.txt")
    sys.setrecursionlimit(100000)
    # silver("test.txt")
    # silver("input.txt")

    draw_board(read("test3.txt"))
    print(gold(read("test3.txt")))
    # print(gold(read("test.txt")))
    # print(gold(read("test2.txt")))
    # print(gold(read("input.txt")))

    # inp = read("test.txt")
    # nums = slice(inp)
    # print(nums)
        

