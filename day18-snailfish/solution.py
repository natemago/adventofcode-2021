from math import ceil, floor

def read_input(inpf):
    with open(inpf) as f:
        res = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            res.append(line)
        return res

class Num:

    def __init__(self, value=None, depth=0):
        self.depth = depth
        self.l = None
        self.r = None
        self.value = value
        self.parent = None
    
    def set_depth(self, initial=0):
        self.depth = initial
        if self.value != ',':
            return
        for c in [self.l, self.r]:
            c.set_depth(self.depth + 1)

    def __str__(self):
        if self.value == ',':
            return '[{},{}]'.format(str(self.l), str(self.r))
        return str(self.value)
    
    def __repr__(self):
        return self.__str__()
    
    def postfix(self, fn):
        if self.value == ',':
            self.l.postfix(fn)
            self.r.postfix(fn)
        fn(self)
    
    def __add__(self, o):
        if not isinstance(o, Num):
            raise Exception('Invalid object')
        ast = Num(value=',')
        ast.l = self
        ast.r = o
        self.parent = ast
        o.parent = ast

        ast = reduce(ast)
        ast.set_depth()
        return ast
    
    def magnitude(self):
        if self.value == ',':
            return self.l.magnitude()*3 + self.r.magnitude()*2
        return self.value


def parse(sn):
    op = []
    out = []

    for c in sn:
        if c.isnumeric():
            out.append(int(c))
        elif c == ',':
            while op and op[-1] != '[':
                out.append(op.pop())
            op.append(c)
        elif c == '[':
            op.append(c)
        elif c == ']':
            if not op:
                raise Exception('Unbalanced parenteses[1]')
            while op and op[-1] != '[':
                out.append(op.pop())
            if not op:
                raise Exception('Unbalanced parenteses[2]')
            op.pop()
    
    while op:
        c = op.pop()
        if c == '[':
            raise Exception('Unbalanced parenteses[3]')
        out.append(c)
    
    ast = None
    stack = []
    for t in out:
        if t == ',':
            r = stack.pop()
            l = stack.pop()
            o = Num(',')
            o.r = r
            o.l = l
            r.parent = o
            l.parent = o
            stack.append(o)
        else:
            stack.append(Num(t))
    
    if len(stack) != 1:
        print(stack)
        raise Exception('Invalid syntax for number')
    ast = stack[0]

    ast.set_depth()

    return ast


def as_list(num):
    result = []

    def _visit(n):
        if n.value != ',':
            result.append(n)
    
    num.postfix(_visit)

    return result

def explode(ast):
    ast.set_depth()
    nums = as_list(ast)
    first = None
    last = None

    curr = None
    for i, n in enumerate(nums):
        if n.depth > 4:
            np = n.parent
            if np.l.value == ',' or np.r.value == ',':
                continue
            curr = n
            
            if i+2 < len(nums):
                last = nums[i+2]
            if i > 0:
                first = nums[i-1]
            break
    
    if not curr:
        return (ast, False)
    
    curr = curr.parent
    left_val = curr.l.value
    right_val = curr.r.value
    if curr == curr.parent.l:
        zero = Num(value=0)
        zero.parent = curr.parent
        curr.parent.l = zero
    else:
        zero = Num(value=0)
        zero.parent = curr.parent
        curr.parent.r = zero
    
    if first:
        first.value += left_val
    
    if last:
        last.value += right_val
    
    ast.set_depth()
    return (ast, True)


def split(ast):
    ast.set_depth()
    nums = as_list(ast)
    for n in nums:
        if n.value >= 10:
            o = Num(value=',')
            o.l = Num(value=floor(n.value/2))
            o.r = Num(value=ceil(n.value/2))
            o.l.parent = o
            o.r.parent = o
            o.parent = n.parent
            if n.parent.l == n:
                n.parent.l = o
            else:
                n.parent.r = o
            ast.set_depth()
            return (ast, True)
    return (ast, False)


def reduce(ast):
    while True:
        ast, reduced_e = explode(ast)
        if reduced_e:
            continue
        ast, reduced_s = split(ast)
        if not (reduced_e or reduced_s):
            return ast
    


def part1(numbers):
    numbers = [parse(n) for n in numbers]
    res = numbers[0]
    for o in numbers[1:]:
        res = res + o
    print('Homework Snailfish number is:', res)
    return res.magnitude()


def part2(numbers):
    magnitude = 0
    for x in numbers[0:-1]:
        for y in numbers[1:]:
            sx = parse(x)
            sy = parse(y)
            m = (sx + sy).magnitude()
            #print(x, ' + ', y, '= mag ', magnitude)
            if m >= magnitude:
                magnitude = m
    return magnitude


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))

