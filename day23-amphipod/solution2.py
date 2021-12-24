from math import inf
from heapq import heappush, heappop

def read_input(inpf, p2=False):
    cave = []
    with open(inpf) as f:
        for line in f:
            if not line.strip():
                continue
            cave.append(line)
    
    if p2 and len(cave) == 5:
        cave = cave[0:3] + [
            '  #D#C#B#A#',
            '  #D#B#A#C#',
        ] + cave[3:]

    state = ''
    for c in (3, 5, 7, 9):
        if p2:
            state += cave[5][c] if cave[5][c] in 'ABCD' else '0'
            state += cave[4][c] if cave[4][c] in 'ABCD' else '0'
            state += cave[3][c] if cave[3][c] in 'ABCD' else '0'
            state += cave[2][c] if cave[2][c] in 'ABCD' else '0'
        else:
            state += cave[3][c] if cave[3][c] in 'ABCD' else '0'
            state += cave[2][c] if cave[2][c] in 'ABCD' else '0'
    for h in (1, 2, 4, 6, 8, 10, 11):
        state += cave[1][h] if cave[1][h] in 'ABCD' else '0'
    return state

DEBUG = False
PART_2 = False


def _print(*args,**kwargs):
    if DEBUG:
        print(*args,**kwargs)

def print_state(state):
    if PART_2:
        print(
        '''#############
#{}.{}.{}.{}.{}#
###{}#{}#{}#{}###
  #{}#{}#{}#{}#
  #{}#{}#{}#{}#
  #{}#{}#{}#{}#
  #########'''.format(
            state[16:18], state[18], state[19], state[20], state[21:],
            state[3],state[7],state[11],state[15],
            state[2],state[6],state[10],state[14],
            state[1],state[5],state[9],state[13],
            state[0],state[4],state[8],state[12],
    )    
)
        return
    print(
        '''#############
#{}.{}.{}.{}.{}#
###{}#{}#{}#{}###
  #{}#{}#{}#{}#
  #########'''.format(
            state[8:10], state[10], state[11], state[12], state[13:],
            state[1],
            state[3],
            state[5],
            state[7],
            state[0],
            state[2],
            state[4],
            state[6],
        )
    )


'''
h1-h2-+-h3-+-h4-+-h5-+-h6-h7
      |    |    |    |
      r2   r4   r6   r8
      |    |    |    |
      r1   r3   r5   r7
'''
g1 = {
    'r1': {'r2': 1},
    'r2': {'r1': 1, 'h2': 2, 'h3': 2},
    'r3': {'r4': 1},
    'r4': {'h3': 2, 'h4': 2, 'r3': 1},
    'r5': {'r6': 1,},
    'r6': {'h4': 2, 'h5': 2, 'r5': 1},
    'r7': {'r8': 1},
    'r8': {'h5': 2, 'h6': 2, 'r7': 1},
    'h1': {'h2': 1},
    'h2': {'h1': 1, 'h3': 2, 'r2': 2},
    'h3': {'h2':2, 'h4': 2, 'r2': 2, 'r4': 2},
    'h4': {'h3': 2, 'h5': 2, 'r4': 2, 'r6': 2},
    'h5': {'h4': 2, 'h6': 2, 'r6': 2, 'r8': 2},
    'h6': {'h5': 2, 'h7': 1, 'r8': 2},
    'h7': {'h6': 1},
}
locations = ['r1', 'r2', 'r3','r4', 'r5', 'r6','r7', 'r8', 'h1', 'h2','h3', 'h4','h5', 'h6','h7']
names = {n:i for i,n in enumerate(locations)}

target_rooms = {
    'A': ('r1', 'r2'),
    'B': ('r3', 'r4'),
    'C': ('r5', 'r6'),
    'D': ('r7', 'r8'),
}

costs = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

def generate_graph(g1):
    rooms = ['r{}'.format(i) for i in range(1, (17 if PART_2 else 9))]
    hallway = ['h{}'.format(i) for i in range(1, 8)]

    graph = {}

    def bfs(src, dest):
        q = [(src, 0, [])]
        seen = set()

        while q:
            node, cost, path = q[0]
            q = q[1:]
            if node in seen:
                continue
            seen.add(node)
            if node == dest:
                return (cost, path[1:])

            for n_node, n_cost in g1[node].items():
                q.append((n_node, n_cost + cost, path + [node]))

        raise Exception('unreachable: {} -> {}'.format(src, dest))
    

    # every room to every other room
    for r1 in rooms:
        graph[r1] = {}
        for r2 in rooms:
            if r1 == r2:
                continue
            graph[r1][r2] = bfs(r1, r2)
    # every room to the hallway
    for r1 in rooms:
        for h in hallway:
            graph[r1][h] = bfs(r1, h)
    
    # from the hallway to every room
    for h in hallway:
        graph[h] = {}
        for r1 in rooms:
            graph[h][r1] = bfs(h, r1)

    return graph

