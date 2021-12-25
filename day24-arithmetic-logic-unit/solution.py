from itertools import product
from functools import cache
from math import floor, ceil


def read_input(inpf):
    with open(inpf) as f:
        instructions = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            instructions.append(tuple(p.strip() for p in line.split()))
        return instructions

class ALU:

    def __init__(self, instrcutions):
        self.instructions = instrcutions
        self._procedures = self.procedures()
        self.behaviour = self.detect_procedures_behaviour()
    
    def procedures(self):
        procs = []
        proc = []

        for instr in self.instructions:
            if instr[0] == 'inp':
                if proc:
                    procs.append(proc)
                    proc = []
            proc.append(instr)
        
        if proc:
            procs.append(proc)
        
        return procs


    @cache
    def exec_proc(self, proc_id, z, inp):
        state = {
            'x': 0,
            'y': 0,
            'z': z,
            'w': inp,
        }

        procedure = self._procedures[proc_id]
        assert procedure[0] == ('inp', 'w')

        for instr in procedure[1:]:
            op, v1, v2 = instr
            v2 = state[v2] if v2 in 'xyzw' else int(v2)
            if op == 'add':
                state[v1] = state[v1] + v2
            elif op == 'mul':
                state[v1] = state[v1] * v2
            elif op == 'div':
                if v2 == 0:
                    raise Exception('Alu Crash!')
                state[v1] = state[v1] // v2
            elif op == 'mod':
                if state[v1] < 0 or v2 <= 0:
                    raise Exception('ALU Crash!')
                state[v1] = state[v1] % v2
            elif op == 'eql':
                state[v1] = 1 if state[v1] == v2 else 0
            else:
                raise Exception('Unknown instruction: {}', instr)
        
        return state

    def run(self, inputs):
        z = 0
        for i, d in enumerate(inputs):
            state = self.exec_proc(i, z, d)
            z = state['z']
        return z
    
    def check_for_digit(self, proc_id, d, target):
        n = 0
        while True:
            res = self.exec_proc(proc_id, n, d)['z']
            if res == target:
                print('       .found one:', proc_id, d, target, ' => ', n)
                break
            n += 1
            if n > 10_000_000:
                return None
        return n
    
    @cache
    def check_for_procedure(self, proc_id, target):
        results = []
        d = 9
        while d >= 0:
            res = self.check_for_digit(proc_id - 1, d, target)
            if res is None:
                continue
            results.append(res)

            d -= 1
        

    def detect_procedure_behaviour_per_digit(self, proc_id, d):
        detected_jump = None
        prev = None
        first = None
        coeffs = []
        for i in range(0, 1000):
            res = self.exec_proc(proc_id, i, d)['z']
            if i:
                coeffs.append(res/i)
            if prev is None:
                prev = res
                continue
            if res < prev:
                if first is None:
                    first = i
                else:
                    detected_jump = i - first
                    return ('jump', detected_jump, first)
            prev = res
        
        # linear increase

        coeff = sum(coeffs)/len(coeffs)
        if not (coeff > 25 and coeff < 27):
            print('!!!!!>>', coeff)
            raise Exception('Not steady increase?')

        return ('increase', coeff)

    def detect_procedures_behaviour(self):
        result = {}
        for proc_id in range(14):
            result[proc_id] = {}
            for d in range(1, 10):
                result[proc_id][d] = self.detect_procedure_behaviour_per_digit(proc_id, d)
        return result
    
    def find_target(self, proc_id, d, target):
        beh = self.behaviour[proc_id][d]
        if beh[0] == 'jump':
            _, size, start = beh
            curr = self.exec_proc(proc_id, start, d)['z']
            if curr == target:
                print('exact')
                return start
            start += size*(target-1)
            print((target-start)/size, 'steps')
            while True:
                start += size
                res = self.exec_proc(proc_id, start, d)['z']
                if res == target:
                    print('found', res)
                    return start
                if res > target:
                    return None
                #print('       checking', res, '==', target)
        elif beh[0] == 'increase':
            _, coeff = beh
            start = floor(target/(coeff+0.2))
            end = ceil(target/(coeff-0.2))
            #print('find ', target, ' between ', (start, end), 
                # (self.exec_proc(proc_id, start, d)['z'],
                # self.exec_proc(proc_id, end, d)['z'],
                # ))
            for i in range(start, end+1):
                res = self.exec_proc(proc_id, i, d)['z']
                if res == target:
                    print(':::found', i)
                    return i
            
            return None
        else:
            raise Exception('Uknown behaviour: {}'.format(beh))


    @cache
    def find_target_p(self, proc_id, target):
        possible = []
        for d in range(9, 0, -1):
            res = self.find_target(proc_id, d, target)
            if res is None:
                continue
            possible.append((res, d))
        
        return possible
    


    def check(self):
        q = [(13, 0)]

        c = 0
        while q:
            proc_id, target = q[0]
            q = q[1:]

            if proc_id == 0:
                print('FOUND!')
            
            for tg, d in self.find_target_p(proc_id, target):
                q.append((proc_id-1, tg))
            c += 1
            if c % 10 == 0:
                print(c, proc_id, len(q))
    
    def assert_procedure(self, proc_id, proc, tests=1000):
        passed = 0
        failed = 0
        for i in range(0, tests):
            for d in range(1, 10):
                expected = self.exec_proc(proc_id, i, d)['z']
                value = proc(i, d)
                if value != expected:
                    print('Failed for procedure {} on digit {} (input {}). Expected {}, but got {} instead.'.format(
                        proc_id, d, i, expected, value))
                    failed += 1
                else:
                    passed += 1
        print('Tests: {}. Failed: {}. Passed: {}'.format((failed+passed), failed, passed))
        return failed


