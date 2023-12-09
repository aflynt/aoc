import sys

fname = 'ex.txt'
fname = 'input.txt'

D = open(fname).read().strip()
L = D.split("\n")

parts = D.split("\n\n")
seed,*others = parts
seed = [int(x) for x in seed.split(':')[1].split()]

class Function:
    def __init__(self, S):
        lines = S.split('\n')[1:] # throw away name
        # dst src sz
        self.tuples = [[int(x) for x in line.split()] for line in lines]
    def apply_one(self, x: int) -> int:
        for (dst, src, sz) in self.tuples:
            if src<=x<=src+sz:
                return x+dst-src
        return x
    # list of [start, end) ranges
    def apply_range(self, R):
        A = []
        for (dest, src, sz) in self.tuples:
            src_end = src+sz
            NR = []
            while R:
                # [st                               ed)
                #             [src    src_end]
                # [before    ][inter         ][after  )
                (st, ed) = R.pop()
                before = (st, min(ed,src))
                inter  = (max(st, src), min(src_end, ed))
                after  = (max(src_end, st), ed)
                if before[1]>before[0]:
                    NR.append(before)
                if inter[1]>inter[0]:
                    A.append((inter[0]-src+dest, inter[1]-src+dest))   
                if after[1]>after[0]:
                    NR.append(after)
            R = NR
        return A+R
                   
Fs = [Function(s) for s in others]

P1 = []
for x in seed:
    for f in Fs:
        x = f.apply_one(x)
    P1.append(x)
print(min(P1))


P2 = []
pairs = list(zip(seed[::2], seed[1::2]))
for st, sz in pairs:
    # inclusive on the left, exclusive on the right
    # eg [1,4) -> [1,2,3]
    # length of [a,b) = b-a
    # [a,b) + [b,c) = [a,c)
    R = [(st, st+sz)]
    for f in Fs:
        R = f.apply_range(R)
    P2.append(min(R)[0])
print(min(P2))    



