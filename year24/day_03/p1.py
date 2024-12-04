import re
from typing import List
from itertools import accumulate

def print_nums(mem):
    # print a list of numbers 
    for i in range(0,80):
        if i%10 == 0:
            pstr = "_"
        else:
            pstr = f"{i%10:d}"
        print(pstr, end="")
    print()

def get_input(fname):
    lines = open(fname, "r").read().strip("\n").split("\n")
    return lines

def pop_front(vec:List):
    head = vec[0]
    newvec  = vec[1:]
    return head, newvec

def p1(mem, debug=False):
    muls = re.findall(r'mul\(\d\d?\d?,\d\d?\d?\)', mem)
    
    ans = 0
    for mul in muls:
        l,r = mul.split(",")
        l = l.replace("mul(","")
        r = r.replace(")","")
        try:
            lnum = int(l)
            rnum = int(r)
            ires = lnum*rnum
            if debug:
                print(f"{mul} -> {lnum}*{rnum} = {ires}")
            ans += ires
        except:
            if debug:
                print(f"fail for {l},{r}")

    print(ans)

def p2(mem):
    i_ms = re.finditer(r'do\(\)', mem)
    o_ms = re.finditer(r'don\'t\(\)', mem)
    
    i_starts = [m.start() for m in i_ms]
    o_starts = [m.start() for m in o_ms]
    
    gmask = [ 1 if i in i_starts else 0 for i in range(len(mem))]
    bmask = [-1 if i in o_starts else 0 for i in range(len(mem))]
    bgmask = [g + b for b,g in zip(bmask,gmask)]
    mask_ok = list(accumulate(bgmask, lambda x,y: min(max(x+y,0),1)))
    
    on_chars = [c for c,m in zip(mem,mask_ok) if m ==1]
    new_mem = ''.join(on_chars)
    
    p1(new_mem)

#mem = get_input('ex.txt')
mem = get_input('in.txt')
mem = "".join(mem)
mem = "do()"+mem
p1(mem)
p2(mem)