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

def par1(instructions):
    alu = ALU(instructions)
    return alu.check()


#print('Part 1: ', par1(read_input('input')))

def test_procedures(instrs):
    alu = ALU(instrs)

    # print(
    #     alu.detect_procedure_behaviour(13)
    # )

    # for p in range(14):
    #     print('Proc: ', p)
    #     print('==========')
    #     for d in range(1, 10):
    #         r = alu.detect_procedure_behaviour_per_digit(p, d)
    #         print('  >', d, r)

    #print(alu.find_target_p(12, 9))
    alu.check()
            

test_procedures(read_input('input'))