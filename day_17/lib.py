from collections import deque
from itertools import cycle
from copy import copy

class rock:
            
    def __init__(self, type:str , i=0, j=0):
        self.type = type
        self.i = i
        self.j = j

        if self.type == '-':
            self.shape = [
                #0123
                '####',
            ]
            self.solids = [(0,0),(1,0),(2,0),(3,0)]
            self.NI = 4
            self.NJ = 1
        elif self.type == '+':
            self.shape = [
                #0123
                '.#.',
                '###',
                '.#.',
            ]
            self.solids= [(1,0),(0,1),(1,1),(2,1),(1,2)]
            self.NI = 3
            self.NJ = 3
        elif self.type == 'J':
            self.shape = [
                #0123
                '..#',
                '..#',
                '###',
            ]
            self.solids = [(2,0),(2,1),(0,2),(1,2),(2,2)]
            self.NI = 3
            self.NJ = 3
        elif self.type == 'I':
            self.shape = [
                '#',
                '#',
                '#',
                '#',
            ]
            self.solids = [(0,0) ,(0,1) ,(0,2) ,(0,3)]
            self.NI = 1
            self.NJ = 4
        else:  #self.type == 'O':
            self.shape = [
                '##',
                '##',
            ]
            self.solids = [(0,0),(1,0),(0,1),(1,1)]
            self.NI = 2
            self.NJ = 2
    def __str__(self):
        return '\n'.join(self.shape)
    def __repr__(self):
        return f'rock({self.type})'


class chamber:
    def __init__(self, jet_cycle):
        self.NI = 9
        init_NJ = 1
        self.HGRID = 1
        self.grid = deque([ self.mk_empty_row() for _ in range(init_NJ)])
        self.jet_cycle = jet_cycle
        self.seen = set()

        # change floor
        for i in range(self.NI):
            self.grid[init_NJ-1][i] = '-'
        self.grid[init_NJ-1][0] = '+'
        self.grid[init_NJ-1][self.NI-1] = '+'

        self.my_rock = rock('-')

    def plot_file(self, f):
        f.write('\n')
        for j in range(min( len(self.grid), 30)):
            pstr = f'{j:>3d} '
            f.write(pstr)
            for i in range(self.NI):
                f.write(self.grid[j][i])
            f.write('\n')
                    
    def plot(self, f=None):
        if f:
            self.plot_file(f)

        print()
        for j in range(min( len(self.grid), 30)):
            print(f'{j:>3d} ', end='')
            for i in range(self.NI):
                print(self.grid[j][i], end='')
            print()

    def mk_empty_row(self):
        row = ['.' for _ in range(self.NI)]

        row[        0] = '|'
        row[self.NI-1] = '|'

        return row

    def write_rock(self, r:rock, char:str='@'):
        
        for si,sj in r.solids:
            si += r.i
            sj += r.j
            self.grid[sj][si] = char
    
    def add_rock(self, r:rock):
        # reserve newNJ amount at the top
        self.my_rock = r

        # insert new empty rows
        for j in range(r.NJ+3):
            erow = self.mk_empty_row()
            self.grid.insert(0,erow)

        # shift rock coords to local coords
        r.i = 3
        r.j = 0

        # write solids to grid
        for si,sj in r.solids:
            si += r.i
            sj += r.j

            self.grid[sj][si] = '@'

    def hit_something(self, r:rock):

        good_chars = ['.', '@']

        for si,sj in r.solids:
            gi = r.i + si
            gj = r.j + sj
            grid_char = self.grid[gj][gi]
            if grid_char not in good_chars:
                return True

        return False


    def move_rock(self, jet_char:str):
        newrock = copy(self.my_rock)
        if jet_char == '>':
            newrock.i += 1
        elif jet_char == '<':
            newrock.i -= 1
        else:
            newrock.j += 1

        hit = self.hit_something(newrock)

        if hit and jet_char not in ['<', '>']:
            self.write_rock(self.my_rock, '#')
            
        elif not hit:
            # ok, we can move
            self.write_rock(self.my_rock, '.')
            self.my_rock = newrock
            self.write_rock(self.my_rock, '@')

        return not hit

    def get_top_str(self):
        NJ = min(len(self.grid), 10)
        top_str = ''
        for j in range(NJ):
            for i in range(len(self.grid[0])):
                char = self.grid[j][i]
                top_str += char

        return top_str

    def drop_rock(self, f, do_plot=False):

        mv_ok = True
        #self.plot()
        
        while mv_ok:
            
            jet_char = next(self.jet_cycle)

            #print(f'blow {jet_char}')
            self.move_rock(jet_char)

            #self.plot()

            mv_ok = self.move_rock('v')

            #self.plot()

        self.record_grid_height()

        if do_plot:
            self.plot(f)

        # store state
        seen = False
        if len(self.grid) < 100:
            return False
        else:
            top_str = self.get_top_str()
            cur_state = (jet_char, self.my_rock.type, self.my_rock.i, self.my_rock.j, top_str)

            if cur_state in self.seen:
                seen = True

            self.seen.add(cur_state)

        f.write(f'{cur_state}')
        print(cur_state)

        return seen


    def record_grid_height(self):

        POS_END = len(self.grid)
        POS_ROCK = self.my_rock.j

        dH = POS_END - POS_ROCK

        self.HGRID = max(dH, self.HGRID)

        # remove top rows from 0 to rock's j position
        curH = len(self.grid)

        while curH > self.HGRID:
            self.grid.popleft()
            self.my_rock.j -= 1
            curH = len(self.grid)
        


            

def get_data(fname):
    
    with open(fname, 'r') as f:
        line = f.readline()
    return line