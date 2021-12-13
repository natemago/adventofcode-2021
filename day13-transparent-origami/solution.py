def read_input(inpf):
    points = []
    folds = []

    with open(inpf) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('fold along'):
                p = line[len('fold along '):].split('=')
                axis = p[0].strip()
                value = int(p[1].strip())
                folds.append((axis, value))
            else:
                p = line.split(',')
                points.append((
                    int(p[0].strip()),
                    int(p[1].strip()),
                ))
    return points, folds


def fold(paper, axis, value):
    if axis == 'x':
        return fold_left(paper, value)
    return fold_up(paper, value)


def fold_left(paper, value):
    result = []

    for row in paper:
        a = list(reversed(row[:value]))
        b = row[value+1:]

        for i, v in enumerate(b):
            if i < len(a):
                a[i] = a[i] | v
            else:
                a.append(v)
            
        result.append(list(reversed(a)))

    return result

def fold_up(paper, value):

    a = list(reversed(paper[0: value]))
    b = paper[value+1:]

    for i, row in enumerate(b):
        if i < len(a):
            for j, v in enumerate(row):
                a[i][j] = a[i][j] | v
        else:
            a.append(row)
    

    return list(reversed(a))


def get_paper(points):
    minx = min(points, key=lambda p: p[0])[0]
    maxx = max(points, key=lambda p: p[0])[0]
    miny = min(points, key=lambda p: p[1])[1]
    maxy = max(points, key=lambda p: p[1])[1]

    rows = maxy - miny + 1
    cols = maxx - minx + 1

    paper = [[0 for x in range(0, cols)] for y in range(0, rows)]

    for x, y in points:
        paper[y-miny][x-minx] = 1

    return paper


def print_paper(paper):
    for row in paper:
        for c in row:
            if c:
                print('#', end='')
            else:
                print('.', end='')
        print()
    

def part1(points, folds):
    paper = get_paper(points)
    axis, value = folds[0]
    paper = fold(paper, axis, value)

    return sum([sum(row) for row in paper])
    

def part2(points, folds):
    paper = get_paper(points)

    for axis, value in folds:
        paper = fold(paper, axis, value)
    
    print('Folded manual:')
    print_paper(paper)

print('Part 1: ', part1(*read_input('input')))
part2(*read_input('input'))