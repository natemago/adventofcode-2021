from math import ceil
def read_input(inpf):
    initial = ''
    rules = {}
    with open(inpf) as f:
        for line in f:
            line = line.strip()
            if '->' in line:
                p = line.split('->')
                rules[p[0].strip()] = p[1].strip()
            elif line:
                initial = line
    return initial, rules

def part1(initial, rules):
    result = initial
    for i in range(0, 10):
        t = ''
        for k in range(0, len(result) - 1):
            t += result[k] + rules[result[k:k+2]]
        t += result[-1]
        result = t

    freq = {}
    for c in result:
        freq[c] = freq.get(c, 0) + 1
    
    pairs = {}
    for i in range(0, len(result) - 1):
        pairs[result[i:i+2]] = pairs.get(result[i:i+2], 0) + 1
    

    return max(freq.values()) -  min(freq.values())


def part2(initial, rules):
    pairs = {}
    for i in range(0, len(initial) - 1):
        pairs[initial[i:i+2]] = pairs.get(initial[i:i+2], 0) + 1
    
    nrules = {}
    for k, v in rules.items():
        nrules[k] = (
            k[0] + v, 
            v + k[1],
            v
        )
    res = None
    for N in range(0, 40):
        res = {}
        interim = {}
        for pair in list(pairs.keys()):
            count = pairs[pair]
            p1, p2, v = nrules[pair]

            if pair == p1 and pair == p2:
                interim[pair] = interim.get(pair, 0) + count #  + count
            elif pair in (p1, p2):
                p = p1 if pair != p1 else p2
                interim[pair] = interim.get(pair, 0) + 0 # no change there
                interim[p] = interim.get(p, 0) + count # add the new pair
            else: # two new pairs
                interim[pair] = interim.get(pair, 0) - count
                interim[p1] = interim.get(p1, 0) + count
                interim[p2] = interim.get(p2, 0) + count
            
        for p, delta in interim.items():
            pairs[p] = pairs.get(p, 0) + delta

       
    freq = {}
    for pair, count in pairs.items():
        if not count:
            continue
        for p in pair:
            freq[p] = freq.get(p, 0) + count
    
    for l, count in list(freq.items()):
        freq[l] = ceil(freq[l]/2)

    return max(freq.values()) -  min(freq.values())


    

print('Part 1:', part1(*read_input('input')))
print('Part 2:', part2(*read_input('input')))