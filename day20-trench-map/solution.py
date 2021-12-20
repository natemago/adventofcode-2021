def read_input(inpf):
    with open(inpf) as f:
        algo = f.readline().strip()
        f.readline()

        image = []
        for line in f:
            if not line.strip():
                continue
            image.append(line.strip())
        
        return algo, image
    

class State:

    def __init__(self, sx, ex, sy, ey, state, algo, outside=0):
        self.sx = sx
        self.ex = ex
        self.sy = sy
        self.ey = ey
        self.state = state
        self.algo = algo
        self.outside = outside
    
    def _is_outside(self, x, y):
        return x < self.sx  or x > self.ex or y < self.sy or y > self.ey

    def get(self, x, y):
        if self._is_outside(x, y):
            return self.outside
        return self.state.get((x, y))
    
    def get_calculated(self, x, y):
        s = ''
        for yy in (y-1, y, y+1):
            for xx in (x-1, x, x+1):
                s += '1' if self.get(xx, yy) else '0'
        return self.algo[int(s, 2)]
    
    def borders(self):
        return (
            (self.sx, self.ex),
            (self.sy, self.ey),
        )

    def next(self):
        sx = self.sx - 1
        ex = self.ex + 1
        sy = self.sy - 1
        ey = self.ey + 1

        nstate = {}
        for y in range(sy, ey + 1):
            for x in range(sx, ex + 1):
                if self.get_calculated(x, y) == '#':
                    nstate[(x, y)] = 1
        
        out_idx = 511 if self.outside else 0
        outside = 1 if self.algo[out_idx] == '#' else 0

        return State(sx, ex, sy, ey, nstate, self.algo, outside)

    def print(self, border=0):
        for y in range(self.sy-border, self.ey + 1 + border):
            for x in range(self.sx-border, self.ex + 1 + border):
                # if self._is_outside(x, y):
                #     print('X', end='')
                #     continue
                print('#' if self.get(x, y) else '.', end='')
            print()

    def how_many_on(self):
        return len(self.state)

def to_init_state(image):
    state = {}
    for y, row in enumerate(image):
        for x, c in enumerate(row):
            if c == '#':
                state[(x, y)] = 1
    return 0, len(image) - 1, 0, len(image[0]) -1, state


def part1(algo, image):
    sy, ey, sx, ex, state_map = to_init_state(image)
    state = State(sx, ex, sy, ey, state_map, algo, outside=0)
    print('------- initial state ------')
    state.print(border=3)
    print('----------------------------')
    state = state.next()
    state.print(border=2)
    print('----------------------------')
    state = state.next()
    state.print(border=1)

    return state.how_many_on()

def part2(algo, image):
    sy, ey, sx, ex, state_map = to_init_state(image)
    state = State(sx, ex, sy, ey, state_map, algo, outside=0)

    for i in range(0, 50):
        state = state.next()
    
    return state.how_many_on()

print('Part 1: ', part1(*read_input('input')))
print('Part 2: ', part2(*read_input('input')))