import heapq as pq

def read(loc):
    with open(loc) as f:
        rows = [line.strip() for line in f.readlines()]
        return [
            [int(c) for c in line] for line in rows
        ]


def solve(grid):
    N = (0,-1)
    E = (1,0)
    S = (0,1)
    W = (-1,0)


    heap = [(0, 0, 0, S, 0)]
    seen = set()
    pq.heapify(heap)

    while heap:
        cost, x, y, dir, steps = pq.heappop(heap)
        if y == len(grid) - 1 and x == len(grid[0]) - 1:
            return cost

        if dir in {N, S}:
            nxt = [(E, 1), (W, 1)]
        else:
            nxt = [(S, 1), (N, 1)]
        if steps < 3:
            nxt.append((dir, steps + 1))
        for next_dir, next_steps in nxt:
            dx, dy = next_dir
            xx = x + dx
            yy = y + dy
            if (xx, yy, next_dir, next_steps) in seen:
                continue
            if not(0 <= yy < len(grid)):
                continue
            if not(0 <= xx < len(grid[0])):
                continue
            seen.add((xx, yy, next_dir, next_steps))
            pq.heappush(heap, (cost + grid[yy][xx], xx, yy, next_dir, next_steps))


def ultrasolve(grid):
    N = (0,-1)
    E = (1,0)
    S = (0,1)
    W = (-1,0)


    heap = [(0, 0, 0, S, 0), (0, 0, 0, E, 0)]
    seen = set()
    pq.heapify(heap)

    while heap:
        cost, x, y, dir, steps = pq.heappop(heap)
        if y == len(grid) - 1 and x == len(grid[0]) - 1 and 4 <= steps:
            return cost

        nxt = []
        if steps < 10:
            nxt.append((dir, steps + 1))
        if 4 <= steps:
            if dir in {N, S}:
                nxt.extend([(E, 1), (W, 1)])
            else:
                nxt.extend([(S, 1), (N, 1)])

        for next_dir, next_steps in nxt:
            dx, dy = next_dir
            xx = x + dx
            yy = y + dy
            if (xx, yy, next_dir, next_steps) in seen:
                continue
            if not(0 <= yy < len(grid)):
                continue
            if not(0 <= xx < len(grid[0])):
                continue
            seen.add((xx, yy, next_dir, next_steps))
            pq.heappush(heap, (cost + grid[yy][xx], xx, yy, next_dir, next_steps))

def silver(loc):
    return solve(read(loc))

def gold(loc):
    return ultrasolve(read(loc))

if __name__ == '__main__':
    tests = [
        ([
            [1,2,3],
            [4,5,6],
            [7,8,9]
        ], 20),
        ([
            [1,9,1,1,1,9,1,1,1],
            [1,9,1,9,1,9,1,9,1],
            [1,1,1,9,1,1,1,9,1]
        ], 18),
        ([
            [1,1,1,1,1,1],
            [1,1,1,1,1,1]
        ], 6),
        (read("test.txt"), 102),
        ([        
            [1,9,9,9,9,9,9],
            [1,1,1,1,1,1,1],
            [9,9,9,1,9,9,1],
            [9,9,1,1,9,9,1],
            [9,9,1,1,9,9,1],
        ], 18)
        
    ]
    for grid, out in tests:
        res = solve(grid)
        if res != out:
            print(f"Wrong answer: Got {res} instead of {out} for {grid}.")

    print(silver("input.txt"))

    ultratests = [
        (read("test.txt"), 94),
        (read("test2.txt"), 71),
    ]
    
    for grid, out in ultratests:
        res = ultrasolve(grid)
        if res != out:
            print(f"Wrong answer: Got {res} instead of {out} for {grid}.")

    print(gold("input.txt"))
