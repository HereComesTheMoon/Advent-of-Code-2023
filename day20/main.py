import math
from collections import deque



# class Flipflop:
#     def __init__(self, name, out):
#         self.name = name
#         self.on = False
#         self.out = out

#     def pulse(self, inp):
#         if inp:
#             return
#         self.on = not self.on
#         for module in self.out:
#             yield (module, self.on)


# class Conjunction:
#     def __init__(self, name, out):
#         self.name = name
#         self.out = out
#         self.inputs = {}

#     def pulse(self, inp):
#         for module in self.out:
#             yield (module, inp)


# class Broadcaster:
#     def __init__(self, name, out):
#         self.name = name
#         self.out = out

#     def pulse(self, inp):
#         for module in self.out:
#             yield (module, inp)


def read(loc):
    res = {}
    with open(loc) as f:
        for line in f:
            line.strip()
            [name, rest] = line.split(" ", 1)
            out = [out.strip() for out in rest[2:].split(",")]
            if name == "broadcaster":
                res[name] = (out,)
                # res[name] = Broadcaster(name, out)
            elif name[0] == '%':
                res[name[1:]] = ('%', out, False)
                # res[name] = Flipflip(name, out)
            elif name[0] == '&':
                res[name[1:]] = ('&', out, {})
                # conj[name] = Conjunction(name, out)
            else:
                print(name)
                assert False
    outputs = []
    for name, module in res.items():
        match module:
            case (out,) | (_, out, _):
                for child in out:
                    if child not in res:
                        outputs.append(child)
    for output in outputs:
        res[output] = ([],)

    for name, module in res.items():
        match module:
            case (out,) | (_, out, _):
                for child in out:
                    if res[child][0] == '&':
                        res[child][2][name] = False
                        
        # match res[name]:
        #     case ('&', _, inputs):
        #         inputs[name] = False
        #     case _:
        #         pass
    return res
            

def button(modules):
    pulses = deque([("button", "broadcaster", False)])
    count_low = 0
    count_high = 0
    k = 0
    while pulses:
        source, sink, high = pulses.popleft()
        k += 1
        # print(k, sink, high)
        if high:
            count_high += 1
        else:
            count_low += 1
        if sink == 'rx':
            return (0, 0)
          # continue
        match modules[sink]:
            case (out,): # broadcaster
                pulses.extend(((sink, x, False) for x in out))
            case ('%', out, on):
                if high:
                    continue
                modules[sink] = ('%', out, not on)
                pulses.extend(((sink, x, not on) for x in out))
            case ('&', out, inputs):
                assert source in inputs
                inputs[source] = high
                # print("HERE", inputs)
                if all(inputs.values()):
                    pulses.extend(((sink, x, False) for x in out))
                else:
                    pulses.extend(((sink, x, True) for x in out))
    return (count_low, count_high)
                    


def cycle_length(modules, name):
    pulses = deque([])
    k = 0
    while True:
        if not pulses:
            k += 1
            pulses.append(("button", "broadcaster", False))
        source, sink, high = pulses.popleft()
        if sink == name and not high:
            return k
        match modules[sink]:
            case (out,): # broadcaster
                pulses.extend(((sink, x, False) for x in out))
            case ('%', out, on):
                if high:
                    continue
                modules[sink] = ('%', out, not on)
                pulses.extend(((sink, x, not on) for x in out))
            case ('&', out, inputs):
                # assert source in inputs
                inputs[source] = high
                if all(inputs.values()):
                    pulses.extend(((sink, x, False) for x in out))
                else:
                    pulses.extend(((sink, x, True) for x in out))
    return None
                    


def silver(loc):
    modules = read(loc)

    count_low = 0
    count_high = 0
    for x in range(1000):
        low, high = button(modules)
        count_low += low
        count_high += high

    print(f"{count_low=}, {count_high=}, {count_high*count_low=}")

    # print(modules)

def gold(loc):
    # modules = read(loc)

    # cycles = 
    # for x in cycles:
        # print(x, cycle_length(modules, x))
    cycles = [cycle_length(read(loc), name) for name in ["fv", "kk", "vt", "xr"]]
    print(cycles)
    print(math.lcm(*cycles))

    # print("Solution: ", k)
    return 0


if __name__ == '__main__':
    # print(silver("test1.txt"))
    # print(silver("test2.txt"))
    # print(silver("input.txt"))
    print(gold("input.txt"))



    
