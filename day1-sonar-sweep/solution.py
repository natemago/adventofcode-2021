from functools import reduce


def read_input(inpf):
    with open(inpf) as f:
        return [int(line.strip()) for line in f.readlines()]


def part1(depths):
    return reduce(lambda acc, curr: (curr, acc[1] + 1) if curr > acc[0] else (curr, acc[1]), depths, (depths[0], 0))[1]



def part2(depths):
    count = 0
    prev = sum(depths[0:3])
    for i in range(1, len(depths) - 2):
        curr = sum(depths[i: i+3])
        if curr > prev:
            count += 1
        prev = curr
    return count


print('Part 1: ', part1(read_input('input')))
print('Part 2: ', part2(read_input('input')))