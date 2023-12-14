def read(loc):
    with open(loc) as f:
        chunks = f.read().split("\n\n")

        chunks = [ chunk.strip().split("\n") for chunk in chunks ]

        return chunks

def transpose(pattern):
    a = [
        "" for _ in range(len(pattern[0]))
    ]
    for y in range(len(pattern)):
        for x in range(len(pattern[y])):
            a[x] += pattern[y][x]
    return a


def check(pattern, i):
    m = min(i, len(pattern) - i)
    for k in range(m):
        if pattern[i-1-k] != pattern[i+k]:
            return False
        # else:
            # print(f"{pattern[i-1-k]} != {pattern[i+k]}")
    return True


def check2(pattern, i):
    m = min(i, len(pattern) - i)
    res = 0
    for k in range(m):
        res += sum(x != y for x, y in zip(pattern[i-1-k], pattern[i+k]))
        if 1 < res:
            return False
        # else:
            # print(f"{pattern[i-1-k]} != {pattern[i+k]}")
    return res == 1


def find_reflection(pattern):
    for i in range(1, len(pattern)):
        if check(pattern, i):
            # print(i)
            # for x in pattern:
            #     print(x)
            return i
    else:
        return None


def find_reflection2(pattern):
    for i in range(1, len(pattern)):
        if check2(pattern, i):
            # print(i)
            # for x in pattern:
            #     print(x)
            return i
    else:
        return None

    
def silver(loc):
    chunks = read(loc)
    res = 0
    for pattern in chunks:
        val = find_reflection(pattern)
        val2 = find_reflection(transpose(pattern))

        if val is not None:
            res += 100 * val
        if val2 is not None:
            res += val2
        if val is None and val2 is None:
            print()
            for x in pattern:
                print(x)
        
    return res

def gold(loc):
    chunks = read(loc)
    res = 0
    for pattern in chunks:
        val = find_reflection2(pattern)
        val2 = find_reflection2(transpose(pattern))

        if val is not None:
            res += 100 * val
        if val2 is not None:
            res += val2
        if val is None and val2 is None:
            print()
            for x in pattern:
                print(x)
        
    return res

if __name__ == '__main__':
    print(silver("test.txt"))
    print(silver("input.txt"))
    print(gold("test.txt"))
    print(gold("input.txt"))
    # chunks = read("test.txt")
    # for chunk in chunks:
    #     a = transpose(chunk)
    #     print(chunk)
    #     print(a)
    #     assert chunk == transpose(a)
    # not 23572, too low
