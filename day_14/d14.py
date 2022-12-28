import copy
import matplotlib.pyplot as plt

def get_lines(fname):
    lines = []

    with open(fname, 'r') as f:
        lines = f.readlines()
    
    lines = [ line.strip() for line in lines]
    return lines

#def get_rocks(lines:list[str]):
def get_rocks(lines):
    rock_lines = []
    for line in lines:
        xys = line.split(' -> ')
        xys = [xy.split(',') for xy in xys]
        xys = [(int(x),int(y)) for x,y in xys]
        
        rock_lines.append(xys)
    
    return rock_lines


def get_extents(rock_lines):

    x0 =  10000000000
    x1 = -10000000000
    y1 = -10000000000

    for line in rock_lines:
        # list of xys
    
        npoints = len(line)
    
        for i in range(npoints - 1):
            dest = line[i+1]
            orig = line[i]

            dx,dy = dest[0], dest[1]
            ox,oy = orig[0], orig[1]

            x0 = min(x0, dx, ox)
            x1 = max(x1, dx, ox)
            y1 = max(y1, dy, oy)
    return x0,x1,y1

def make_grid(nx,ny, char='.'):
    grid = []
    for j in range(ny):
        row = []
        for i in range(nx):
            row.append(char)
        grid.append(row)

    return grid

def write_grid(grid, fname='out.dat'):
    nx = len(grid[0])
    ny = len(grid)

    lines = []

    for j in range(ny):
        linestr = f'{j:>3d} '
        for i in range(nx):
            linestr += grid[j][i]
        linestr += '\n'
        lines.append(linestr)

    with open(fname, 'w') as f:
        f.writelines(lines)


def print_grid(grid):
    nx = len(grid[0])
    ny = len(grid)

    for j in range(ny):
        print(f'{j:>3d} ',end='')
        for i in range(nx):
            print(grid[j][i], end='')
        print()
    return

def get_rock_coords(rock_lines):

    rock_coords = []

    for line in rock_lines:
        # list of xys
    
        npoints = len(line)
    
        for i in range(npoints - 1):
            dest = line[i+1]
            orig = line[i]

            dx,dy = dest[0], dest[1]
            ox,oy = orig[0], orig[1]

            if dx == ox: # x is not changing -> same col
                ys = [y for y in range(min(oy,dy), max(oy,dy)+1)]
                xs = [ox for _ in range(len(ys))]
            if dy == oy: # y is not changing -> same row
                xs = [x for x in range(min(ox,dx), max(ox,dx)+1)]
                ys = [oy for _ in range(len(xs))]
            
            for x,y in zip(xs,ys):
                rock_coords.append((x,y))

    return rock_coords


#def draw_char(xy_pair:tuple[int,int], char:str, grid:list[list[str]], xref:int):
def draw_char(xy_pair, char, grid, xref):

    # get x,y coords
    x,y = xy_pair

    # shift x coord
    x = x - xref

    grid[y][x] = char


def get_char(x,y, grid,xref):
    # shift x coord
    x = x - xref
    if x >=0 and x < len(grid[0]) and y >= 0 and y < len(grid):
        return grid[y][x]
    else:
        return '.'

def drop_sand(sand_coord, grid,xref):

    x,y = sand_coord
    done = False
    
    while not done:
        # check char below

        if get_char(x,y+1,grid, xref) == '.':
            # ok can proceed
            y += 1
        
        elif get_char(x-1, y+1, grid, xref) == '.':
            # ok move diag L
            x -= 1
            y += 1
            if y == len(grid) - 1:
                done = True
        
        elif get_char(x+1, y+1, grid, xref) == '.':
            # ok move diag R
            x += 1
            y += 1
            if y == len(grid) - 1:
                done = True
        else:
            # we are stuck. stop and return
            draw_char((x,y), 'o', grid, xref)
            done = True

#########################################
#lines = get_lines('example.txt')
lines = get_lines('real.txt')

rock_lines = get_rocks(lines)
xref,xmax,ymax = get_extents(rock_lines)
print(f'x min = {xref}, x max = {xmax} ymax = {ymax}')

# part 2
xref -= ymax+5
xmax += ymax+5
ymax += 2

nx = xmax - xref + 1
ny = ymax + 1


rock_char = '#'
air_char  = '.'
sand_src_char = '+'
sand_dest_char = 'o'

sand_orig_xy = (500, 0)

rock_coords = get_rock_coords(rock_lines)

x = xref
while x <= xmax:
    rock_coords.append((x,ymax))
    x +=1

fig, ax = plt.subplots()

grid = make_grid(nx, ny)

draw_char(sand_orig_xy, sand_src_char, grid, xref)

for rc in rock_coords:
    draw_char(rc, rock_char, grid, xref)

print_grid(grid)



n_units = 0
done = False
while not done:
    old_grid = copy.deepcopy(grid)

    # drop_sand
    drop_sand(sand_orig_xy, grid, xref)
    n_units += 1

    #print_grid(grid)
    #write_grid(grid)
    print(n_units)
    #resp = input(f'n = {n_units:>2d} continue y,n?')

    ## stop if grid is unchanged
    #if old_grid == grid or resp.startswith('n'):
    if old_grid == grid:
        done = True

    
print(f'n = {n_units-1}')
print_grid(grid)
