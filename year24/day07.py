

#def apply_op(v, tmp, op, i=0):
#    #print(f"calling with: v:{v} tmp:{tmp}, op:{op}, i:{i}")
#    if len(v) == 0:
#        return tmp
#
#    else:
#        first = v[0]
#        if op == "+":
#            newtmp = first + tmp
#        else:
#            newtmp = first * tmp
#        return apply_op(v[1:], newtmp, op, i+1)
def exec_op(op, a, b):

    if op == "+":
        x = a + b
    elif op == "*":
        x = max(a,1)*max(b,1)
    else:
        # || op
        x = int(f"{str(a)}{str(b)}")
    return x


def apply_two_ops_stack(res, v, tmp, op):
    print(f"calling with: tmp: {tmp}, op:{op}, v:{v}, res:{res}")

    # assume we can always get two values from v
    x0 = v[0]
    x1 = v[1]

    opval = exec_op(op, x0, x1)

    # base case of two args in stack
    if len(v) == 2:
        res.add(opval)
        return opval

    # push back onto stack
    v[1] = opval
    newv = v[1:]

    #try other options with newv

    # try op + on (first,v)
    res1 = apply_two_ops_stack(res, newv, tmp, "+")
    #res1 = apply_two_ops_stack(res, v[1:], first+tmp, "+")

    # try op * on (first,v)
    res2 = apply_two_ops_stack(res, newv, tmp, "*")
    #res2 = apply_two_ops_stack(res, v[1:], first*max(tmp,1), "*")
    res3 = apply_two_ops_stack(res, newv, tmp, "||")


    return res1|res2|res3

def apply_two_ops(res, v, tmp, op):
    print(f"calling with: tmp: {tmp}, op:{op}, v:{v}, res:{res}")
    if len(v) == 0:
        #res.append(tmp)
        res.add(tmp)
        return res

    else:
        first = v[0]

        # try op * on (first,v)
        res1 = apply_two_ops(res, v[1:], first+tmp, "+")

        # try op + on (first,v)
        res2 = apply_two_ops(res, v[1:], first*max(tmp,1), "*")

        res3 = set()
        res4 = set()

        # try op || on (first,v)
        if len(v) >= 2:
            sec = v[1]
            concat = f"{str(first)}{str(sec)}"
            concat = int(concat)
            res3 = apply_two_ops(res, v[2:], concat*max(tmp,1), "||")
            res4 = apply_two_ops(res, v[2:], concat+tmp, "||")

        return res1|res2|res3|res4

def parse_input(fname):

    d = open(fname, "r").read()
    lines = d.split("\n")

    return lines

eqns = parse_input("test.dat")
#eqns = parse_input("day07ex.txt")
#eqns = parse_input("day07in.txt")


ans = 0
for eq in eqns:
    tv, nums = eq.split(": ")
    tval = int(tv)
    nums = nums.split()
    v = [int(num) for num in nums]
    
    #results = apply_two_ops(set(), v, 0, "+")
    results = apply_two_ops_stack(set(), v, 0, "+")
    if tval in results:
        ans += tval
        print(f"hooray for tval: {tval}")
print(ans)
