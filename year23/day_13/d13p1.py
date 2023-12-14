from colorama import init
from colorama import Fore, Back, Style
init()

def get_lines(fname):
    with open(fname) as f:
        c = f.read()
        ps = c.split("\n\n")

    puzzles = []
    for p in ps:
        grid = p.split("\n")
        puzzles.append(grid)

    return puzzles

def are_same(b_s, a_s):

    for p1,p2 in zip(b_s,a_s):
        if p1 != p2:
            return False
    return True

def are_one_different(b_s, a_s):
    
    ndiffs = 0
    for p1,p2 in zip(b_s,a_s):
        for c1,c2 in zip(p1,p2):
            if c1 != c2:
                ndiffs += 1
    return ndiffs == 1

def is_row_mirror(lines, i_split, isp2=False):
    b_s = []
    a_s = []
    for i,line in enumerate(lines):
        if i < i_split:
            b_s.append(line)
        else:
            a_s.append(line)
    
    b_s = b_s[::-1]

    if not isp2:
        return are_same(b_s, a_s)
    else:
        return are_one_different(b_s, a_s)

def get_row_mirrors(p, isp2=False):
    for i in range(0,len(p)-1):
        row = i+1
        if is_row_mirror(p, row, isp2):
            return row
    return 0
        
def get_transpose(p):
    NI = len(p)
    NJ = len(p[0])

    G = {}
    for i,line in enumerate(p):
        for j,char in enumerate(line):
            G[(i,j)] = char

    tp = []
    # transpose rows and columns
    for j in range(NJ): # ith row 
        row_data = [G[(i,j)] for i in range(NI)]
        row_data = "".join(row_data)
        tp.append(row_data)

    return tp

def print_puzzle(rp, rm, cm):
    print()
    for i,line in enumerate(rp):
        chars = []
        for c in line:
            if c == "#":
                chars.append(Fore.LIGHTBLACK_EX+"\u2588" + Style.RESET_ALL)
            else:
                chars.append(Fore.WHITE+"\u2588"+Style.RESET_ALL)
        if cm >0:
            chars.insert(cm, Fore.RED + "\u2588" + Style.RESET_ALL)
        chars = "".join(chars)
        print(chars)
        if rm > 0 and i+1 == rm:

            chars = ["\u2588" for j in range(len(line))]
            chars = "".join(chars)
            print(Fore.RED + chars + Style.RESET_ALL)

fname = [ "d13_ex.txt", "d13_in.txt"][1]

ps = get_lines(fname)

def solve(ps, ispart2=False):
    allsum = 0
    for rp in ps:
        cp = get_transpose(rp)
        rm = get_row_mirrors(rp, ispart2)
        cm = get_row_mirrors(cp, ispart2)
        allsum += cm + 100*rm
        #print_puzzle(rp, rm, cm)
    return allsum

print(solve(ps, False))
print(solve(ps, True))
