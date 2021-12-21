def part1(p1, p2):
    p1_score = 0
    p2_score = 0

    i = 0

    while True:
        tot = (i% 1000) + 1 + ((i+1)% 1000) + 1 + ((i+2)% 1000) + 1
        p1 = (p1 - 1 + tot) % 10 + 1
        p1_score += p1
        i += 3
        if p1_score >= 1000:
            break
        
        tot = (i% 1000) + 1 + ((i+1)% 1000) + 1 + ((i+2)% 1000) + 1
        p2 = (p2 - 1 + tot) % 10 + 1
        p2_score += p2
        i += 3
        if p2_score >= 1000:
            break
        
    losing_score = p1_score if p1_score < p2_score else p2_score
    return losing_score * i

print('Part 1:', part1(8, 10))

sums = {}
for i in range(3):
    for j in range(3):
        for k in range(3):
            k = (i+1, j+1, k+1)
            s = sum(k)
            sums[s] = sums.get(s, 0) + 1

from itertools import product
from functools import cache


@cache
def roll(p1, p1_score, p2, p2_score, target):
    p1_wins = 0
    p2_wins = 0
    for r1 in product((1,2,3), repeat=3):
        s = sum(r1)
        cp1 = (p1-1+s)%10 + 1
        cp1_score = p1_score + cp1
        if cp1_score >= target:
            p1_wins += 1
            continue
        for r2 in product((1,2,3), repeat=3):
            s2 = sum(r2)
            cp2 = (p2 - 1 + s2) % 10 + 1
            cp2_score = p2_score + cp2
            if cp2_score >= target:
                p2_wins += 1
                continue
            p1w, p2w = roll(cp1, cp1_score, cp2, cp2_score, target)
            p1_wins += p1w
            p2_wins += p2w
    return p1_wins, p2_wins
            
def part2(p1, p2):
    return max(roll(p1, 0, p2, 0, 21))
    
print('Part 2:', part2(8, 10))
        
