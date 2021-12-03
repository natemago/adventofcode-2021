def read_input(inpf):
    with open(inpf) as f:
        return [line.strip() for line in f.readlines()]


def part1(lines):
    results = []
    gamma = ''
    epsilon = ''
    for i in range(0, len(lines[0])):
        r = {}
        for line in lines:
            c = line[i]
            r[c] = r.get(c, 0) + 1
        gamma += '1' if r['1'] > r['0'] else '0'
        epsilon += '1' if r['1'] < r['0'] else '0'
    return int(gamma, 2) * int(epsilon, 2)


def get_bits_stats(lines, i):
    r = {}
    for line in lines:
        c = line[i]
        r[c] = r.get(c, 0) + 1
    return r


def get_rating(lines, rating_fn):
    i = 0
    n = len(lines[0])

    while len(lines) > 1:
        r = get_bits_stats(lines, i)
        rating = rating_fn(r)
        lines = list(filter(lambda line: line[i] == rating, lines))
        i += 1
    
    return lines[0]


def part2(lines):
    oxygen_rating_fn = lambda r: '1' if r['1'] >= r['0'] else '0'
    co2_rating_fn = lambda r: '1' if r['1'] < r['0'] else '0'
    oxygen_rating = get_rating(lines, oxygen_rating_fn)
    co2_rating = get_rating(lines, co2_rating_fn)
    return int(oxygen_rating, 2) * int(co2_rating, 2)


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))
