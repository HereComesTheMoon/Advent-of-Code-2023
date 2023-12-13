import functools


def read(loc):
    with open(loc) as f:
        lines = [line.split() for line in f.readlines()]
        lines = [(spring, tuple(map(int, nums.split(",")))) for [spring, nums] in lines]
        return lines


@functools.cache
def combs(s, run, chunks):
    if not s:
        if not chunks and run == 0:
            return 1
        if len(chunks) == 1 and chunks[0] == run:
            return 1
        return 0
    if s[0] == '#':
        return combs(s[1:], run + 1, chunks)
    if not chunks:
        if run != 0:
            return 0
        return 1 if all(c != "#" for c in s) else 0
    if chunks[0] < run:
        return 0
    if chunks[0] == run:
        return combs(s[1:], 0, chunks[1:])
    if s[0] == '.':
        if run == 0:
            return combs(s[1:], 0, chunks)
        return 0
    if run == 0:
        return combs(s[1:], 1, chunks) + combs(s[1:], 0, chunks)
    return combs(s[1:], run + 1, chunks)


def silver(loc):
    res = 0
    for [s, chunks] in read(loc):
        res += combs(s, 0, chunks)
    return res


def gold(loc):
    res = 0
    for [s, chunks] in read(loc):
        s = "?".join([s,s,s,s,s])
        chunks = chunks*5
        res += combs(s, 0, chunks)
    return res


if __name__ == '__main__':
    print(silver("test.txt"))
    print(silver("input.txt"))
    print(gold("test.txt"))
    print(gold("input.txt"))

    
