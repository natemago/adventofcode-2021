from math import ceil, floor, sqrt
def part1(area):
    x1,x2 = area[0]
    y1,y2 = area[1]
    y = max(abs(y1), abs(y2))
    return y*(y-1)//2


def simulate(v, bx, by):
    x, y = 0, 0

    while True:
        if x >= bx[0] and x <= bx[1] and y >= by[0] and y <= by[1]:
            return True
        if x > bx[1]:
            return False
        if y < by[0]:
            return False
        
        x += v[0]
        y += v[1]

        v[1] -= 1
        if v[0]:
            if v[0] < 0:
                v[0] += 1
            else:
                v[0] -= 1


def part2(area):
    x1, x2 = area[0]
    y1, y2 = area[1]

    results = set()

    for x in range(0, x2+1):
        for y in range(y1, abs(y1) + 1):
            if simulate([x, y], (x1, x2), (y1, y2)):
                results.add((x, y))
    
    return len(results)

print('Part 1: ', part1([(209, 238), (-86, -59)]))
print('Part 2: ', part2([(209, 238), (-86, -59)]))