def read_input(inpf):
    with open(inpf) as f:
        result = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            on = parts[0] == 'on'
            ranges = parts[1].strip().split(',')
            if len(ranges) != 3:
                raise Exception('Error on line: {}'.format(line))
            rgs = []
            for rg in ranges:
                parts = rg[2:].split('..')
                rgs.append(
                    (
                        int(parts[0]),
                        int(parts[1]),
                    )
                )
            result.append((on, rgs))
        return result


def range_intersection(r1, r2):
    a1, a2 = r1
    b1, b2 = r2

    if a1 > b1:
        return range_intersection(r2, r1)
    
    if a2 < b1:
        return None

    if a1 <= b1 and a2 >= b2:
        return (b1, b2)
    
    return (b1, a2)


def paral_intersection(p1, p2):
    ix = range_intersection(p1[0], p2[0])
    iy = range_intersection(p1[1], p2[1])
    iz = range_intersection(p1[2], p2[2])

    if not (ix and iy and iz):
        return None

    p1x, p1y, p1z = p1
    p2x, p2y, p2z = p2

    p1_paralelograms = []
    for x1, x2 in ((p1x[0], ix[0] - 1), (ix[0], ix[1]), (ix[1] + 1, p1x[1]),):
        for y1, y2 in ((p1y[0], iy[0] - 1), (iy[0], iy[1]),  (iy[1] + 1, p1y[1]),):
            for z1, z2 in ((p1z[0], iz[0] - 1), (iz[0], iz[1]), (iz[1] + 1, p1z[1])):
                if x2 < x1 or y2 < y1 or z2 < z1 or x2 > p1x[1] or y2 > p1y[1] or z2 > p1z[1]:
                    continue
                para = (
                    (x1, x2),
                    (y1, y2),
                    (z1, z2)
                )
                if para == (ix, iy, iz):
                    continue
                p1_paralelograms.append(para)
    
    p2_paralelograms = []
    for x1, x2 in ((p2x[0], ix[0] - 1), (ix[0], ix[1]), (ix[1] + 1, p2x[1]),):
        for y1, y2 in ((p2y[0], iy[0] - 1), (iy[0], iy[1]),  (iy[1] + 1, p2y[1]),):
            for z1, z2 in ((p2z[0], iz[0] - 1), (iz[0], iz[1]), (iz[1] + 1, p2z[1])):
                if x2 < x1 or y2 < y1 or z2 < z1 or x2 > p2x[1] or y2 > p2y[1] or z2 > p2z[1]:
                    continue
                para = (
                    (x1, x2),
                    (y1, y2),
                    (z1, z2)
                )
                if para == (ix, iy, iz):
                    continue
                p2_paralelograms.append(para)

    
    return (
        (ix, iy, iz),
        p1_paralelograms,
        p2_paralelograms,
    )


def part1(commands):
    cube = {}
    i = 0
    s = 0
    for on, ranges in commands:
        print('command ', i ,'of', len(commands))
        i+=1
        rx1, rx2 = ranges[0]
        ry1, ry2 = ranges[1]
        rz1, rz2 = ranges[2]

        rx = range_intersection((rx1, rx2), (-50, 50))
        ry = range_intersection((ry1, ry2), (-50, 50))
        rz = range_intersection((rz1, rz2), (-50, 50))

        if not (rx and ry and rz):
            continue
        rx1, rx2 = rx
        ry1, ry2 = ry
        rz1, rz2 = rz
        

        for x in range(rx1, rx2+1):
            for y in range(ry1, ry2+1):
                for z in range(rz1, rz2+1):
                    if on:
                        cube[(x,y,z)] = 1
                    else:
                        cube[(x, y, z)] = 0
    return sum(cube.values())


def print_partials(intersection, p1, p2):
    print('Intersection: ', intersection)
    print('P1: len=', len(p1), '; ', ', '.join(['<{}, {}, {}>'.format(*p) for p in p1]))
    print('P2: len=', len(p2), '; ', ', '.join(['<{}, {}, {}>'.format(*p) for p in p2]))

def match(on, p, paralelograms):
    p_bodies = [p]

    i = 0
    while p_bodies:
        p2 = p_bodies[0]
        p_bodies = p_bodies[1:]

        curr_body_intersects = False
        
        for i, p1 in enumerate(paralelograms):
            p1 = paralelograms[i]
            res = paral_intersection(p1, p2)
            if not res:
                continue
            intesection, p1_paras, p2_paras = res
            curr_body_intersects = True

            if on:
                # remove the current body from the paralelograms list
                # append p1_paras and intersection to it
                # append p2_paras to the p_bodues queue
                p_bodies += p2_paras
            else:
                # remove the current body from the list of paralelograms
                # append only p1 paralelograms without the intersection
                # append p2_paras to the p_bodies queue
                paralelograms = paralelograms[0:i] + p1_paras + paralelograms[i+1:]
                p_bodies += p2_paras
            break
        if not curr_body_intersects and on:
            paralelograms.append(p2)
    
    if p_bodies:
        paralelograms += p_bodies

    return paralelograms

def part2(commands):
    paralelograms = []

    i = 0
    for on, p in commands:
        paralelograms = match(on, p, paralelograms)
        i += 1
        print(i, 'paralelograms=', len(paralelograms))
    
    total = 0
    for p in paralelograms:
        x1, x2 = p[0]
        y1, y2 = p[1]
        z1, z2 = p[2]
        total += abs(x2-x1+1) * abs(y2-y1+1) * abs(z2-z1+1)
    
    return total


print('Part 1: ', part1(read_input('input')))
print('Part 2: ', part2(read_input('input')))
