import copy

def read(loc):
    with open(loc) as f:
        return [list(row.strip()) for row in f.readlines()]


def next(grid, x, y, dx, dy):
    ax, ay = x, y
    while True:
        while 0 <= ay < len(grid) and 0 <= ax < len(grid[ay]) and grid[ay][ax] != '.':
            ax += dx
            ay += dy
        bx, by = ax, ay
        while 0 <= by < len(grid) and 0 <= bx < len(grid[by]) and grid[by][bx] == '.':
            bx += dx
            by += dy
        if not(0 <= by < len(grid) and 0 <= bx < len(grid[by])):
            break
        if grid[by][bx] == '#':
            ax = bx
            ay = by
        else: # == 'O'
            yield ((ax, ay), (bx, by))
            
    return None


def cycle(grid):
    for (ax, ay), (bx, by) in cycle_iter(grid):
        grid[ay][ax] = grid[by][bx]
        grid[by][bx] = '.'
    
def cycle_iter(grid):
    for x in range(len(grid[0])):
        yield from next(grid, x, 0, 0, 1)

    for y in range(len(grid)):
        yield from next(grid, 0, y, 1, 0)

    for x in range(len(grid[0])):
        yield from next(grid, x, len(grid) - 1, 0, -1)

    for y in range(len(grid)):
        yield from next(grid, len(grid[0]) - 1, y, -1, 0)

def grid_to_str(grid):
    return "\n".join("".join(row) for row in grid)

def find_start_of_cycle(grid):
    seen = set()
    count = 0
    seen.add(grid_to_str(grid))
    while True:
        count += 1
        for (ax, ay), (bx, by) in cycle_iter(grid):
            grid[ay][ax] = grid[by][bx]
            grid[by][bx] = '.'
        next = grid_to_str(grid)
        if next in seen:
            return count
        else:
            seen.add(next)

def find_period(grid):
    start = copy.deepcopy(grid)
    count = 1
    cycle(grid)
    while grid != start:
        cycle(grid)
        count += 1
    return count

def compute_load(grid):
    res = 0
    for k, row in enumerate(grid):
        res += (len(grid) - k) * sum(x == 'O' for x in row)
    return res


def silver(loc):
    grid = read(loc)
    for x in range(len(grid[0])):
        for (ax, ay), (bx, by) in next(grid, x, 0, 0, 1):
            grid[ay][ax] = grid[by][bx]
            grid[by][bx] = '.'

    return compute_load(grid)

def gold(loc):
    grid = read(loc)

    offset = find_start_of_cycle(grid)
    period = find_period(grid)

    print(f"{offset=}, {period=}")
    total_cycles = 1_000_000_000
    mod_cycles = (total_cycles - offset) % period
    for _ in range(mod_cycles):
        cycle(grid)
    
    return compute_load(grid)


if __name__ == '__main__':
    print(silver("test.txt"))
    print(silver("input.txt"))
    print(gold("test.txt"))
    print(gold("input.txt"))
