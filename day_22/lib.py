from collections import deque

def get_input(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()

    return lines

def get_header_str(board):
    ostr = ''

    for i,_ in enumerate(board[0]):
        if i%10 == 0:
            if i >= 100:
                i -= 100
            ostr += f'{i//10}'
        else:
            ostr += ' '
    ostr += '\n'
    for i,_ in enumerate(board[0]):
        ostr += f'{i%10}'
    ostr += '\n'

    return ostr

def print_header(board):
    for i,_ in enumerate(board[0]):
        if i%10 == 0:
            if i >= 100:
                i -= 100
            print(f'{i//10}',end='')
        else:
            print(f' ',end='')
    print()
    for i,_ in enumerate(board[0]):
        print(f'{i%10}',end='')
    print()

def write_board(fname, board, posR, posC):
    with open(fname, 'w') as f:

        ostr = get_header_str(board)

        f.write(ostr)

        for r,row in enumerate(board):
            for c,char in enumerate(row):
                if r == posR and c == posC:
                    f.write(f'x')
                else:
                    f.write(f'{char}')
            f.write('\n')

def print_board(board, posR, posC):

    print_header(board)

    for r,row in enumerate(board):
        for c,char in enumerate(row):
            if r == posR and c == posC:
                print(f'x',end='')
            else:
                if abs(r - posR) < 10:
                    print(f'{char}',end='')
        if abs(r - posR) < 10:
            print()

def find_initial_positon(board):

    posR = 0
    posC = 0
    for i,char in enumerate(board[0]):
        if char == '.':
            posC = i
            break

    return posR, posC

def parse_steps(path:str):

    rotations = []

    for char in path:
        if char == 'R':
            rotations.append('R')
        elif char == 'L':
            rotations.append('L')

    path = path.replace('L', '_')
    path = path.replace('R', '_')
    steps = path.split('_')
    steps = [ int(step) for step in steps ]

    return steps, rotations



def find_end_row(board, col):

    end_row = len(board) - 1

    while end_row > 0:
        char = board[end_row][col]
        if char != ' ':
            # we found a nonblank char
            break
        end_row -= 1
    return end_row

def find_start_row(board, col):

    i = 0

    for i, _ in enumerate(board):
        char = board[i][col]
        if char != ' ':
            break

    return i

def find_left_bounds(board, row):

    for i,val in enumerate(board[row]):
        if val != ' ':
            return i

    return len(board[row])-1



def find_right_bounds(board, row):

    icol = len(board[row])-1

    while icol >= 0:

        char = board[row][icol]
        if char != ' ':
            break
        icol -= 1
    return icol



def get_nbr_n(board, r, c):

    if r-1 < 0:
        n = find_end_row(board, c)
        return n

    val = board[r-1][c]
    if val == ' ':
       n = find_end_row(board, c)
    else:
       # ok to move up
       n = r - 1

    return n

def get_nbr_s(board, r, c):

    if r+1 == len(board):
        s = find_start_row(board, c)
        return s

    s = r+1
    val = board[s][c]

    if val == ' ':
        s = find_start_row(board, c)

    return s

def get_nbr_w(board, r, c):

    if c-1 < 0:
        w = find_right_bounds(board, r)
        return w

    w = c - 1
    val = board[r][w]
    if val == ' ':
        w = find_right_bounds(board, r)

    return w

def get_nbr_e(board, r, c):

    e = c + 1

    if e > len(board[r])-1:
        e = find_left_bounds(board, r)
        return e

    val = board[r][e]
    if val == ' ':
        e = find_left_bounds(board, r)

    return e

def get_grid_limits(board):

    limits = {}

    for r,row in enumerate(board):
        for c,_ in enumerate(row):

            n = get_nbr_n(board, r, c)
            e = get_nbr_e(board, r, c)
            w = get_nbr_w(board, r, c)
            s = get_nbr_s(board, r, c)

            limits[(r,c)] = (n, s, e, w)

    return limits


def mk_grid(board):

    NC_max = 0
    for row in board:
        NC_max = max(NC_max, len(row))

    NR = len(board)
    NC = NC_max

    grid = []
    for _ in range(NR):
        grid.append([ ' ' for _ in range(NC) ])

    for irow, row in enumerate(board):
        for icol, col in enumerate(row):
            grid[irow][icol] = col

    return grid


def step_fwd(facing, posR, posC, limits):

    r,c = posR, posC

    n,s,e,w = limits[(posR,posC)]

    if   facing == 'N':
        r = n
    elif facing == 'S':
        r = s
    elif facing == 'E':
        c = e
    elif facing == 'W':
        c = w

    return r,c

def step_cube(irow, icol, facing):
    r = irow
    c = icol
    f = facing

    if   facing == 'N':
        r -= 1
    elif facing == 'S':
        r += 1
    elif facing == 'E':
        c += 1
    elif facing == 'W':
        c -= 1

    if facing == 'N' and irow == 0 and icol in range(50,100):
        r = icol + 100
        c = 0
        f = 'E'
    elif facing == 'W' and icol == 0 and irow in range(150,200):
        r = 0
        c = irow - 100
        f = 'S'
    elif facing == 'W' and icol == 50 and irow in range(0, 50):
        r = 149 - irow
        c = 0
        f = 'E'
    elif facing == 'W' and icol == 0 and irow in range(100, 150):
        r = 149 - irow
        c = 50
        f = 'E'
    elif facing == 'N' and irow == 100 and icol in range(0, 50):
        r = icol + 50
        c = 50
        f = 'E'
    elif facing == 'W' and icol == 50 and irow in range(50, 100):
        r = 100
        c = irow - 50
        f = 'S'
    elif facing == 'E' and icol == 99 and irow in range(50, 100):
        r = 49
        c = irow + 50
        f = 'N'
    elif facing == 'S' and irow ==  49 and icol in range(100, 150):
        c = 99
        r = icol - 50
        f = 'W'
    elif facing == 'E' and icol == 149 and irow in range(  0,  50):
        c = 99
        r = 149 - irow
        f = 'W'
    elif facing == 'E' and icol ==  99 and irow in range(100, 150):
        c = 149
        r = 149 - irow
        f = 'W'
    elif facing == 'N' and irow ==   0 and icol in range(100, 150):
        r = 199
        c = icol - 100
        f = 'N'
    elif facing == 'S' and irow == 199 and icol in range(  0,  50):
        r = 0
        c = icol + 100
        f = 'S'
    elif facing == 'E' and icol ==  49 and irow in range(150, 200):
        r = 149
        c = irow - 100
        f = 'N'
    elif facing == 'S' and irow == 149 and icol in range( 50, 100):
        c = 49
        r = icol + 100
        f = 'W'

    return r,c,f



def rotate(facing:str, rotations:deque[str]):

    if len(rotations) == 0:
        return facing

    direction = rotations.popleft()

    newfacing = {
        ("N", "L") : 'W',
        ("N", "R") : 'E',
        ("E", "L") : 'N',
        ("E", "R") : 'S',
        ("S", "L") : 'E',
        ("S", "R") : 'W',
        ("W", "L") : 'S',
        ("W", "R") : 'N',
    }

    return newfacing[(facing,direction)]








