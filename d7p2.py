from collections import defaultdict
from enum import IntEnum

class HANDTYPE(IntEnum):
    FIVEOFONEKIND = 0
    FOUROFONEKIND = 1
    FULLHOUSE     = 2
    THREEOFAKIND  = 3
    TWOPAIR       = 4
    ONEPAIR       = 5
    HIGHCARD      = 6

class CARDTYPE(IntEnum):
    _A = 0
    _K = 1
    _Q = 2
    _T = 3
    _9 = 4
    _8 = 5
    _7 = 6
    _6 = 7
    _5 = 8
    _4 = 9
    _3 = 10
    _2 = 11
    _J = 12

def get_card_type(card_name):
    if   card_name == 'A': ct = CARDTYPE._A
    elif card_name == 'K': ct = CARDTYPE._K
    elif card_name == 'Q': ct = CARDTYPE._Q
    elif card_name == 'J': ct = CARDTYPE._J
    elif card_name == 'T': ct = CARDTYPE._T
    elif card_name == '9': ct = CARDTYPE._9
    elif card_name == '8': ct = CARDTYPE._8
    elif card_name == '7': ct = CARDTYPE._7
    elif card_name == '6': ct = CARDTYPE._6
    elif card_name == '5': ct = CARDTYPE._5
    elif card_name == '4': ct = CARDTYPE._4
    elif card_name == '3': ct = CARDTYPE._3
    else:                  ct = CARDTYPE._2
    return ct
        

def get_input1(fname):
    lines = []
    with open(fname, 'r') as f:
        lines = f.readlines()

    lines = [line.strip('\n') for line in lines]
    hands = []

    for line in lines:
        hand,bid = line.split()
        bid = int(bid)
        hand = [l for l in hand]
        hands.append((hand,bid))

    return hands


def get_card_counts(hand):
    hd = defaultdict(int)

    for l in hand:
        hd[l] += 1
    return hd.values()
    

def get_hand_type(hand):

    card_counts = get_card_counts(hand) # hand dict of card_label: card_count

    has5 = 5 in card_counts
    has4 = 4 in card_counts
    has3 = 3 in card_counts
    has2 = 2 in card_counts
    numPairs = len([ 1 for v in card_counts if v == 2])

    # is 5 of a kind?
    if has5:
        return HANDTYPE.FIVEOFONEKIND

    # is 4 of a kind?
    elif has4:
        return HANDTYPE.FOUROFONEKIND

    # is full house?
    elif has3 and has2:
        return HANDTYPE.FULLHOUSE

    # is 3 of a kind?
    elif has3:
        return HANDTYPE.THREEOFAKIND

    # is two pair?
    elif numPairs == 2:
        return HANDTYPE.TWOPAIR

    # is one pair?
    elif numPairs == 1:
        return HANDTYPE.ONEPAIR
    # high card?
    else:
        return HANDTYPE.HIGHCARD

def is_full_house(ncnts,jcnt):

    numPairs = len([ 1 for v in ncnts if v == 2])
    has3_std = 3 in ncnts
    has2_std = 2 in ncnts
    """
    _____
    is_c1 xxxyy -> has_3_std and has_2_std
    is_c2 xxJyy -> has two_pair_std and 1 J
    is_c3 xJJyy -> has one_pair_std and 2 J
    is_c4 JJJyy -> has one_pair_std and 3 J
    """
    is_c1 = has3_std and has2_std
    is_c2 = numPairs == 2 and jcnt == 1
    is_c3 = numPairs == 1 and jcnt > 1
    is_fh = any([is_c1 , is_c2 , is_c3])
    return is_fh

def is_three_of_a_kind(ncnts, jcnt):
    has3_std = 3 in ncnts
    has2_std = 2 in ncnts

    is_c1 = has3_std
    is_c2 = has2_std and jcnt == 1
    is_c3 = has2_std and jcnt > 1
    is_c4 = jcnt >= 2
    is3 = any([is_c1 , is_c2 , is_c3 , is_c4])
    return is3
    
def is_five_of_a_kind(ncnts,jcnt):
    # ncnts = [1 2 1 1] -> list of card counts
    nmax = 0
    if len(ncnts) > 0:
        nmax = max(ncnts)
    if nmax + jcnt >= 5:
        return True
    return False

def is_four_of_a_kind(ncnts,jcnt):
    # ncnts = [1 2 1 1] -> list of card counts
    nmax = max(ncnts)
    if nmax + jcnt >= 4:
        return True
    return False

def is_two_pair(ncnts, jcnt):

    numPairs = len([ 1 for v in ncnts if v == 2])

    is2_1 = numPairs == 2 
    is2_2 = numPairs == 1 and jcnt > 0
    res = is2_1 or is2_2
    return res

def is_one_pair(ncnts, jcnt):

    numPairs = len([ 1 for v in ncnts if v == 2])

    is_c1 = numPairs >= 1
    is_c2 = jcnt > 0
    res = is_c1 or is_c2
    return res

def get_counts(hand):

    hd = defaultdict(int)
    for card in hand:
        hd[card] += 1

    ncnts = [v for k,v in hd.items() if k != 'J'] # normal counts
    jcnt = hd['J'] # joker count

    return ncnts, jcnt
    

def get_hand_type2(hand):

    ncnts, jcnt = get_counts(hand)

    if is_five_of_a_kind(ncnts,jcnt):
        return HANDTYPE.FIVEOFONEKIND

    elif is_four_of_a_kind(ncnts,jcnt):
        return HANDTYPE.FOUROFONEKIND

    elif is_full_house(ncnts,jcnt):
        return HANDTYPE.FULLHOUSE

    elif is_three_of_a_kind(ncnts, jcnt):
        return HANDTYPE.THREEOFAKIND

    elif is_two_pair(ncnts, jcnt):
        return HANDTYPE.TWOPAIR

    elif is_one_pair(ncnts, jcnt):
        return HANDTYPE.ONEPAIR
    else:
        return HANDTYPE.HIGHCARD

    
def collect_results(hands):
    # results = (hand_type, card_types, cards, bid)
    rs = []

    for cards,bid in hands:
        hand_type  = get_hand_type2(cards)
        card_types = [ get_card_type(card) for card in cards ]
        rs.append((hand_type, card_types, cards, bid))
    
    rs = sorted(rs, key=lambda t: (t[0], t[1]))
    rs = reversed(rs)
    return rs

def get_winnings(rs):

    tot_winnings = 0
    for i, r in enumerate(rs):
        tot_winnings += (i+1)*r[3]

    return tot_winnings
    
def print_results(rs):
    rs = list(rs).copy()
    for i, r in enumerate(rs):
        rank = i+1
        hand_type = r[0]
        cts       = r[1]
        cards     = r[2]
        bid       = r[3]
        handstr = ''.join(cards)
        ct_names = [ct.name for ct in cts]

        print(f'{rank:4d} bid: {bid:4d} hand: {handstr} ',end='')
        print(f'hand_type: {hand_type.name:15s} card_types: {ct_names}')
    return rs

def main2():
    #fname = 'ex.txt'
    #fname = 'ex2.txt'
    #fname = 'ex3.txt'
    fname = 'input.txt'
    hands = get_input1(fname)

    rs = collect_results(hands)

    #rs = print_results(rs)
    tot_winnings = get_winnings(rs)

    print(f"winnings: {tot_winnings}")


if __name__ == '__main__':
    main2()

#p2 250665248
