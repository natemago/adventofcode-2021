def read_input(inpf):
    with open(inpf) as f:
        sea_map = []
        for line in f:
            line = line.strip()
            if not line:
                break
            sea_map.append([c for c in line])
        return sea_map

def to_state(sea_map):
    state = {'v': set(), '>': set()}
    for y, row in enumerate(sea_map):
        for x, c in enumerate(row):
            if c in '>v':
                state[c].add((x, y))
    return state, len(sea_map[0]), len(sea_map)


def move_herd(state, width, height, herd):
    moving = state[herd]
    stationary = state['>' if herd == 'v' else 'v']
    dx, dy = (1, 0) if herd == '>' else (0, 1)

    moved = set()
    unmoved = set()
    for x, y in moving:
        n = ((x+dx)%width, (y+dy)%height)
        if n in stationary or n in moving:
            unmoved.add((x, y))
        else:
            moved.add(n)
    ns = {}
    ns.update(state)
    ns[herd] = moved.union(unmoved)
    
    return ns, len(moved)

def next_state(state, width, height):
    state, h_moved = move_herd(state, width, height, '>')
    state, v_moved = move_herd(state, width, height, 'v')

    return state, h_moved or v_moved

    
def print_state(state, w, h):
    vert = state['v']
    hor = state['>']
    for y in range(h):
        for x in range(w):
            n = (x, y)
            if n in vert:
                print('V', end='')
            elif n in hor:
                print('>', end='')
            else:
                print('.', end='')
        print()



def part1(sea_map):
    state, width, height = to_state(sea_map)
    step = 0
    while True:
        state, has_moved = next_state(state, width, height)
        step += 1
        if not has_moved:
            break
    return step

print(('\033[33m' + '★' + '\033[0m')*50)
print('\033[32mThe cucumbers stop moving after: \033[0m\033[31m', part1(read_input('input')), '\033[0m\033[32msteps.\033[0m')
print(('\033[33m' + '★' + '\033[0m' + '\033[32m' + '★' + '\033[0m')*25)