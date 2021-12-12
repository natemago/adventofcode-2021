def read_input(inpf):
    result = []
    with open(inpf) as f:
        for line in f:
            line = line.strip().split('-')
            result.append((line[0].strip(), line[1].strip()))
    return result


class V:

    def __init__(self, name):
        self.name = name
        self.is_upper = name == name.upper()
        self.edges = set()
    
    def outgoing(self):
        out = set()
        for e in self.edges:
            for v in (e.v1, e.v2):
                if v != self:
                    # if v.is_upper:
                    #     for vv in v.outgoing():
                    #         if vv != self:
                    #             out.add(vv)
                    # else:
                    #     out.add(v)
                    out.add(v)
        return out

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class E:
    def __init__(self, v1, v2, via_upper=False):
        self.v1 = v1
        self.v2 = v2
        self.via_upper = via_upper


class G:

    def __init__(self):
        self.vertices = {}
        self.edges = {}
    
    def vertex(self, name):
        v = self.vertices.get(name)
        if not v:
            v = V(name)
            self.vertices[name] = v
        return v
    
    def edge(self, v1, v2, via_upper=False):
        k1 = '{}-{}'.format(v1.name, v2.name)
        k2 = '{}-{}'.format(v2.name, v1.name)
        e = self.edges.get(k1) or self.edges.get(k2)
        if not e:
            e = E(v1, v2, via_upper)
            self.edges[k1] = e
            self.edges[k2] = e
        v1.edges.add(e)
        v2.edges.add(e)
        return e
    

def part1(conns):
    graph = G()
    for a, b in conns:
        graph.vertex(a)
        graph.vertex(b)
    
    for a, b in conns:
        va = graph.vertex(a)
        vb = graph.vertex(b)
        graph.edge(va, vb)
    
    start = graph.vertex('start')
    end = graph.vertex('end')
    
    r = {'count': 0}
    def reach(v, end, path):
        if v == end:
            # print(path + [end])
            r['count'] += 1
            return
        for vn in v.outgoing():
            if vn in path:
                if not vn.is_upper:
                    continue
            reach(vn, end, path + [v])
        

    reach(start, end, [])
    return r['count']


def part2(conns):
    graph = G()
    for a, b in conns:
        graph.vertex(a)
        graph.vertex(b)
    
    for a, b in conns:
        va = graph.vertex(a)
        vb = graph.vertex(b)
        graph.edge(va, vb)
    
    start = graph.vertex('start')
    end = graph.vertex('end')
    small_caves = filter(lambda v: not v.is_upper, graph.vertices.values())

    paths = set()
    def reach(v, end, small_cave, path):
        if v == end:
            p = ','.join([a.name for a in path + [end]])
            # print(p)
            paths.add(p)
            return
        for vn in v.outgoing():
            if vn in path:
                if not vn.is_upper:
                    # count how many times this cave has been visited already
                    visited = len(list(filter(lambda c: c == vn, path)))
                    if vn == start:
                        continue
                    if vn == small_cave:
                        if visited == 2:
                            continue
                    else:
                        continue

            reach(vn, end, small_cave, path + [v])
        

    for sm in small_caves:
        reach(start, end, sm, [])
    return len(paths)


print('Part 1: ', part1(read_input('input')))
print('Part 2: ', part2(read_input('input')))