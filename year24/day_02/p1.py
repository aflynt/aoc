def get_input(fname):
    lines = open(fname, "r").read().strip("\n").split("\n")
    return lines

def get_deltas(levels):

    deltas = []

    x0 = levels[0]
    for i in range(len(levels)-1):
        dx = levels[i] - levels[i+1]
        deltas.append(dx)

    return deltas

def check_safe(deltas):

    is_pos = [x > 0 for x in deltas]
    is_not_pos = [x < 0 for x in deltas]
    diff_ok = all([abs(x) >= 1 and abs(x) <= 3 for x in deltas])
    is_ascending = all(is_not_pos)
    is_descending = all(is_pos)
    is_safe = (is_ascending or is_descending) and diff_ok

    return is_safe


#reports = get_input("ex.txt")
reports = get_input("in.txt")

def p1():

    nsafe = 0

    for i,report in enumerate(reports):
        levels = report.split()
        levels = [int(j) for j in levels]
        deltas = get_deltas(levels)
        is_safe = check_safe(deltas)
    
        if is_safe:
            nsafe += 1
    
        #print(f"{i} -> any_safe: [{any_safe}] nsafe: [{nsafe}]")
    
    print(f"nsafe: {nsafe}")

def p2():

    nsafe = 0

    for i,report in enumerate(reports):
        levels = report.split()
        levels = [int(k) for k in levels]
    
        any_safe = False
    
        for j in range(len(levels)):
            ls = levels.copy()
            ls.pop(j)
            deltas = get_deltas(ls)
            is_safe = check_safe(deltas)
            #print(f"checking levels: [{ls}] -> j={j:3d} ds=[{deltas}] is_safe={is_safe}")
            if is_safe:
                any_safe = True
    
        if any_safe:
            nsafe += 1
    
        #print(f"{i} -> any_safe: [{any_safe}] nsafe: [{nsafe}]")
    
    print(f"nsafe: {nsafe}")

p1()
p2()