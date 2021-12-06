def read_input(inpf):
    result = []
    with open(inpf) as f:
        for line in f:
            line = line.strip()
            points = line.split('->')
            if len(points) != 2:
                raise Exception('Invalid line:', line)
            p1 = points[0].strip().split(',')
            p2 = points[1].strip().split(',')
            result.append((
                (int(p1[0]), int(p1[1])),
                (int(p2[0]), int(p2[1])),
            ))
    return result



def part1(points):
    world = {}
    for p1,p2 in points:
        x1,y1=p1
        x2,y2=p2

        if x1 == x2:
            m1 = min([y1, y2])
            m2 = max([y1, y2])
            for i in range(m1, m2+1):
                world[(x1, i)] = world.get((x1, i), 0) + 1
        elif y1 == y2:
            m1 = min([x1, x2])
            m2 = max([x1, x2])
            for i in range(m1, m2+1):
                world[(i, y1)] = world.get((i, y1), 0) + 1

    count = 0
    for _, v in world.items():
        if v > 1:
            count += 1
    return count


def part2(points):
    world = {}
    for p1,p2 in points:
        x1,y1=p1
        x2,y2=p2

        dx = x2-x1
        dy = y2-y1

        sx = dx/abs(dx) if dx != 0 else 0
        sy = dy/abs(dy) if dy != 0 else 0

        x,y = x1,y1

        while True:
            world[(x, y)] = world.get((x, y), 0) + 1
            x += sx
            y += sy
            if (x,y) == (x2, y2):
                world[(x, y)] = world.get((x, y), 0) + 1
                break
        

    count = 0
    for _, v in world.items():
        if v > 1:
            count += 1

    return count


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))