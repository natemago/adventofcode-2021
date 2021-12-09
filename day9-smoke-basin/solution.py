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

def bfs(x, y, heights):
    seen = set()
    q = [(x, y)]

    r = []

    while q:
        x, y = q[0]
        q = q[1:]

        if (x, y) in seen:
            continue

        value = heights[y][x]
        seen.add((x, y))

        can_roll = False
        for nx,ny in adjacent(x, y, heights):
            if (nx, ny) not in seen and heights[ny][nx] <= value:
                q.append((nx, ny))
                can_roll = True
        
        if not can_roll:
            r.append((value, (x, y)))

    return r


def mark_all(x, y, heights):
    r = set()
    q = [(x, y)]
    seen = set()
    value = heights[y][x]

    while q:
        x, y = q[0]
        q = q[1:]

        if (x,y) in seen:
            continue
        
        seen.add((x, y))
        
        if heights[y][x] != value:
            continue

        r.add((x, y))

        for xx, yy in adjacent(x, y, heights):
            if heights[yy][xx] == value:
                q.append((xx, yy))
    
    return r


def mark_a_basin(x, y, heights):
    q = [(x, y)]
    seen = set()

    basin = set()

    while q:
        x, y = q[0]
        q = q[1:]

        if (x, y) in seen:
            continue

        if heights[y][x] == 9:
            continue
        
        if would_it_overflow(x, y, heights, seen):
            continue

        seen.add((x, y))
        basin.add((x, y))
        for xx, yy in adjacent(x, y, heights):
            q.append((xx, yy))
    return basin

def would_it_overflow(x, y, heights, seen):
    q = [(x, y)]
    marked = set()

    while q:
        x, y = q[0]
        q = q[1:]

        if (x, y) in seen or (x, y) in marked:
            continue

        value = heights[y][x]

        marked.add((x, y))

        for xx, yy in adjacent(x, y, heights):
            if (xx, yy) in seen or (xx, yy) in marked:
                continue
            if heights[yy][xx] < value:
                return True
            if heights[yy][xx] == value:
                q.append((xx, yy))

    return False


def part1(heights):
    marked = set()
    total = 0
    low_points = set()
    for y, row in enumerate(heights):
        for x, value in enumerate(row):
            r = bfs(x, y, heights)
            if r:
                lpv, lpp = min(r, key=lambda k: k[0])
                points = mark_all(lpp[0], lpp[1], heights)
                if not points.issubset(marked):
                    marked = marked.union(points)
                    low_points.add(lpp)
                    total += lpv + 1

    return total, low_points



def print_h(heights, seen):
    for y, row in enumerate(heights):
        for x, v in enumerate(row):
            if (x, y) in seen:
                print('\033[94m' + str(v) + '\033[0m', end='')
            else:
                print(v, end='')
        print()

def part2(heights):
    _, low_points = part1(heights)
    basins = []
    for x, y in low_points:
        basin = mark_a_basin(x, y, heights)
        basins.append(basin)
        print('Basin of length: ', len(basin))
        print_h(heights, basin)
        print()
    
    basins = list(sorted(basins, key=lambda b: len(b)))
    return len(basins[-1]) * len(basins[-2]) * len(basins[-3])



print('Part 1:', part1(read_input('input'))[0])
print('Part 2:', part2(read_input('input')))