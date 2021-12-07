from functools import reduce
def read_input(inpf):
    with open(inpf) as f:
        return [int(p.strip()) for p in f.readline().strip().split(',')]

def cost(positions, x):
    return reduce(lambda a, p: a + abs(p - x), positions, 0)

def cost_cumulative(positions, x):
    return reduce(lambda a, p: a + abs(p - x)*(abs(p - x) + 1)//2, positions, 0)

def part1(positions):
    s = min(positions)
    e = max(positions)
    return min([cost(positions, p) for p in range(s, e+1)])


def part2(positions):
    s = min(positions)
    e = max(positions)
    return min([cost_cumulative(positions, p) for p in range(s, e+1)])

print('Part 1: ', part1(read_input('input')))
print('Part 2: ', part2(read_input('input')))

def part1_m(positions):
    pos = sorted(positions)[len(positions)//2] # median
    return cost(positions, pos)


def part2_m(positions):
    p = sum([2*a + 1 for a in positions])//(2*len(positions)) - 1  # min of the cost function
    return cost_cumulative(positions, p)


print('Part 1 (maths): ', part1_m(read_input('input')))
print('Part 2 (maths): ', part2_m(read_input('input')))

