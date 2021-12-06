def read_input(inpf):
    with open(inpf) as f:
        return [int(n.strip()) for n in f.readline().strip().split(',')]


def part1(timers):
    print('Initial state: ', timers)
    for i in range(0, 80):
        new = []
        for j,t in enumerate(timers):
            if t == 6:
                timers[j] -= 1
            elif t == 0:
                timers[j] = 6
                new.append(8)
            else:
                timers[j] -= 1
        timers += new
        #print(i, ' -> ', timers)
    return len(timers)


def count_fish(days, cache):
    count = cache.get(days)
    if count:
        return count
    count = 0
    
    n = days
    
    while n >= 0:
        count += 1
        if n - 9 >= 0:
            count += count_fish(n-9, cache)
        n -= 7

    cache[days] = count

    return count


def part2(timers, days=256):
    total = 0
    cache = {}
    for t in timers:
        total += count_fish(days - t - 1, cache) + 1
    
    return total


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))