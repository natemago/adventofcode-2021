def read_input(inpf):
    with open(inpf) as f:
        result = []
        for line in f:
            line = line.strip()
            result.append([int(c) for c in line])
        return result


def adjacent(x, y, heights):
    r = []
    for xx, yy in ((x + 1, y), (x, y-1), (x-1, y), (x, y+1)):
        if yy >= 0 and yy < len(heights) and xx >= 0 and xx < len(heights[yy]):
            r.append((xx, yy))
    return r

def flood_fill(x, y, heights, next):
    q = [(x, y)]
    seen = set()

    while q:
        x, y = q[0]
        q = q[1:]

        if (x, y) in seen:
            continue
        seen.add((x, y))
        adj = adjacent(x, y, heights)
        for n in next(adj, heights[y][x], (x, y)):
            q.append(n)
    
    return seen

def part1(heights):

    def get_low_point(x, y, seen):
        adj = list(filter(lambda p: heights[p[1]][p[0]] <= heights[y][x], set(adjacent(x, y, heights)) - seen))
        seen.add((x, y))
        if not adj:
            return (heights[y][x], x, y)
        return min([ get_low_point(xx, yy, seen) for xx, yy in adj])
    
    seen = set()
    total = 0

    for y, row in enumerate(heights):
        for x, _ in enumerate(row):
            p = get_low_point(x, y, set())
            all_points = flood_fill(p[1], p[2], heights, lambda adj, value, _: filter(lambda k: heights[k[1]][k[0]] == value, adj))
            if all_points.issubset(seen):
                continue
            seen = seen.union(all_points)
            total += p[0] + 1
    return total

def part2(heights):
    basins = set()
    for y, row in enumerate(heights):
        for x, _ in enumerate(row):
            if heights[y][x] == 9:
                continue
            basin = flood_fill(x, y, heights, lambda adj, value, _: filter(lambda a: heights[a[1]][a[0]] != 9, adj))
            basin = frozenset(basin)
            if basin not in basins:
                basins.add(basin)
                print('Basin of size: ', len(basin))
                print_h(heights, basin)
    basins = list(sorted([len(b) for b in basins]))

    return basins[-1] * basins[-2] * basins[-3]


def print_h(heights, seen):
    for y, row in enumerate(heights):
        for x, v in enumerate(row):
            if (x, y) in seen:
                print('\033[94m' + str(v) + '\033[0m', end='')
            else:
                print(v, end='')
        print()

print('Part 1: ', part1(read_input('input')))
print('Part 2: ', part2(read_input('input')))