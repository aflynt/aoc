from collections import deque
from lib import *

#fname = 'ex.dat'
fname = 'input.dat'

lines = get_input(fname)

path  = lines[-1].strip('\n')
board = [ line.strip('\n') for line in lines[:-2] ]
grid = mk_grid(board)

posR, posC = find_initial_positon(board)
steps, rotations = parse_steps(path)
rotations = deque(rotations)
facing = 'E'

for step in steps:

    for i in range(step):

        newR, newC, newF = step_cube(posR, posC, facing)

        newChar = grid[newR][newC]
        if newChar == '#':
            break
        else:
            posR, posC, facing = newR, newC, newF
            #print(f'{i+1}/{step} steps  r,c,f: {newR},{newC},{facing}')

        #print_board(grid, posR, posC)
        #write_board('o.dat', grid, posR, posC)

        #_ = input('?')
    facing = rotate(facing, rotations)
    #print(f'rotate to face: {facing}')

face_val = 3
if facing == 'E':
    face_val = 0
elif facing == 'S':
    face_val = 1
elif facing == 'W':
    face_val = 2

print(f'final facing = {facing}, face_val = {face_val}')
print(f'final rowval = {posR+1}, row_val  = {1000*(posR+1)}')
print(f'final colval = {posC+1}, row_val  = {   4*(posC+1)}')

pss = face_val + 1000*(posR+1) + 4*(posC+1)
print(f'pss = {pss}')