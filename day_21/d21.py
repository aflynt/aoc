def get_var_expr(lines):

    lines = [ line for line in lines if len(line) > 0 ]
    lines = [ (line.split(':')) for line in lines ]
    lines = [ (var, expr.strip()) for (var, expr) in lines ]

    return lines

def parse_context(lines) -> dict[str,int]:

    ctx = {}

    for var,expr in lines:

        # either value or binary op
        if expr[-1] in [ '0','1','2','3','4','5','6','7','8','9',]:
            # expr is an integer value
            ctx[var] = int(expr)
        else:
            # we have a binary op
            var_l, opchar, var_r = expr.split()
            ctx[var] = (var_l, opchar, var_r)

    return ctx

def get_lines(fname):

    with open(fname, 'r') as f:
        lines = f.readlines()
    lines = [ line.strip('\n') for line in lines]
    return lines

in_data = '''
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
'''

fname = 'indata.txt'

lines = get_lines(fname)

#lines = in_data.split('\n')
lines = get_var_expr(lines)
E = parse_context(lines)

def f(name, h):
    words = E[name]

    if name == 'humn' and h >= 0:
        return h

    if isinstance(words, int):
        return words
    else:
        assert len(words) == 3
        e1 = f(words[0], h)
        e2 = f(words[2], h)
        #print(f'e1 = {e1}, op={words[1]} e2 = {e2}')
        if   words[1] =='*':
            return e1 * e2
        elif words[1] == '/':
            return e1 / e2
        elif words[1] == '+':
            return e1 + e2
        elif words[1] == '-':
            return e1 - e2
        else:
            assert False, words


print(int(f('root',-1)))


p1 = E['root'][0]
p2 = E['root'][2]

if f(p2,0) != f(p2,1):
    p1,p2 = p2,p1


assert f(p1,0) != f(p1,1)
assert f(p2,0) == f(p2,1)
target = f(p2,0)

lo = 0
hi = int(1e20)
while lo < hi:
    mid = (lo+hi)//2
    score = target - f(p1,mid)
    if score < 0:
        lo = mid
    elif score == 0:
        print(mid)
        break
    else:
        hi = mid





