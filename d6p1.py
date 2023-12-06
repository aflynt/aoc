import numpy as np
import math as m

def quadratic(a,b,c):
    x1 = (-b + m.sqrt(b*b - 4*a*c))/(2*a)
    x2 = (-b - m.sqrt(b*b - 4*a*c))/(2*a)

    xhi = max(x1,x2)
    xlo = min(x1,x2)
    return xlo,xhi

def get_input(fname):
    lines = []
    with open(fname, 'r') as f:
        lines = f.readlines()

    lines = [line.strip('\n') for line in lines]

    dts = lines[0].split(':')[1].split()
    dxs = lines[1].split(':')[1].split()

    dts = [int(dt) for dt in dts]
    dxs = [int(dx) for dx in dxs]

    dtxs = list(zip(dts,dxs))

    return dtxs

def get_input2(fname):
    lines = []
    with open(fname, 'r') as f:
        lines = f.readlines()

    lines = [line.strip('\n') for line in lines]

    dts = lines[0].split(':')[1].split()
    dxs = lines[1].split(':')[1].split()

    dt = int(''.join(dts))
    dx = int(''.join(dxs))

    return dt,dx

def is_pos(x):
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1

def cnt_wins(dt_max, dx_rec):
    dtw = np.arange(1,dt_max) # wait time
    dx  = dtw*dt_max-dtw**2
    diff = dx - dx_rec
    sgn = [is_pos(x) for x in diff]
    oks = [i for i in sgn if i > 0]
    #print(f'dt_max = {dt_max}, N_OK: {len(oks)}')
    return len(oks)



def main1():
    #fname = 'ex.txt'
    fname = 'input.txt'
    dtxs = get_input(fname)
    ns = []
    for dt,dx in dtxs:
        n = cnt_wins(dt,dx)
        ns.append(n)
    p1 = np.product(ns)
    print(f"p1: {p1}")


def main2():
    #fname = 'ex.txt'
    fname = 'input.txt'
    dt,dx = get_input2(fname)
    a = 1
    b = -dt
    c = dx
    xlo,xhi = quadratic(a,b,c)

    xhi = m.floor(xhi)
    xlo = m.ceil(xlo)
    cnt = xhi-xlo+1
    print(f'p2: {cnt}')

if __name__ == '__main__':
    main1()
    main2()