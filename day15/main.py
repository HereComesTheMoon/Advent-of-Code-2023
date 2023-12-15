def read(loc):
    with open(loc) as f:
        return f.read().strip().split(',')


def read_gold(loc):
    data = read(loc)
    res = []
    for s in data:
        if '=' in s:
            res.append(s.split('='))
        else:
            res.append([s[:len(s)-1]])
    return res


def hash(s):
    res = 0
    for c in s:
        res = ((res + ord(c)) * 17) % 256
    return res


def focusing_power(boxes):
    res = 0
    for k, box in enumerate(boxes, 1):
        for i, (label, focal_power) in enumerate(box.items(), 1):
            # print(f"{k} * {i} * {focal_power} = {k * i * int(focal_power)}")
            res += k * i * int(focal_power)
    return res


def silver(loc):
    return sum(hash(seq) for seq in read(loc))


def gold(loc):
    seqs = read_gold(loc)
    boxes = [ {} for _ in range(256) ]
    for seq in seqs:
        if len(seq) == 2:
            boxes[hash(seq[0])][seq[0]] = seq[1]
        else:
            boxes[hash(seq[0])].pop(seq[0], None)
    return focusing_power(boxes)


if __name__ == '__main__':
    print(silver("test.txt"))
    print(silver("input.txt"))
    print(gold("test.txt"))
    print(gold("input.txt"))
