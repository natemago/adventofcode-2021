from functools import reduce
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


def fold(points, axis, value):
    axis = 'xy'.index(axis)
    points = set(points)
    
    def translate(a, x):
        ''' Fold a over x
        '''
        return 2*x - a
    
    res = set(filter(lambda p: p[axis] < value, points))
    gtv = filter(lambda p: p[axis] > value, points)
    return reduce(
        lambda p, a: p.union(
            {(a[0], translate(a[1], value))} if axis else {(translate(a[0], value), a[1])}
        ),
        gtv,
        res,
    )
        
def print_paper(points):
    minx = min(points, key=lambda p: p[0])[0]
    maxx = max(points, key=lambda p: p[0])[0]
    miny = min(points, key=lambda p: p[1])[1]
    maxy = max(points, key=lambda p: p[1])[1]

    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            if (x, y) in points:
                print('#', end='')
            else:
                print('.', end='')
        print()


def part1(points, folds):
    axis, value = folds[0]
    return len(fold(points, axis, value))

def part2(points, folds):
    for axis, value in folds:
        points = fold(points, axis, value)
    print_paper(points)


print('Part 1: ', part1(*read_input('input')))
print('Part 2:')
part2(*read_input('input'))