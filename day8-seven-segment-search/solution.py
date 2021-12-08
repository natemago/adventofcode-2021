def read_input(inpf):
    patterns = []
    with open(inpf) as f:
        for line in f:
            parts = line.strip().split('|')
            patterns.append((
                parts[0].strip().split(),
                parts[1].strip().split(),
            ))
    return patterns


def part1(patterns):
    lines_with_8 = 0
    count = 0
    for inputs, outputs in patterns:
        has8 = False
        for p in  outputs:
            if len(p) in [2, 3, 4, 7]:
                count += 1
        
        for p in inputs + outputs:
            if len(p) == 7:
                has8 = True
        if has8:
            lines_with_8 += 1
    print('Lines with 8:', lines_with_8)
    print('Total lines: ', len(patterns))
    return count


'''
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

   5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
'''
DIGITS = {
    'abcefg': 0,
    'cf': 1,
    'acdeg': 2,
    'acdfg': 3,
    'bcdf': 4,
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7,
    'abcdefg': 8,
    'abcdfg': 9,
}

def translate(digit, tr):
    r = ''
    for c in digit:
        r += tr[c]
    return ''.join(sorted(r))

def is_valid_combo(digits, tr):
    for d in digits:
        t = translate(d, tr)
        if t not in DIGITS:
            return False
    return True

def decode_digit(d, tr):
    return DIGITS[translate(d, tr)]

def decode(inputs, outputs):
    from itertools import permutations

    digits = inputs + outputs

    for combo in permutations(['a', 'b', 'c', 'd', 'e', 'f', 'g']):
        tr = {}
        for i, c in enumerate(combo):
            tr[c] = 'abcdefg'[i]
        if is_valid_combo(digits, tr):
            return (
                [decode_digit(d, tr) for d in inputs],
                [decode_digit(d, tr) for d in outputs],
            )
    
    raise Exception('Oh no! :O')

def part2(patterns):
    total = 0
    for inputs, outputs in patterns:
        dec_inps, dec_outs = decode(inputs, outputs)
        a,b,c,d = dec_outs
        total += 1000*a + 100*b + 10*c + d
    return total

print('Part 1: ', part1(read_input('input')))
print('Part 2: ', part2(read_input('input')))
