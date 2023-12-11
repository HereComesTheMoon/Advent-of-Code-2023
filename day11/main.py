def read(loc: str):
    with open(loc) as f:
        map = [
            [x == "#" for x in row] for row in f
        ]
        empty_lines = [0]
        for k in range(1, len(map)):
            empty_lines.append(empty_lines[-1] + int(not any(map[k-1])))

        empty_columns = [0]
        for k in range(1, len(map[0])):
            empty_columns.append(empty_columns[-1] + int(not any(map[i][k-1] for i in range(len(map)))))

        galaxy = []
        for y in range(len(map)):
            for x in range(len(map[0])):
                if map[y][x]:
                    galaxy.append((y,x,empty_lines[y],empty_columns[x]))

        return galaxy

def expand(galaxy, factor):
    return [
        (y + rows*(factor - 1), x + cols*(factor - 1)) for (y,x,rows,cols) in galaxy
    ]

def get_distances(coords):
    dists = []
    for k, (y, x) in enumerate(coords):
        for (yy, xx) in coords[k+1:]:
            dists.append(abs(y - yy) + abs(x - xx))

    return dists

def silver(loc):
    galaxy = read(loc)
    coords = expand(galaxy, 2)
    dists = get_distances(coords)
    return sum(dists)


def gold(loc):
    galaxy = read(loc)
    coords = expand(galaxy, 1_000_000)
    dists = get_distances(coords)
    return sum(dists)



if __name__ == '__main__':
    print(silver("test.txt"))
    print(silver("input.txt"))
    print(gold("test.txt"))
    print(gold("input.txt"))
