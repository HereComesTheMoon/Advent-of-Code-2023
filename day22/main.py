from dataclasses import dataclass
from itertools import chain
import copy
from collections import defaultdict


@dataclass
class Pt:
    x: int
    y: int
    z: int

class Brick:
    def __init__(self, p: Pt, q: Pt):
        self.low = p
        self.hi = q

    def intersect(self, other):
        x = self.low.x <= other.hi.x and other.low.x <= self.hi.x
        y = self.low.y <= other.hi.y and other.low.y <= self.hi.y
        z = self.low.z <= other.hi.z and other.low.z <= self.hi.z
        return x and y and z

    def check_if_supported_by(self, support):
        assert not self.intersect(support)
        assert self.low.z != 1
        lowered = Brick(
            Pt(self.low.x, self.low.y, self.low.z - 1),
            Pt(self.hi.x, self.hi.y, self.hi.z - 1),
        )
        return lowered.intersect(support)

    def __str__(self):
        s = f"({self.low} ~ {self.hi})"
        return s

    def __repr__(self):
        s = f"({self.low} ~ {self.hi})"
        return s


def read(loc):
    res = []
    with open(loc) as f:
        for line in f:
            [p, q] = line.strip().split('~', 1)
            p = [int(x) for x in p.split(',')]
            q = [int(x) for x in q.split(',')]
            for pp, qq in zip(p, q):
                assert pp <= qq
            res.append(Brick(Pt(*p), Pt(*q)))
    return res


def lower_all(bricks):
    bricks.sort(key=lambda brick: brick.hi.z)
    res = defaultdict(list)
    for brick in bricks:
        while True:
            if brick.low.z == 1:
                break
            if any(brick.check_if_supported_by(other) for other in res[brick.low.z - 1]):
                break
            brick.low.z -= 1
            brick.hi.z -= 1
        res[brick.hi.z].append(brick)
    res = { level: bricks for level, bricks in res.items() }
    res[0] = []
    return res


def lower_count(bricks):
    bricks.sort(key=lambda brick: brick.hi.z)
    levels = defaultdict(list)
    counter = 0
    for brick in bricks:
        if brick.low.z == 1 or any(brick.check_if_supported_by(other) for other in levels[brick.low.z - 1]):
                pass
        else:
            counter += 1
            while True:
                brick.low.z -= 1
                brick.hi.z -= 1
                if brick.low.z == 1:
                    break
                if any(brick.check_if_supported_by(other) for other in levels[brick.low.z - 1]):
                    break
        levels[brick.hi.z].append(brick)
    return counter


def silver(loc):
    bricks = read(loc)
    bricks.sort(key=lambda brick: brick.low.z)
    levels = lower_all(bricks)
    res = set()
    for level in levels.values():
        for brick in level:
            supporters = [other for other in levels[brick.low.z - 1] if brick.check_if_supported_by(other)]
            if len(supporters) == 1:
                res.add(supporters[0])
    return sum(len(level) for level in levels.values()) - len(res)


def gold(loc):
    bricks = read(loc)
    bricks.sort(key=lambda brick: brick.low.z)
    levels = lower_all(bricks)
    bricks = list(chain(*levels.values()))

    res = 0
    for k in range(len(bricks)):
        new_bricks = copy.deepcopy(bricks[:k] + bricks[k+1:])
        a = lower_count(new_bricks)
        res += a
    return res


if __name__ == '__main__':
    print(silver("test.txt"))
    print(gold("test.txt"))
    print(silver("input.txt"))
    print(gold("input.txt"))
    
           
