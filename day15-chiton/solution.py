from itertools import product
from heapq import heappush, heappop

def read_input(inpf):
    with open(inpf) as f:
        result = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            result.append([int(c) for c in line])
        return result
    

def adjacent(x, y, risks):
    result = []
    for xx, yy in ((x-1, y), (x, y-1), (x+1, y), (x, y+1)):
        if yy >= 0 and yy < len(risks) and xx >= 0 and xx < len(risks[yy]):
            result.append((xx, yy))
    return result


def metric(p1, p2):
    return (abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]))*5


def astar(openset, start, end, heuristic, gfn, next_elems):
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    unvisited = []
    for elem in openset:
        heappush(unvisited, (f_score.get(elem, float('inf')), elem))
    
    while unvisited:
        _, elem = heappop(unvisited)
        curr_g_score = g_score.get(elem, float('inf'))

        if elem == end:
            return (curr_g_score, elem)
        
        for n in next_elems(elem):
            t_score = curr_g_score + gfn(n)
            n_g_score = g_score.get(n, float('inf'))
            if t_score < n_g_score:
                g_score[n] = t_score
                f_score[n] = t_score + heuristic(elem, n)
                heappush(unvisited, (f_score[n], n))
    return None


def part1(risks):

    risk, _ = astar(
        openset=list(product(range(len(risks)), range(len(risks)))),
        start=(0, 0),
        end=(len(risks[0]) - 1, len(risks) - 1),
        heuristic=metric,
        gfn=lambda p: risks[p[1]][p[0]],
        next_elems=lambda p: adjacent(p[0], p[1], risks))
    return risk

def part2(risks):

    def add(m, v):
        r = []

        for row in m:
            r.append([((c -1 + v)%9)+1 for c in row])

        return r

    expanded = []
    matrices = []
    for i in range(0, 5):
        row = []
        for j in range(0, 5):
            row.append(add(risks, i + j))
        matrices.append(row)
    
    for r in range(0, len(risks) * 5):
        mr = r % len(risks)
        mm = r // len(risks)
        row = []
        for i in range(0, 5):
            row += matrices[mm][i][mr]
        expanded.append(row)

    
    return part1(expanded)



print('Part 1: ', part1(read_input('input')))
print('Part 2: ', part2(read_input('input')))