def procedure_0(z, w):
    return z * 26 + w + 14

def rev_procedure_0(target):
    # return z * 26 + w + 14
    '''
    z * 26 + w + 14 = t
    z * 26 = t - 14 - w
    
        t - w - 14
    z = -----------
            26
    '''
    results = {}
    
    for w in range(1, 10):
        p = target - w - 14
        if p < 0:
            continue
        if p % 26:
            continue
        results[w] = results.get(w) or []
        results[w].append(p//26)

    return results

def procedure_1(z, w):
    return z * 26 + w + 6

def rev_procedure_1(target):
    results = {}
    
    for w in range(1, 10):
        p = target - w - 6
        if p < 0:
            continue
        if p % 26:
            continue
        results[w] = results.get(w) or []
        results[w].append(p//26)

    return results

procedure_2 = procedure_1
rev_procedure_2 = rev_procedure_1

def procedure_3(z, w):
    return z * 26 + w + 13

def rev_procedure_3(target):
    results = {}
    
    for w in range(1, 10):
        p = target - w - 13
        if p < 0:
            continue
        if p % 26:
            continue
        results[w] = results.get(w) or []
        results[w].append(p//26)

    return results



def procedure_4(z, w):
    if (z % 26) - 12 == w: # z%26 must be [13 to 21]
        return (z // 26)
    else:
        # will increase with steps of length 26
        return (z // 26) * 26 + (w + 8) # always positive

def rev_procedure_4(target):
    results = {n:[] for n in range(1, 10)}
    for i in range(21, 13-1, -1):
        results[i-12].append(target*26 + i)
    for i in range(1, 10):
        if target%26 == (i+8):
            results[i].append(target - (target%26))
    return results

def procedure_5(z, w):
    return z * 26 + w + 8

def rev_procedure_5(target):
    results = {}
    
    for w in range(1, 10):
        p = target - w - 8
        if p < 0:
            continue
        if p % 26:
            continue
        results[w] = results.get(w) or []
        results[w].append(p//26)

    return results

def procedure_6(z, w):
    if (z % 26) - 15 == w: # for z % 26 in [16 to 24]
        return (z // 26)
    else:
        # will increase with steps of length 26
        return (z // 26) * 26 + (w + 7) # always positive

def rev_procedure_6(target):
    results = {n:[] for n in range(1, 10)}
    for i in range(24, 16-1, -1):
        results[i-15].append(target*26 + i)
    for i in range(1, 10):
        if target%26 == (i+7):
            results[i].append(target - (target%26))
    return results


def procedure_7(z, w):
    return z * 26 + w + 10

def rev_procedure_7(target):
    results = {}
    
    for w in range(1, 10):
        p = target - w - 10
        if p < 0:
            continue
        if p % 26:
            continue
        results[w] = results.get(w) or []
        results[w].append(p//26)

    return results

procedure_8 = procedure_5
rev_procedure_8 = rev_procedure_5

def procedure_9(z, w):
    if (z % 26) - 13 == w: # z%26 must be [14 to 22]
        return (z // 26)
    else:
        # will increase with steps of length 26
        return (z // 26) * 26 + (w + 12) # always positive

def rev_procedure_9(target):
    results = {n:[] for n in range(1, 10)}
    for i in range(22, 14-1, -1):
        results[i-13].append(target*26 + i)
    for i in range(1, 10):
        if target%26 == (i+12):
            results[i].append(target - (target%26))
    return results

def procedure_10(z, w):
    if (z % 26) - 13 == w: # z%26 must be [14 to 22]
        return (z // 26)
    else:
        # will increase with steps of length 26
        return (z // 26) * 26 + (w + 10) # always positive

def rev_procedure_10(target):
    results = {n:[] for n in range(1, 10)}
    for i in range(22, 14-1, -1):
        results[i-13].append(target*26 + i)
    for i in range(1, 10):
        if target%26 == (i+10):
            results[i].append(target - (target%26))
    return results


def procedure_11(z, w):
    if (z % 26) - 14 == w: # z%26 must be [15 to 23]
        return (z // 26)
    else:
        # will increase with steps of length 26
        return (z // 26) * 26 + (w + 8) # always positive

def rev_procedure_11(target):
    results = {n:[] for n in range(1, 10)}
    for i in range(23, 15-1, -1):
        results[i-14].append(target*26 + i)
    for i in range(1, 10):
        if target%26 == (i+8):
            results[i].append(target - (target%26))
    return results

def procedure_12(z, w):
    if (z % 26) - 2 == w: # z%26 must be [3 to 11]
        return (z // 26)
    else:
        # will increase with steps of length 26
        return (z // 26) * 26 + (w + 8) # always positive


def rev_procedure_12(target):
    results = {n:[] for n in range(1, 10)}
    for i in range(11, 3-1, -1):
        results[i-2].append(target*26 + i)
    for i in range(1, 10):
        if target%26 == (i+8):
            results[i].append(target - (target%26))
    return results

def procedure_13(z, w):
    if (z % 26) - 9 == w: # z%26 must be [10 to 18]
        return (z // 26) # z must be less than 26 - so z can be [10,...,18]
    else:
        # will increase with steps of length 26
        return (z // 26) * 26 + (w + 7) # always positive


def rev_procedure_13(target):
    results = {n:[] for n in range(1, 10)}
    for i in range(18, 10-1, -1):
        results[i-9].append(target*26 + i)
    for i in range(1, 7):
        if target%26 == (i+7):
            results[i].append(target - (target%26))
    return results


def par1(instructions):
    alu = ALU(instructions)
    return alu.check()


#print('Part 1: ', par1(read_input('input')))

# def test_procedures(instrs):
#     alu = ALU(instrs)

#     # print(
#     #     alu.detect_procedure_behaviour(13)
#     # )

#     # for p in range(14):
#     #     print('Proc: ', p)
#     #     print('==========')
#     #     for d in range(1, 10):
#     #         r = alu.detect_procedure_behaviour_per_digit(p, d)
#     #         print('  >', d, r)

#     # print(alu.find_target_p(12, 9))
#     # alu.check()



#     #alu.assert_procedure(12, procedure_12, 10_000)
#     # for i, proc in enumerate(alu.procedures()):
#     #     print('Procedure:', i)
#     #     for p in proc:
#     #         print(' '.join(p))

#     for i in range(100):
#         print('==', i)
#         for w, pos in rev_procedure_13(i).items():
#             #print(z, pos)
#             for z in pos:
#                 r = procedure_13(z, w)
#                 print(' >', r, (z, w))
#                 print(' >>', alu.exec_proc(13, z, w)['z'])


# test_procedures(read_input('input'))
# import os
# os.exit(1)
# # for i in range(30):
# #     print(procedure_0(i, 9))

procedures = [
    (procedure_0, rev_procedure_0),
    (procedure_1, rev_procedure_1),
    (procedure_2, rev_procedure_2),
    (procedure_3, rev_procedure_3),
    (procedure_4, rev_procedure_4),
    (procedure_5, rev_procedure_5),
    (procedure_6, rev_procedure_6),
    (procedure_7, rev_procedure_7),
    (procedure_8, rev_procedure_8),
    (procedure_9, rev_procedure_9),
    (procedure_10, rev_procedure_10),
    (procedure_11, rev_procedure_11),
    (procedure_12, rev_procedure_12),
    (procedure_13, rev_procedure_13),
]





def preliminary_tests(instructions, size=10_000):
    alu = ALU(instructions)

    def _assert(truth, expected, actual):
        if not truth:
            raise Exception('Expected: {}, but got: {}'.format(expected, actual))

    for proc_id in range(14):
        print('Testing procedure: ', proc_id)
        procedure, rev_procedure = procedures[proc_id]
        print('Asserting basic equivalence...')
        failed = alu.assert_procedure(proc_id, procedure)
        assert failed == 0
        print('All OK')
        print('Testing reverse procedures...')
        for target in range(size+1):
            for w, possible in rev_procedure(target).items():
                for z in possible:
                    value = procedure(z, w)
                    _assert( value == target, target, value)
                    # compare against the actual interpreter
                    expected = alu.exec_proc(proc_id, z, w)['z']
                    _assert(value == expected, expected, value)
        print('All OK.')

preliminary_tests(read_input('input'))

def part1(instructions):
    alu = ALU(instrcutions)

    q = [(0, 0)]

    while q:
        proc_id, target = q.pop()
        