graph = generate_graph(g1)

# for k, v in graph.items():
#     print(k, '->')
#     for a, b in v.items():
#         print('   ', a, '->', b)


def path_is_clear(state, path):
    for p in path:
        if state[names[p]] != '0':
            return False
    return True

def move_to(state, p1, p2, am):
    i1 = names[p1]
    i2 = names[p2]

    s = state[0:i1] + '0' + state[i1+1:]
    return s[0:i2] + am + s[i2+1:]

def room_fully_populated_with(state, room_idx, am):
    for i in range(0, len(target_rooms['A'])):
        if state[room_idx*2 + i] != am:
            return False
    return True

def is_target_room_clear(state, target_room):
    for t in target_room:
        if state[names[t]] != '0':
            return False
    return True

def is_target_room_populated_only_with(state, target_room, am):
    for t in target_room:
        if state[names[t]] not in ('0', am):
            return False
    return True

def is_at_the_right_place(state, room, place, am):
    idx = room.index(place)
    for i in range(0, idx+1):
        if state[names[room[i]]] != am:
            return False

    return True

def available_states(graph, state, am, place):
    n = names[place]
    is_room = place[0] == 'r'

    _print(am, place)
    current_room = n//(4 if PART_2 else 2)
    if is_room:
        if 'ABCD'[current_room] == am:
            _print('  . we are in our room:', am, state[current_room*2], state[current_room*2+1], current_room)
            # we're in our room
            # if n % 2 == 0 or (state[current_room*2] == am and state[current_room*2+1] == am):

            # XXX: n%2 == 0 is questionable :P
            #if n % 2 == 0 or room_fully_populated_with(state, current_room, am):
            if is_at_the_right_place(state, target_rooms['ABCD'[current_room]], place, am) or room_fully_populated_with(state, current_room, am):
                # this room is populated properly, don't move this amphipod
                return []

    target_room = target_rooms[am]
    #t1n, t2n = target_room
    _print(' target room:', target_room)
    # let's see if the target room is clear
    #t1, t2 = state[names[target_room[0]]],state[names[target_room[1]]]
    #target_room_clear = t1 == '0' and t2 == '0'
    target_room_clear = is_target_room_clear(state, target_room)
    _print(' target room clear:', target_room_clear)
    if target_room_clear:
        # go to the target room immediately
        results = []
        for t in target_room:
            if t == place:
                continue
            cost, path = graph[place][t]
            if path_is_clear(state, path):
                results.append(( move_to(state, place, t, am) , cost))
                break
        if results:
            return results
    else:
        # target room is not clear, but we can still go if we have one room available and one of our kind
        #if t1 == am:
        if is_target_room_populated_only_with(state, target_room, am):
            # if t2n != place:
            #     cost, path = graph[place][t2n]
            #     if path_is_clear(state, path):
            #         return [( move_to(state, place, t2n, am), cost )]
            for t in target_room:
                if t == place:
                    continue
                if state[names[t]] == '0':
                    cost, path = graph[place][t]
                    if path_is_clear(state, path):
                        return [(
                            move_to(state, place, t, am),
                            cost
                        )]

    if not is_room:
        # we're in a hallway, we cannot move
        return []

    # No room is available, try going to the hallway
    results = []
    for t, td in graph[place].items():
        if t[0] == 'h':
            # a hallway
            cost, path = td
            if path_is_clear(state, path):
                results.append((
                    move_to(state, place, t, am),
                    cost
                ))
    return results


def get_all_available_moves(graph, state):
    moves = []
    for i, p in enumerate(state):
        if p != '0':
            moves += [(state, cost*costs[p]) for state, cost in available_states(graph, state, p, locations[i])]
    return moves



def bfs(graph, state, target):
    q = [state]

    seen = set()

    c = 0
    while q:
        state = q[0]
        q = q[1:]

        if state == target:
            raise Exception('FOUND')
        if state in seen:
            continue
        seen.add(state)

        for ns,_ in get_all_available_moves(graph, state):
            q.append(ns)

        c += 1
        if c % 1000 == 0:
            print(c)
    
    print('Seen: ', len(seen), c, 'iterations.')


