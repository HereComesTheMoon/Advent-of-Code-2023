from functools import cache


DIRS = {
    '^': (0, -1),
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0),
}

def read(loc):
    with open(loc) as f:
        return [line.strip() for line in f.readlines()]


def get_options(grid, x, y):
    if 0 < y and grid[y-1][x] not in {'#', 'v'}:
        yield (x, y-1)

    if y < len(grid) - 1 and grid[y+1][x] not in {'#', '^'}:
        yield (x, y+1)
        
    if grid[y][x-1] not in {'#', '>'}:
        yield (x - 1, y)

    if grid[y][x+1] not in {'#', '<'}:
        yield (x + 1, y)


@cache
def walk(grid, x, y):
    steps = 0
    prev = (-1, -1)
    while True:
        if y + 1 == len(grid):
            return steps
        steps += 1
        if grid[y][x] in DIRS:
            prev = (x, y)
            d = DIRS[grid[y][x]]
            x += d[0]
            y += d[1]
            continue
        options = [option for option in get_options(grid, x, y) if option != prev]
        prev = (x, y)
        if len(options) == 1:
            x, y = options.pop()
            continue
        assert { grid[yy][xx] for xx, yy in options } <= {'^', '>', 'v', '<'}
        assert len(options) == 2
        return steps + max(walk(grid, xx, yy) for xx, yy in options)


def silver(loc):
    grid = read(loc)
    return walk(tuple(grid), 1, 0)


def gold(loc):
    grid = read(loc)
    g = Graph(grid)
    g.test()
    return(g.dfs(g.start, set()))


class Graph:
    def __init__(self, grid):
        self.start = (1, 0)
        self.end = (len(grid[0]) - 2, len(grid) - 1)
        self.v = {}
        self.build(grid)

    def dfs(self, node, seen):
        if node == self.end:
            return 0
        seen.add(node)
        res = float('-inf')
        for adj in self.v[node].keys():
            if adj in seen:
                continue
            res = max(res, self.v[node][adj] + self.dfs(adj, seen))
        seen.discard(node)
        return res
            
        
    def test(self):
        for node, neighbours in self.v.items():
            for adj, steps in neighbours.items():
                assert self.v[adj][node] == steps

    def build(self, grid):
        seen = set()
        next = { self.start }
        while next:
            x, y = next.pop()
            seen.add((x, y))
            self.v[(x, y)] = {}
            for xx, yy in [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]:
                if not(0 <= yy < len(grid)):
                    continue
                if not(0 <= xx < len(grid[0])):
                    continue
                if grid[yy][xx] == '#':
                    continue
                steps, (xxx, yyy) = self.get_next(grid, xx, yy, (x, y))
                self.v[(x, y)][(xxx, yyy)] = steps
                if (xxx, yyy) not in seen:
                    next.add((xxx, yyy))


    def get_next(self, grid, x, y, prev):
        steps = 0
        while True:
            if (x, y) == self.end:
                return steps + 1, (x, y)
            if (x, y) == self.start:
                return steps + 1, (x, y)
            steps += 1
            options = []
            for xx, yy in [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]:
                if not(0 <= yy < len(grid)):
                    continue
                if not(0 <= xx < len(grid[0])):
                    continue
                if grid[yy][xx] == '#':
                    continue
                if (xx, yy) == prev:
                    continue
                options.append((xx, yy))
            prev = (x, y)
            assert options
            if len(options) == 1:
                x, y = options.pop()
                continue
            return steps, (x, y)

if __name__ == '__main__':
    print(silver("test.txt"))
    print(silver("input.txt"))

    print(gold("test.txt"))
    print(gold("test2.txt"))
    print(gold("input.txt"))
