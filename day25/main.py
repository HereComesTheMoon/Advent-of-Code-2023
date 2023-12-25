import networkx as nx


def read(loc):
    res = {}
    with open(loc) as f:
        for line in f:
            [v, edges] = line.strip().split(": ")
            res[v] = edges.split(" ")
    return res
     

def solve(loc):
    data = read(loc)
    g = nx.Graph(data)
    (_, (a, b)) = nx.stoer_wagner(g)
    return len(a) * len(b)

if __name__ == '__main__':
    print(solve("test.txt"))
    print(solve("input.txt"))