def dijkstra(graph, start, target):
    from heapq import heappop, heappush
    from math import inf

    q = [(0, start)]
    dist = {
        start: 0,
    }
    c = 0

    while q:
        cost, state = heappop(q)
        c += 1

        if state == target:
            print('Total cost: ', cost, ' ', c, 'iterations.')
            return cost
        
        for next_state, n_cost in get_all_available_moves(graph, state):
            t_cost = cost + n_cost
            if t_cost < dist.get(next_state, inf):
                dist[next_state] = t_cost
                heappush(q, (t_cost, next_state))
        
        if c % 100000 == 0:
            print('   ', c, 'iterations so far.')
        
        


def part1(state):
    return dijkstra(graph, state, 'AABBCCDD0000000')

# state = read_input('test_input')
# print('>>>>>>>>>>>>>>>')
# print(state)
# print_state(state)
# print('...............')
# for ns, cost in get_all_available_moves(graph, state):
#     print('--------------------')
#     print_state(ns)

print('Part 1: ', part1(read_input('input')))


##### setup part 2
PART_2 = True
g1 = {
    'r1': {'r2': 1},
    'r2': {'r3': 1, 'r1': 1},
    'r3': {'r4': 1, 'r2': 1},
    'r4': {'r3': 1, 'h2': 2, 'h3': 2},
    'r5': {'r6': 1},
    'r6': {'r7': 1, 'r5': 1},
    'r7': {'r8': 1, 'r6': 1},
    'r8': {'h3': 2, 'h4': 2, 'r7': 1},
    'r9': {'r10': 1},
    'r10': {'r9': 1, 'r11': 1},
    'r11': {'r12': 1, 'r10': 1},
    'r12': {'h4': 2, 'h5': 2, 'r11': 1},
    'r13': {'r14': 1},
    'r14': {'r13': 1, 'r15': 1},
    'r15': {'r16': 1, 'r14': 1},
    'r16': {'h5': 2, 'h6': 2, 'r15': 1},
    'h1': {'h2': 1},
    'h2': {'h1': 1, 'h3': 2, 'r4': 2},
    'h3': {'h2':2, 'h4': 2, 'r4': 2, 'r8': 2},
    'h4': {'h3': 2, 'h5': 2, 'r8': 2, 'r12': 2},
    'h5': {'h4': 2, 'h6': 2, 'r12': 2, 'r16': 2},
    'h6': {'h5': 2, 'h7': 1, 'r16': 2},
    'h7': {'h6': 1},
}
locations = [
    'r1', 'r2', 'r3','r4', 
    'r5', 'r6','r7', 'r8', 
    'r9', 'r10','r11', 'r12',
    'r13', 'r14','r15', 'r16',
    'h1', 'h2','h3', 'h4','h5', 'h6','h7']
names = {n:i for i,n in enumerate(locations)}

target_rooms = {
    'A': ('r1', 'r2', 'r3', 'r4'),
    'B': ('r5', 'r6','r7', 'r8'),
    'C': ('r9', 'r10','r11', 'r12'),
    'D': ('r13', 'r14','r15', 'r16'),
}

graph = generate_graph(g1)


def precalculate(graph):
    values = {}
    for am in 'ABCD':
        target_locations = target_rooms[am]
        for place in locations:
            if place not in target_locations:
                for t in target_locations:
                    cost, _ = graph[place][t]
                    values[(place, t)] = cost
    return values

_precalc = precalculate(graph)


def heuristic(state):
    cost = 0
    for i, am in enumerate(state):
        if am == '0':
            continue
        targets = target_rooms[am]
        curr_loc = locations[i]
        if curr_loc not in targets:
            for t in targets:
                cost += _precalc[(curr_loc, t)]
    return cost


def astar(graph, start, target):
    f_score = {
        start: heuristic(start)
    }
    g_score = {
        start: 0,
    }

    q = [(0, start)]
    c = 0

    while q:
        cost, state = heappop(q)
        curr_g_score = g_score.get(state, inf)

        if state == target:
            return curr_g_score
        
        for next_state, n_cost in get_all_available_moves(graph, state):
            t_score = curr_g_score + n_cost
            n_g_score = g_score.get(next_state, inf)
            if t_score < n_g_score:
                g_score[next_state] = t_score
                f_score[next_state] = t_score + heuristic(next_state)
                heappush(q, (f_score[next_state], next_state))

        c += 1
        if c % 100000 == 0:
            print(c, 'iterations.')


def part2(state):
    return dijkstra(graph, state, 'AAAABBBBCCCCDDDD0000000')


# def part2(state):
#     return astar(graph, state, 'AAAABBBBCCCCDDDD0000000')


print('Part 2: ', part2(read_input('input', True)))