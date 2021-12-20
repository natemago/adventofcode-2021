from itertools import permutations, product

def read_input(inpf):
    with open(inpf) as f:
        scanners = []
        curr_scanner = None
        curr_map = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('---'):
                if not curr_scanner:
                    line = line.split()
                    curr_scanner = line[2]
                else:
                    scanners.append((curr_scanner, curr_map))
                    line = line.split()
                    curr_scanner = line[2]
                    curr_map = []
            else:
                line = line.split(',')
                curr_map.append((int(n) for n in line))
        if curr_scanner and curr_map:
            scanners.append((curr_scanner, curr_map))

        return scanners


class Scanner:

    def __init__(self, id, beacons, orient=0):
        self.id = id
        self.beacons = {}
        self.orientation = orient
        
        for x,y,z in beacons:
                orientation = 0
                for b in (
                    (x, y, z),
                    (x, z, -y),
                    (x, -y, -z),
                    (x, -z, y),

                    (-x, y, -z),
                    (-x, -z, -y),
                    (-x, -y, z),
                    (-x, z, y),

                    (-y, x, z),
                    (-z, x, -y),
                    (y, x, -z),
                    (z, x, y),

                    (y, -x, z),
                    (-z, -x, y),
                    (-y, -x, -z),
                    (z, -x, -y),

                    (-z, y, x),
                    (-y, -z, x),
                    (z, -y, x),
                    (y, z, x),

                    (z, y, -x),
                    (-y, z, -x),
                    (-z, -y, -x),
                    (y, -z, -x),

                ):
                    if self.beacons.get(orientation) is None:
                        self.beacons[orientation] = set()
                    self.beacons[orientation].add(b)
                    orientation += 1
        
        self.translations = {}
        for o in range(24):
            for b in self.beacons[o]:
                self.translations[(o, b)] = self._translate(o, b)

        
        print('Scanner {} has {} beacons with {} orientations.'.format(
            self.id,
            len(beacons),
            len(self.beacons),
        ))
                
    def get_beacons(self, orient):
        return self.beacons[orient]
    
    def translate(self, orient, delta):
        return self.translations[(orient, delta)]
    
    def _translate(self, orient, delta):
        return set(map(lambda b: (b[0] - delta[0], b[1] - delta[1], b[2] - delta[2]), self.get_beacons(orient)))
    
    def __str__(self):
        return 'S({})'.format(self.id)
    
    def __repr__(self):
        return self.__str__()




def get_scanners(report):
    return [
        Scanner(id, beacons) for id, beacons in report
    ]

'''

start with the first scanner

initalize the solved with the first

while there are still scanners not matched:
    get next scanner from the unsolved
    try to match the scanner somewhere in the list of solved
    if there was a match:
        put the scanner in the list of solved
        remove it from the list of unsloved

'''

class Found(Exception):
    pass

def part1(report):
    
    scanners = get_scanners(report)
    solved = set([(scanners[0], 0)])
    unsolved = scanners[1:]

    tree = {}

    while unsolved:
        s2 = unsolved[0]
        unsolved = unsolved[1:]
        found = False
        try:
            for o2 in range(24):
                s2_beacons = s2.get_beacons(o2)
                for b2 in s2_beacons:
                    s2_trans = s2.translate(o2, b2)
                    for s1, o1 in solved:
                        s1_beacons = s1.get_beacons(o1)
                        for b1 in s1_beacons:
                            s1_trans = s1.translate(o1, b1)
                            if len(s1_trans.intersection(s2_trans)) >= 12:
                                solved.add((s2, o2))

                                offset = (
                                    b1[0] - b2[0],
                                    b1[1] - b2[1],
                                    b1[2] - b2[2],
                                )

                                k1 = (s1, o1)
                                if k1 not in tree:
                                    tree[k1] = []
                                tree[k1].append((s2, o2, offset))

                                raise Found()
        except Found as e:
            found = True
        if not found:
            unsolved.append(s2)
    
    # print('=========================')
    # for k, v in tree.items():
    #     print(k, ' => ', v)
    

    stack = [(scanners[0], 0, (0, 0, 0))]

    beacons_map = set()

    positions = [(0, 0, 0)]

    while stack:
        s1, o1, offset = stack.pop()

        beacons = [(
            b[0] + offset[0],
            b[1] + offset[1],
            b[2] + offset[2],
        ) for b in s1.get_beacons(o1)]

        beacons_map = beacons_map.union(set(beacons))

        if (s1, o1) not in tree:
            continue
        for c1, oc1, off in tree[(s1, o1)]:
            positions.append((
                offset[0] + off[0],
                offset[1] + off[1],
                offset[2] + off[2],
            ))
            stack.append((
                c1,
                oc1,
                (
                    offset[0] + off[0],
                    offset[1] + off[1],
                    offset[2] + off[2],
                )
            ))

    return len(beacons_map), positions


def part2(report):
    _, positions = part1(report)

    distances = []
    for i, s1 in enumerate(positions[0:-1]):
        for s2 in positions[i+1:]:
            distances.append(sum((
                abs(s1[0] - s2[0]),
                abs(s1[1] - s2[1]),
                abs(s1[2] - s2[2]),
            ))) 

    return max(distances)



print('Part 1:', part1(read_input('input'))[0])
print('Part 2:', part2(read_input('input')))
