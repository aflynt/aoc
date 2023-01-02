from collections import deque

offsets = {
        #     r   c
        'N' : (-1, 0),
        'S' : ( 1, 0),
        'E' : ( 0, 1),
        'W' : ( 0,-1),
        'NE': (-1, 1),
        'NW': (-1,-1),
        'SE': ( 1, 1),
        'SW': ( 1,-1),
        }


class elf:
    def __init__(self, r,c, id_):
        self.r = r
        self.c = c
        self.id = id_
        #self.dirs = deque(['N', 'S', 'E', 'W'])
        self.dirs = deque(['N', 'E', 'S', 'W'])

    def set_pos(self, pos_pair):
        self.r = pos_pair[0]
        self.c = pos_pair[1]

    def help_check_one_dir(self, dir, grid):

        r = self.r
        c = self.c
        loc_n  = grid[r+offsets['N' ][0]][c+offsets['N' ][1]]
        loc_s  = grid[r+offsets['S' ][0]][c+offsets['S' ][1]]
        loc_e  = grid[r+offsets['E' ][0]][c+offsets['E' ][1]]
        loc_w  = grid[r+offsets['W' ][0]][c+offsets['W' ][1]]
        loc_ne = grid[r+offsets['NE'][0]][c+offsets['NE'][1]]
        loc_se = grid[r+offsets['SE'][0]][c+offsets['SE'][1]]
        loc_nw = grid[r+offsets['NW'][0]][c+offsets['NW'][1]]
        loc_sw = grid[r+offsets['SW'][0]][c+offsets['SW'][1]]

        # north locations
        locs = [loc_n, loc_ne, loc_nw]

        if   dir == 'S': locs = [loc_s, loc_se, loc_sw]
        elif dir == 'E': locs = [loc_e, loc_ne, loc_se]
        elif dir == 'W': locs = [loc_w, loc_sw, loc_nw]

        open_list = [ loc == '.' for loc in locs]
        all_open = all(open_list)
        #print(f'all open? {all_open} for {open_list}')

        if all_open:
            return True
        else:
            return False


    def get_valid_dir(self, grid):
        dirs = self.dirs
        dir = dirs[0]

        for dir in dirs:
            mv_ok = self.help_check_one_dir(dir, grid)
            #print(f'dir = {dir} ok ? = {mv_ok}')
            if mv_ok:
                break

        self.dirs.rotate(-1)

        r = self.r
        c = self.c

        return (r+offsets[dir][0], c+offsets[dir][1])

    def check_one(self, grid):

        # consider 8 locations around me
        r = self.r
        c = self.c
        loc_n  = grid[r+offsets['N'][0]][c+offsets['N'][1]]
        loc_s  = grid[r+offsets['S'][0]][c+offsets['S'][1]]
        loc_e  = grid[r+offsets['E'][0]][c+offsets['E'][1]]
        loc_w  = grid[r+offsets['W'][0]][c+offsets['W'][1]]
        loc_ne = grid[r+offsets['NE'][0]][c+offsets['NE'][1]]
        loc_se = grid[r+offsets['SE'][0]][c+offsets['SE'][1]]
        loc_nw = grid[r+offsets['NW'][0]][c+offsets['NW'][1]]
        loc_sw = grid[r+offsets['SW'][0]][c+offsets['SW'][1]]

        nbrs = [ loc_n  ,loc_s  ,loc_e  ,loc_w  ,loc_ne ,loc_se ,loc_nw ,loc_sw , ]

        nbrs = [nbr for nbr in nbrs if nbr == '#']

        if len(nbrs) == 0:
            #print(f'nobody around: dont move')
            # no neighbors, return same position
            return  (r,c)

        # propose moving one step in the first valid direction:
        newr,newc = self.get_valid_dir(grid)
        #print(f'proposed dir = {(newr,newc)}')
        return (newr,newc)







def read_file(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()
    lines = [line.strip('\n') for line in lines]
    return lines

def extend_grid(grid):
    nr = len(grid)
    nc = len(grid[0])
    newgrid = []

    for i in range(nr*3):
        rowchars = []
        for j in range(nc*3):
            rowchars.append('.')
        newgrid.append(rowchars)

    for i in range(nr):
        irow = i + nr
        for j in range(nc):
            jcol = j + nc
            val = grid[i][j]
            newgrid[irow][jcol] = val

    return newgrid

def update_grid(grid, elves):

    # clear grid
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = '.'

    # write new elf positions
    for e in elves:
        grid[e.r][e.c] = '#'

def print_grid(grid):

    for _,row in enumerate(grid):
        for _,char in enumerate(row):
            print(f'{char}', end='')
        print()

def find_elves(grid):
    elves = []

    id_ = 0

    for i,row in enumerate(grid):
        for j,char in enumerate(row):
            if char == '#':
                elves.append(elf(i, j, id_))
                id_ += 1
    return elves

def update_proposed_dirs(elf_mvs:dict[tuple[int,int], int], prop_pos:tuple[int,int], e:elf):
    if (prop_pos) in elf_mvs:
        del elf_mvs[(prop_pos)]
    else:
        elf_mvs[(prop_pos)] = e

def get_move_proposals(grid, elves):
    elf_mvs = {}

    for e in elves:
        prop_pos = e.check_one(grid)
        update_proposed_dirs(elf_mvs, prop_pos, e)

    return elf_mvs

def move_elves(elf_mvs, elves, grid):
    for pos,e in elf_mvs.items():
        #print(f'pos = {pos} for e = {e} at {e.r}, {e.c}')
        e.set_pos(pos)
        #print(f'pos = {pos} for e = {e} at {e.r}, {e.c}')

    update_grid(grid, elves)

###############################################################

def get_limits(E):
    rmin = min([r for r,c in E])
    rmax = max([r for r,c in E])
    cmin = min([c for r,c in E])
    cmax = max([c for r,c in E])
    return rmin,rmax,cmin,cmax

def new_print_grid(E:set[(int,int)]):
    rmin,rmax,cmin,cmax = get_limits(E)

    for r in range(rmin,rmax+1):
        for c in range(cmin, cmax+1):
            char = '#' if (r,c) in E else '.'
            print(char, end='')
        print()

def gather_elves(lines):
    E = set()
    for r,row in enumerate(lines):
        for c,char in enumerate(row):
            if char == '#':
                E.add((r,c))
    return E

###############################################################


fname = 'ex.dat'
fname = 'ex2.dat'

lines = read_file(fname)
E = gather_elves(lines)



#elves = find_elves(grid)
#
#elf_mvs = {}
#
#for round in range(1,10+1):
#    print(f'=============================== ROUND: {round}')
#    elf_mvs.clear()
#    elf_mvs = get_move_proposals(grid, elves)
#    move_elves(elf_mvs, elves, grid)
#    print_grid(grid)

