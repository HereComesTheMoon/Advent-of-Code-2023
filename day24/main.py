import sympy as sp
import itertools


def read(loc):
    res = []
    with open(loc) as f:
        for line in f:
            [pos, vel] = line.split('@')
            res.append(
                (
                    (tuple(map(int, pos.split(',')))),
                    (tuple(map(int, vel.split(',')))),
                )
            )

    return res


def silver(loc, low, high):
    return sum(
        map(lambda _: 1,
            filter(lambda val: low <= val[0][0] <= high and low <= val[0][1] <= high,
                filter(lambda res: bool(res),
                    (
                        sp.intersection(
                            sp.Ray((px, py), (px + pdx, py + pdy)),
                            sp.Ray((qx, qy), (qx + qdx, qy + qdy))
                        ) for (
                            ((px, py, _), (pdx, pdy, _)),
                            ((qx, qy, _), (qdx, qdy, _))
                        ) in itertools.combinations(read(loc), 2)
                    )
                )
            )
        )
    )


def gold(loc):
    x0, y0, z0, dx0, dy0, dz0 = sp.symbols('x0, y0, z0, dx0, dy0, dz0')
    eqs = []
    symbols = []
    tt = sp.numbered_symbols('t')
    for (px, py, pz), (pdx, pdy, pdz) in read(loc)[:3]:
        t = tt.__next__()
        symbols.append(t)
        eqs.append(
            px + t * pdx - (x0 + t * dx0)
        )
        eqs.append(
            py + t * pdy - (y0 + t * dy0)
        )
        eqs.append(
            pz + t * pdz - (z0 + t * dz0)
        )
    return sum(sp.solve(eqs, x0, y0, z0, dx0, dy0, dz0, *symbols)[0][:3])


if __name__ == '__main__':
    print(silver("test.txt", 7, 27))
    print(silver("input.txt", 200000000000000, 400000000000000))
    print(gold("test.txt"))
    print(gold("input.txt"))

