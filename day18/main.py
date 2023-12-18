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
        return res


def solve(inp):
    len_perimeter = sum(steps for _, steps in inp)
    volume = 0
    x = 0
    y = 0
    for (dx, dy), steps in inp:
        xx = x + dx * steps
        yy = y + dy * steps
        volume += y * xx - x * yy
        x = xx
        y = yy
    volume = abs(volume // 2)
    return volume + len_perimeter // 2 + 1


if __name__ == '__main__':
    print(solve(read("test.txt")))
    print(solve(read("input.txt")))
    print(solve(read_gold("test.txt")))
    print(solve(read_gold("input.txt")))
