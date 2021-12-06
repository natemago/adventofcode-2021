def read_input(inpf):
    numbers = []
    boards = []

    with open(inpf) as f:
        numbers = [int(n) for n in f.readline().strip().split(',')]
        f.readline()

        lines = f.readlines()

        while lines:
            board = lines[0:5]
            lines = lines[6:]
            board = [
                [int(n) for n in row.strip().split()] for row in board
            ]
            boards.append(board)

    return numbers, boards


def check_if_complete(board):
    for row in board:
        if ''.join([str(n) for n in row]) == 'xxxxx':
            return True
    
    for i in range(0, 5):
        r = ''
        for j in range(0, 5):
            r += str(board[j][i])
        if r == 'xxxxx':
            return True
    return False


def part1(numbers, boards):
    for n in numbers:
        for board in boards:
            for row in board:
                for i in range(0, 5):
                    if row[i] == n:
                        row[i] = 'x'
            if check_if_complete(board):
                s = 0
                for row in board:
                    for c in row:
                        if c != 'x':
                            s += c
                return s * n


def part2(numbers, boards):
    result = -1
    completed = set()
    for n in numbers:
        for idx, board in enumerate(boards):
            if idx in completed:
                continue
            for row in board:
                for i in range(0, 5):
                    if row[i] == n:
                        row[i] = 'x'
            if check_if_complete(board):
                s = 0
                for row in board:
                    for c in row:
                        if c != 'x':
                            s += c
                result = s * n
                completed.add(idx)
    return result


numbers, boards = read_input('input')
print('Part 1: ', part1(numbers, boards))

numbers, boards = read_input('input')
print('Part 2: ', part2(numbers, boards))
