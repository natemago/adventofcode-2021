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
                # for x, y, z in permutations(beacon):
                #     for b in [(x, y, z), (x, z, -y), (x, -y, -z), (x, -z, -y)]:
                #         if self.beacons.get(orientation) is None:
                #             self.beacons[orientation] = set()
                #         self.beacons[orientation].add(b)
                #         orientation += 1
                for b in (
                    (x, y, z),
                    (x, z, -y),
                    (x, -y, -z),
                    (x, -z, y),
                    
                    (-x, y, -z),
                    (-x, -z, -y),
                    (-x, -y, z),
                    (-x, z, y),

                    (y, -x, z),
                    (y, z, x),
                    (y, x, -z),
                    (y, -z, x),

                    (-y, x, z),
                    (-y, z, -x),
                    (-y, -x, -z),
                    (-y, -z, x),

                    (z, y, -x),
                    (z, -x, -y),
                    (z, -y, x),
                    (z, x, y),

                    (-z, y, x),
                    (-z, x, -y),
                    (-z, -y, -x),
                    (-z, -x, y),

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
    
    def overlap(self, orient, other_beacons):
        beacons = self.get_beacons(orient)
        return beacons.intersection(other_beacons)
    
    def __str__(self):
        return 'S({})'.format(self.id)
    
    def __repr__(self):
        return self.__str__()




def get_scanners(report):
    return [
        Scanner(id, beacons) for id, beacons in report
    ]


def check(scanners):
    s1 = scanners[0]
    o1 = 0

    s =[(s1, o1)]

    checked = set()

    graph = {}


    while s:
        s1, o1 = s[0]
        s = s[1:]
        if (s1, o1) in checked:
            continue
        checked.add((s1, o1))
        print('Looking up match for:', s1.id, o1)
        s1_bcs = s1.get_beacons(o1)
        matches = {}
        for s2 in scanners:
            if s1 == s2:
                continue
            for o2 in range(24):
                s2_bcs = s2.get_beacons(o2)
                for b1 in s1_bcs:
                    s1_trs = s1.translate(o1, b1)
                    found = False
                    for b2 in s2_bcs:
                        s2_trs = s2.translate(o2, b2)
                        if len(s1_trs.intersection(s2_trs)) >= 12:
                            print(s1.id, 'overlaps with', s2.id)
                            if not matches.get(s2):
                                matches[s2] = []
                            matches[s2].append(o2)
                            found = True

                            edg = (s1, o1, b1)
                            if not graph.get(edg):
                                graph[edg] = []
                            
                            graph[edg].append((s2, o2, b2, (
                                b1[0] - b2[0],
                                b1[1] - b2[1],
                                b1[2] - b2[2],
                            )))

                            if len(s1_trs.intersection(s2_trs)) > 12:
                                raise Exception('MORE THAN 12!')

                            #break
                    #if found:
                    #    break

        if matches:
            print(s1.id, 'overlaps with:', matches)
            for s2, v in matches.items():
                for o2 in v:
                    s.append((s2, o2))
            
        if not matches:
            raise Exception('Sumtingswrong')
    
    print('--------------')
    for k,v in graph.items():
        print(k, '->', v)
    print('--------------')

    print('Len', len(graph))

    reconstruct(graph, scanners)

def reconstruct(graph, scanners):
    g1 = {}
    print('++++++++++++++++++++++++++')
    for s1, opts in graph.items():
        if (s1[0], s1[1]) not in g1:
            g1[(s1[0], s1[1])] = {}
        t = {}
        print(s1[0], s1[1])
        for s2 in opts:
            
            state = (s2[0], s2[1])
            print('    ', state)
            if state not in t:
                t[state] = set()
            t[state].add(s2[3])
            print('       ->', t)
        for n, tr in t.items():
            if len(tr) > 1:
                raise Exception('NOPE!')
            g1[(s1[0], s1[1])][n] = list(tr)[0]
            print('>>>>>>', (s1[0], s1[1]), '[', n, ']=', list(tr), '|', tr)
    
    print('=====================')
    for k,v in g1.items():
        print(k, '=>', v)
    

    target = set(scanners)

    start = (scanners[0], 0)
    print('==== Starting with {} ==='.format((start[0], start[1])))
    q = [(start, set())]

    seen = set()
    came_from = {
        start: ('<ROOT>', (0,0,0)),
    }

    while q:
        s1, path = q[0]
        q = q[1:]
        print(' >> at', s1, path)

        if s1 in seen:
            print('    .seen')
            continue

        seen.add(s1)
        
        for nxt, offset in g1[s1].items():
            if nxt in seen:
                continue
            print('    .nxt=', nxt)
            came_from[nxt] = (s1, offset)
            q.append((nxt, path.union({s1[0]})))
        print('<>')
    
    print('===============================')
    for k, v in came_from.items():
        print(k, '<-', v)

    def find_children(g, val):
        for k,v in g.items():
            print('       ...check', val, v)
            if val == v[0]:
                yield (k, v[1])
    
    print(list(find_children(came_from, '<ROOT>')))

    root = list(find_children(came_from, '<ROOT>'))[0]
    beacons_set = set()

    stack = [root]
    seen = set()

    while stack:
        print(stack)
        sdd, offset = stack.pop()
        scanner, orientation = sdd
        seen.add(scanner)
        beacons = [(
            b[0] + offset[0],
            b[1] + offset[1],
            b[2] + offset[2],
        ) for b in scanner.get_beacons(orientation)]
        beacons_set = beacons_set.union(set(beacons))
        print('  ..sdd=', sdd)
        for n, ofs in find_children(came_from, sdd):
            stack.append((n, (
                ofs[0] + offset[0],
                ofs[1] + offset[1],
                ofs[2] + offset[2],
            )))

        
    print(beacons_set)
    print('Len=', len(beacons_set))
    print('Seen=', list(sorted(seen, key=lambda s: s.id)))
    print('Scanners=', scanners)
        



def part1(report):
    scanners = get_scanners(report)

    graph = {}

    for i, s1 in enumerate(scanners[0:-1]):
        for s2 in scanners[i+1:]:
            print('Checking {} with {}'.format(s1.id, s2.id))
            for o1, o2 in product(range(24), range(24)):
                beacons = s1.get_beacons(o1)
                for b1 in beacons:
                    s1_beacons = s1.translate(o1, b1)
                    
                    s2_beacons =  s2.get_beacons(o2) #s2.translate(o2, b)
                    
                    for b2 in s2_beacons:
                        other_beacons = s2.translate(o2, b2)
                        overlap = s1_beacons.intersection(other_beacons)
                        
                        if len(overlap) >= 12:
                            if (s1.id, o1) not in graph:
                                graph[(s1.id, o1)] = []
                            graph[(s1.id, o1)].append((
                                s2, o2, beacons.union(other_beacons), b1
                            ))
                            print('    .overlap of ', len(overlap), ' @ ', o1, o2)



def part1(report):
    scanners = get_scanners(report)
    check(scanners)


print('Part 1:', part1(read_input('input')))


# id, beacons = read_input('test_input')[0]
# scanner = Scanner(id, beacons)

# for i in range(24):
#     print('-----------')
#     for b in sorted(scanner.get_beacons(i), key=lambda n: sum((abs(k) for k in n))):
#         print(b)