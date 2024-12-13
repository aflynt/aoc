import time

def exec_op(op, a, b):

    match op:
        case "+": return a + b
        case "*": return a * b
        case   _: return int(f"{str(a)}{str(b)}")



def apply_two_ops_stack( v, tval, op):
    #print(f"calling with: tval: {tval}, op:{op}, v:{v}, res:{res}")

    # assume we can always get two values from v

    #opval = exec_op(op, v[0], v[1])

    match op:
        case "+": opval = v[0] + v[1]
        case "*": opval = v[0] * v[1]
        case   _: opval = int(f"{str(v[0])}{str(v[1])}")

    # base case of two args in stack
    if len(v) == 2:
        return opval

    if opval > tval:
        return 0

    # push back onto stack
    v[1] = opval
    newv = v[1:]

    #try other options with newv
    if   apply_two_ops_stack( newv.copy(), tval, "+") == tval: 
        return tval
    elif apply_two_ops_stack( newv.copy(), tval, "*") == tval: 
        return tval
    elif apply_two_ops_stack( newv.copy(), tval, "||") == tval: 
        return tval
    else:
        return 0



def parse_input(fname):

    d = open(fname, "r").read()
    lines = d.split("\n")

    return lines

def test_eq(eq):
    tv, nums = eq.split(": ")
    tval = int(tv)
    nums = nums.split()
    v = [int(num) for num in nums]
    
    if   apply_two_ops_stack( v.copy(), tval, "+") == tval: 
        return tval
    elif apply_two_ops_stack( v.copy(), tval, "*") == tval: 
        return tval
    elif apply_two_ops_stack( v.copy(), tval, "||") == tval: 
        return tval
    else:
        return 0

#eqns = parse_input("test.dat")
#eqns = parse_input("day07ex.txt")
eqns = parse_input("day07in.txt")


t_0 = time.time()
ans = 0
for eq in eqns:
    ans += test_eq(eq)
print(ans)


t_1 = time.time()
dt = t_1 - t_0
print(f"dt = {dt} secs")