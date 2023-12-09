import time

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
    C = {}

    # Card 1: w1 w2 ... | p1 p2 ...
    for card in cards:
        x,y = card.split(':')
        x = x.split('Card ')[1]
        x = x.strip()
        cardnum = int(x)
        wstrs,pstrs = y.split('|')
        wstrs = wstrs.strip()
        pstrs = pstrs.strip()
        wnums = wstrs.strip().split(' ')
        pnums = pstrs.strip().split(' ')
        wnums = [w for w in wnums if len(w)>0]
        pnums = [p for p in pnums if len(p)>0]
        n,_ = get_cardval(wnums, pnums)
        C[cardnum] = n

    return C


lines = get_lines('input.txt')
C = get_ws(lines)

def get_card_scratchers(card_num, card_wins, ns ):

    # add card to inscratchers
    ns += 1

    if card_wins:
        card_num += 1
        for icard_num in range(card_num, card_num+card_wins):
            ns = get_card_scratchers(icard_num, C[icard_num], ns)
            
    return ns

    

tic = time.perf_counter()

ns = 0
for card_num, card_wins in C.items():
    if card_wins:
        ns = get_card_scratchers(card_num, card_wins, ns)

toc = time.perf_counter()

#ns = inscratchers
print(f'num scratchers: {ns}')
print(f'time = {toc - tic:10.1f} seconds')