from dataclasses import dataclass
from typing import List


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
    assert len(chunks) == 4
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


def silver(loc):
    wfs, parts = read(loc)
    sorter = Sorter(wfs)
    res = 0
    for part in parts:
        if sorter.sort(part):
            res += sum(value for value in part.values())
    return res


if __name__ == '__main__':
    print(silver("test.txt"))
    print(silver("input.txt"))
        
