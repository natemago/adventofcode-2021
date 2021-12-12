def read_input(inpf):
    with open(inpf) as f:
        result = []
        for line in f:
            result.append([int(c) for c in line.strip()])
        return result


def adjacent(x, y, octos):
    res = []
    for xx, yy in (
        (x-1, y-1), (x, y-1), (x+1, y-1),
        (x-1, y),             (x+1, y),
        (x-1, y+1), (x, y+1), (x+1, y+1),
    ):
        if yy >= 0 and yy < len(octos) and xx >=0 and xx < len(octos[yy]):
            res.append((xx, yy))
    return res

def part1(octos):
    
    total = 0
    i = 1
    all_synced_at = None
    while True:
        state = []
        flashed = set()
        # increase all by 1
        for y, row in enumerate(octos):
            sr = []
            for x, value in enumerate(row):
                value += 1
                if value > 9:
                    flashed.add((x, y))
                sr.append(value)
            state.append(sr)
        
        q = list(flashed)

        while q:
            x, y = q[0]
            q = q[1:]
            
            for xx, yy in adjacent(x, y, state):
                state[yy][xx] += 1
                if state[yy][xx] > 9:
                    if (xx, yy) not in flashed:
                        q.append((xx, yy))
                        flashed.add((xx, yy))
        
        for x,y in flashed:
            state[y][x] = 0
        
        octos = state
        if i <= 100:
            total += len(flashed)
        
        if len(flashed) == 100:
            all_synced_at = i
        
        if i > 100 and all_synced_at:
            break
        
        i += 1

    return total, all_synced_at

print('Part 1: {}\nPart 2: {}'.format(*part1(read_input('input'))))
