import re
from typing import List

def pop_front(vec:List):
    head = vec[0]
    newvec  = vec[1:]
    return head, newvec


def get_input(fname):
    lines = open(fname, "r").read().strip("\n").split("\n")
    return lines

#mem = get_input('ex.txt')
mem = get_input('ex2.txt')
#mem = get_input('in.txt')
mem = "".join(mem)
mem = "do()"+mem
for i in range(0,67):
    if i%10 == 0:
        pstr = "_"
    else:
        pstr = f"{i%10:d}"
    print(pstr, end="")
print()
print(mem)

def p1():
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
            print(f"{mul} -> {lnum}*{rnum} = {ires}")
            ans += ires
        except:
            print(f"fail for {l},{r}")

    print(ans)

def p2():
    #in_ms = re.findall(r'do\(\)', mem)
    i_ms = re.finditer(r'do\(\)', mem)
    o_ms = re.finditer(r'don\'t\(\)', mem)

    i_starts  = [m.start() for m in i_ms]
    o_starts = [m.start() for m in o_ms]
    print(f" i starts = {i_starts}")
    print(f" o starts = {o_starts}")




    #ins = re.findall(r'.*do.*mul\(\d\d?\d?,\d\d?\d?\)', mem)
    #muls = re.findall(r'mul\(\d\d?\d?,\d\d?\d?\)', mem)
    
    #ans = 0
    #for mul in muls:
        #l,r = mul.split(",")
        #l = l.replace("mul(","")
        #r = r.replace(")","")
        #try:
        #    lnum = int(l)
        #    rnum = int(r)
        #    ires = lnum*rnum
        #    print(f"{mul} -> {lnum}*{rnum} = {ires}")
        #    ans += ires
        #except:
        #    print(f"fail for {l},{r}")

    #print(ans)


#p2()

gs = [0, 10, 20, 40]
bs = [5,  7, 30, 50]

head, gs = pop_front(gs)
tail, bs = pop_front(bs)
res = [(head, tail)]
is_good_state = False


while len(bs) > 0:

    if not is_good_state:
        # in bad state -> keep eating bad points
    
        head,gs = pop_front(gs)
        tail,bs = pop_front(bs)
    
        while tail < head:
            tail,bs = pop_front(bs)
        is_good_state = True

        res.append((head, tail))
    
    else:
        # in good_state -> keep eating good points
        head,gs = pop_front(gs)
        tail,bs = pop_front(bs)
        next_head = gs[0]
        while next_head < tail:
            head,gs = pop_front(gs)
            next_head = gs[0]
        is_good_state = False

        res.append((head, tail))

    print(f"sg: {is_good_state} bs: {bs} gs: {gs} head: {head} tail: {tail} res: {res}")




