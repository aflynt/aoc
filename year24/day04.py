
from collections import defaultdict

def parse_input():

    d = open('ex4.txt', "r").read()
    #d = open('in4.txt', "r").read()
    
    rules,updates = d.split("\n\n")
    
    rules = rules.splitlines()
    updates = updates.splitlines()
    
    uppages = [u.split(",") for u in updates]
    updates = [[ int(p) for p in ps] for ps in uppages]
    
    
    d_fb = defaultdict(list)
    d_bf = defaultdict(list)
    
    for rule in rules:
        f,b = rule.split("|")
        f,b = int(f), int(b)
        d_fb[f].append(b)
        d_bf[b].append(f)

    return updates, d_fb


def check_update(update, d_fb):

    OK = True
    seen = set()
    for page in update:
    
        #ok looking at page
        back_elems = set(d_fb[page])
    
        any_seen = back_elems & seen
        if len(any_seen) > 0:
            OK = False
        #print(f" - page = {page}: back_elems: {back_elems} any_seen: {any_seen} seen: {seen} OK?:{OK}")
        seen.add(page)

    return OK

updates, d_fb = parse_input()
    

def p1():

    okmidvals = []
    for update in updates:
        OK = check_update(update, d_fb)
        if OK:
            midval = update[len(update)//2]
            okmidvals.append(midval)
            #print(f"ok for update: {update} with midval = {midval}")
    
    ans = sum(okmidvals)
    print()
    print(ans)
    print()

#p1() # 5509

def reorder_update(update, d_fb):
    print(f" got bad update: {update}")

def p2():

    okmidvals = []
    for update in updates:
        OK = check_update(update, d_fb)
        if not OK:
            newupdate = reorder_update(update, d_fb)
            #midval = newupdate[len(newupdate)//2]
            #okmidvals.append(midval)
            #print(f"ok for update: {update} with midval = {midval}")
    
    #ans = sum(okmidvals)
    #print()
    #print(ans)
    #print()
#p2()

for k,v in d_fb.items():
    print(f"{k} -> {v}")