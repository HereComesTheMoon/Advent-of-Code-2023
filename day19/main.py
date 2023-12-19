from dataclasses import dataclass
from typing import List
import copy


@dataclass
class Step:
    field: str
    op: str
    value: int
    goal: str

    def check(self, part):
        match self.op:
            case '<':
                return part[self.field] < self.value
            case '>':
                return part[self.field] > self.value

    def split(self, part):
        a, b = part[self.field]
        res = []
        match self.op:
            case '<' if b < self.value:
                res.append((self.goal, part))
            case '<' if self.value <= a:
                res.append((None, part))
            case '>' if a > self.value:
                res.append((self.goal, part))
            case '>' if self.value >= b:
                res.append((None, part))
            case '<':
                c = self.value
                aa = copy.copy(part)
                aa[self.field] = (a, c)
                res.append((self.goal, aa))
                bb = copy.copy(part)
                bb[self.field] = (c, b)
                res.append((None, bb))
            case '>':
                c = self.value
                aa = copy.copy(part)
                aa[self.field] = (a, c + 1)
                res.append((None, aa))
                bb = copy.copy(part)
                bb[self.field] = (c + 1, b)
                res.append((self.goal, bb))
            case _:
                print("what?")
        return res


@dataclass
class Workflow:
    name: str
    steps: list[Step]
    last: str

    def sort(self, part):
        for step in self.steps:
            if step.check(part):
                return step.goal
        return self.last

    def split(self, part):
        done = []
        parts = [part]
        for step in self.steps:
            doing = []
            while parts:
                part = parts.pop()
                doing.extend(step.split(part))
            for next, part in doing:
                if next is None:
                    parts.append(part)
                else:
                    done.append((next, part))
        for part in parts:
            done.append((self.last, part))
        return done


def read(loc):
    with open(loc) as f:
        workflows = []
        for line in f:
            line = line.rstrip()
            if not line:
                break
            workflows.append(parse_workflow(line))

        parts = []
        for line in f:
            line = line.rstrip()
            parts.append(parse_part(line))
        return workflows, parts


def parse_workflow(line):
    i = line.index("{")
    name = line[:i]
    chunks = line[i+1:len(line)-1].split(",")
    last = chunks.pop()
    steps = []
    for chunk in chunks:
        chunk = chunk.split(":")
        goal = chunk.pop()
        chunk = chunk.pop()
        field = chunk[0]
        op = chunk[1]
        value = int(chunk[2:])
        steps.append(Step(field, op, value, goal))
    return Workflow(name, steps, last)

        
def parse_part(line):
    chunks = line[1:len(line)-1].split(",")
    d = {}
    for chunk in chunks:
        d[chunk[0]] = int(chunk[2:])
    return d


class Sorter:
    def __init__(self, workflows: List[Workflow]):
        self.wfs = {
            wf.name: wf for wf in workflows
        }

    def sort(self, part) -> bool:
        now = 'in'
        next = self.wfs[now].sort(part)
        while next not in { 'A', 'R' }:
            now = next
            next = self.wfs[now].sort(part)
        return next == 'A'

    def rec(self, part, wf):
        parts = self.wfs[wf].split(part)
        res = 0
        for wf, part in parts:
            if any(b <= a for a, b in part.values()):
                return 0
            if wf == 'A':
                val = 1
                for (a, b) in part.values():
                    val *= (b - a)
                res += val
                continue
            if wf == 'R':
                continue
            res += self.rec(part, wf)
        return res
        

def silver(loc):
    wfs, parts = read(loc)
    sorter = Sorter(wfs)
    res = 0
    for part in parts:
        if sorter.sort(part):
            res += sum(value for value in part.values())
    return res


def gold(loc):
    wfs, _ = read(loc)
    start = {
        'x': (1, 4001),
        'm': (1, 4001),
        'a': (1, 4001),
        's': (1, 4001)
    }
    sorter = Sorter(wfs)
    return sorter.rec(start, "in")


if __name__ == '__main__':
    print(silver("test.txt"))
    print(silver("input.txt"))
    print(gold("test.txt"))
    print(gold("input.txt"))
