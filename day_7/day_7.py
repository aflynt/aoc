from aoc_lib import *
import os


class file:
    def __init__(self, name, size):
        self.name = name
        self.size = size

class dir_:
    def __init__(self, name:str, files:list[file], subdirs:list):
        self.name = name
        self.files = files
        self.subdirs = subdirs
    def __str__(self):
        fstr = ','.join(self.files)
        fstr = '[' + fstr + ']'
        dstr = ','.join(self.subdirs)
        dstr = '[' + dstr + ']'
        return f'{self.name}: fs: {fstr} ds: {dstr}'

    def get_subdir_names(self) -> list[str]:
        names = [d.name for d in self.subdirs]
        return names

    def get_subdir(self, dirname):
        sdnames = self.get_subdir_names()
        sdirs = self.subdirs

        for name, sd in zip(sdnames, sdirs):
            if name == dirname:
                return sd
        



def get_next_command(line:str):

    type = 'cd'

    if line.startswith('$ cd'):
        cd_dest = line.split()[-1].strip()
    else: # ls
        type = 'ls'
        cd_dest = '.'
    
    return (type, cd_dest)


def kid_in_subdir_list(subdirs:list[str], kid:str):
    if kid in subdirs:
        return True
    return False

def point_to_kid(kidname:str, r:dir_, p:dir_, c:dir_):
    p = c
    c = c.get_subdir(kidname)
    return c

def process_cd(dest, r, p, c:dir_):

    cur_name = c.name
    subdirs  = c.subdirs
    subdirnames = c.get_subdir_names()
    parent = p

    if dest == '..':
        # go to parent directory
        print('going back up')
        c = p
        return p 

    if dest == '/':
        # go to parent directory
        print('going to root')
        c = r
        p = r
        return r

    # got here so cd to a child
    
    # A) kid is     in my subdir list
    if kid_in_subdir_list(subdirnames, dest):
        c = point_to_kid(dest, r,p,c)
    # B) kid is not in my subdir list
    #elif dest not in c.subdirs():
        pass
        # cd to new sub directory, so add it as key
        #c[dest] = {}
        #print(f'cd to {dest}')
        #return c[dest]

def process_cmd(type,dest, lines, r:dir_, p:dir_, c:dir_):

    print(f"cmd_type = {type}, dest = {dest}")
    print(f'r: {r}')
    print(f'p: {p}')
    print(f'c: {c}')
    print(f'line0 = {lines[0]}')

    if type == 'cd':
        process_cd(dest, r, p, c)

    else: # ls
        pass

def print_lines(lines, ic):

    for i, line in enumerate(lines):

        ic_str = ''
        if ic == i:
            ic_str = f'<---------------------- {ic}'
        print(f'{i:2d} : {line} {ic_str}')


def change_dir(r:dir_, p:list, c:dir_, dest:str):

    if dest == '/':
        p = []
        c = r
    elif dest == '..':
        # cwd = root -> no change
        # p = [r]
        if len(p) == 0:
            # at root, dont back up
            c = r
        else :
            # multi dirs in parent_list
            # p = [r, d0, d1 , d2]
            c = p.pop()

    else: # cd to subdir
        # find target subdir
        for subdir in c.subdirs:
            if subdir.name == dest:
                # found matching subdir

                # push cwd
                p.append(c)

                # change cwd
                c = subdir
                break
        

def read_listing(r:dir_,p:list,c:dir_,ic:int, lines:list[str]):

    good_lines = lines[ic:]

    for line in good_lines:
        if line.startswith('$'):
            # done we reached the next command
            break
        elif line.startswith('dir'):
            # found a subdir
            # add it to our cwd list of subdirs
            subdirlist = c.subdirs

            dirname = line.split()[-1]

            subdirnames = [ dir.name for dir in subdirlist]

            if dirname not in subdirnames:
                subdirlist.append(dir_(dirname, [], []))
        else:
            # found a file
            fsize,fname = line.split()
            f = file(fname, fsize)

            # add to list of files
            c.files.append(f)

        ic += 1
        
    return ic


def solve(fname, r,p,c):
    data = read_input(fname)

    lines = data.splitlines()
    nlines = len(lines)

    ic = 0  # instruction counter

    print_lines(lines, ic)


    while (ic < nlines):

        line = lines[ic]

        cmd_type,dest = get_next_command(line)
        ic+=1

        print(f'cmd_type = {cmd_type}')
        if cmd_type == 'cd':
            change_dir(r, p, c, dest)
        else: # ls
            ic = read_listing(r,p,c, ic, lines)
        # cd, dest
        # ls, .

    #c = process_cmd(cmd_type, cmd_dest, lines, r,p,c)

    #print(type, dest)
    #print(tree)
    ## get next line
    #cmd = lines[0]

    #print(f'cmd = {cmd}')



    

os.chdir('day_7')
cwd = current_path() + '\\'

r = dir_("/", [], [])

p = []
c = r

fname = 'input_real.txt'
fname = 'input_test.txt'

n1 = solve(cwd+fname,  r, p, c)
#n2 = solve(cwd+fname, 14)

