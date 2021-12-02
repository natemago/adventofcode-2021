def read_input(inpf):
    with open(inpf) as f:
        return list(map(
            lambda line: (line.strip().split()[0], int(line.strip().split()[1])), 
            f.readlines()))

def part1(instructions):
    x = 0
    y = 0
    for instr, value in instructions:
        if instr == 'up':
            y -= value
        elif instr == 'down':
            y += value
        elif instr == 'forward':
            x += value
        else:
            raise Exception('Unknown command: {} {}'.format(instr, value))
    return x * y


def part2(instructions):
    x = 0
    y = 0
    aim = 0
    for instr, value in instructions:
        if instr == 'up':
            aim -= value
        elif instr == 'down':
            aim += value
        elif instr == 'forward':
            x += value
            y += aim*value
        else:
            raise Exception('Unknown command: {} {}'.format(instr, value))
    return x * y


print('Part 1: ', part1(read_input('input')))
print('Part 2: ', part2(read_input('input')))