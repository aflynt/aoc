import math as m

def get_cardval(w, p):

    nmatch = 0
    cardval = 0
    for val in p:
        if val in w:
            nmatch += 1
            if nmatch == 1:
                cardval = 1
            else:
                cardval *= 2
    return nmatch, cardval

def get_lines(fname):
    with open(fname) as f:
        lines = f.readlines()
        
    lines = [line.strip() for line in lines]
    return lines



def get_ws(cards):
    Ws = []

    for card in cards:
        leader = card.split(':')[1]
        wstrs = leader.split('|')[0]
        nums = wstrs.strip().split(' ')
        Ws.append(nums)

    Ws = [w for w in Ws if len(w) > 0]
    return Ws

def get_ps(cards):
    Ws = []

    for card in cards:
        leader = card.split(':')[1]
        wstrs = leader.split('|')[1]
        nums = wstrs.strip().split(' ')
        nums = [n for n in nums if len(n)> 0]
        Ws.append(nums)
    
    Ws = [w for w in Ws if len(w) > 0]
    return Ws

#cards = get_lines('input.txt')
cards = get_lines('input_test.txt')

Ws = get_ws(cards)
Ps = get_ps(cards)


total = 0
i = 1
for w,p in zip(Ws,Ps):
    n2 = [a for a in p if a in w]
    n2 = len(n2)
    #n, cardval = get_cardval(w,p)
    c2 = m.floor(2**(n2-1))
                
    total += c2
    print(f'i: {i:3d} n: {n2:2d} cardval: {c2}')
    i += 1

print(f'total = {total}')