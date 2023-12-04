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
    C = []

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
        n,v = get_cardval(wnums, pnums)
        C.append((cardnum, n, v))

    return C

def retrieve_card(card_list, i):
    card = (0,0,0)
    # card = (num, nwins, val)
    for card in card_list:
        num, nwins, val = card
        if num == i:
            return card
    return card

def get_card_scratchers(card, card_list, inscratchers):

    card_num, card_wins, _ = card

    # add card to inscratchers
    inscratchers.append(card_num)

    # get list of cards that this card won us
    copy_cards = list(range(card_num+1,card_num+card_wins+1))
    copy_cards = [ retrieve_card(card_list,i) for i in copy_cards]

    if len(copy_cards) == 0:
        return inscratchers
    else:
        # get the copy cards scratchers
        for cpc in copy_cards:
            get_card_scratchers(cpc, card_list, inscratchers)
            
        return inscratchers

lines = get_lines('input.txt')
C = get_ws(lines)
    
scratchers = []
for c in C:
    get_card_scratchers(c, C, scratchers)

ns = len(scratchers)
print(f'num scratchers: {ns}')