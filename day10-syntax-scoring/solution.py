def read_input(inpf):
    with open(inpf) as f:
        return [l.strip() for l in f.readlines()]


brakets = {
    '{': '}',
    '[': ']',
    '<': '>',
    '(': ')',
    '}': '{',
    ']': '[',
    '>': '<',
    ']': '[',
    ')': '(',
}

score = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

completion_score = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def check(line):
    stack = []
    for i, c in enumerate(line):
        if c in '{[(<':
            stack.append(c)
        elif c in '}])>':
            if stack[-1] != brakets[c]:
                return c, None
            stack.pop()
        else:
            raise Exception('Invalid char: {}'.format(c))

    completion = list(reversed([brakets[c] for c in stack]))

    return None, completion


def part1(lines):
    errors = []
    for line in lines:
        err, _ = check(line)
        if err:
            errors.append(err)
    
    return sum([score[e] for e in errors])


def part2(lines):
    scores = []
    for line in lines:
        error, completion = check(line)
        if error:
            continue
        if completion:
            s = 0
            for c in completion:
                s = s*5 + completion_score[c]
            scores.append(s)
    scores = list(sorted(scores))
    return scores[len(scores)//2]

print('Part 1: ', part1(read_input('input')))
print('Part 2: ', part2(read_input('input')))
