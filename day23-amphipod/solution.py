from math import inf
from heapq import heappush, heappop

def read_input(inpf):
    cave = []
    with open(inpf) as f:
        for line in f:
            if not line.strip():
                continue
            cave.append(line)
    
    state = ''
    for c in (3, 5, 7, 9):
        state += cave[3][c] if cave[3][c] in 'ABCD' else '0'
        state += cave[2][c] if cave[2][c] in 'ABCD' else '0'
    for h in (1, 2, 4, 6, 8, 10, 11):
        state += cave[1][h] if cave[1][h] in 'ABCD' else '0'
    return state

'''
h1-h2-+-h3-+-h4-+-h5-+-h6-h7
      |    |    |    |
      r2   r4   r6   r8
      |    |    |    |
      r1   r3   r5   r7
'''
graph = {
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

'''
a state: string of positions: r1,r2,r3,r4,r5,r6,r7,r8,h1,h2,h3,h4,h5,h6,h7
example: 
r1,r2,r3,r4,r5,r6,r7,r8,h1,h2,h3,h4,h5,h6,h7
A , B, A, C, C, D, B, D, 0, 0, 0, 0, 0, 0, 0
"ABACCDBD0000000"
'''

DEBUG = False

def _print(*args,**kwargs):
    if DEBUG:
        print(*args,**kwargs)

def print_state(state):
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

valid_rooms = {
    'A': (0, 1),
    'B': (2, 3),
    'C': (4, 5),
    'D': (6, 7),
}


def next_states(graph, state, curr_amph):
    amph = state[curr_amph]
    room = ''
    if curr_amph <= 7:
        room = 'r{}'.format(curr_amph+1)
    else:
        room = 'h{}'.format(curr_amph-7)
    _print('-----')
    _print(amph, room)
    curr_room_group = curr_amph//2

    # check if this apmh is at the bottom of its room
    if curr_amph < 7 and curr_amph %2 == 0 and amph == 'ABCD'[curr_room_group]:
        _print('   !already at the bottom of its room!')
        return []


    states = []
    for r, cost in graph[room].items():
        i = int(r[1]) - 1 if r[0] == 'r' else int(r[1]) + 7
        # check if occupied
        if state[i] != '0':
            _print('                  target=', i, '=> occupied', state)
            continue

        # check if the target is a valid room:
        #   1. if we're comming from a hallway we can only go to our room
        #   2. if we're in another room we can only go to the hallway
        #   3. if we're in our room we can go down
        if curr_amph > 7 and i <= 7:
            # we're comming from a hallway and we want to go to a room
            target_room_group = i//2
            if i not in valid_rooms[amph]:
                # we cannot go in this room
                continue


        s = state[0:curr_amph] + '0' + state[curr_amph+1:]
        s = s[0:i] + amph + s[i+1:]
        states.append((s, cost, amph))
    
    return states


def get_next_states_for_all(graph, state):
    all_states = []
    for i, apmh in enumerate(state):
        if apmh != '0':
            cs = next_states(graph, state, i)
            _print(apmh, 'at', i, '->', cs)
            all_states += cs
    return all_states


def dijkstra(graph, state, target):
    print('==========')
    print('Initial state:')
    print_state(state)
    print('Target state:')
    print_state(target)
    print('  ---')
    c = 0
    
    q = [(0, state)]
    dists = {state: 0}
    came_from = {}
    seen = set()

    while q:
        # state = q[0]
        # q = q[1:]
        cost, state = heappop(q)
        #cost = dists[state]


        #print('>', state, cost)

        seen.add(state)

        

        

        if state == target:
            print('Here we are...', state, cost)
            break

        for next_state, n_cost, _ in get_next_states_for_all(graph, state):
            if next_state in seen:
                continue
            possible_cost = cost + n_cost
            #print('  >', next_state, possible_cost, dists.get(next_state, inf))
            if possible_cost < dists.get(next_state, inf):
                # a better solution
                dists[next_state] = possible_cost
                came_from[next_state] = state
                #q.append(next_state)
                heappush(q, (possible_cost, next_state))
                #print_state(next_state)
            else:
                heappush(q, (dists.get(next_state, inf), next_state))

        
        # now we need to sort the queue
        #q = sorted(q, key=lambda st: dists.get(st, inf))
        c += 1
        if c % 1000 == 0:
            print('Looked through ', c, 'moves. Total configurations: ', len(seen))

    

def part1(state):
    print(state)
    print_state(state)
    target = 'AABBCCDD000000'
    dijkstra(graph, state, target)


#print(get_next_states_for_all(graph, "ABACCDBD0000000"))
#dijkstra(graph, 'ABACCDBD0000000', 'AABBCCDD0000000')
print('Part 1:', part1(read_input('test_input')))

# state = read_input('test_input')
# print_state(state)

# for ns,_,_ in get_next_states_for_all(graph, state):
#     print('-----------------')
#     print_state(ns)
#     print('-----------------')