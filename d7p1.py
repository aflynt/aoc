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
    _A  = 0
    _K  = 1
    _Q  = 2
    _J  = 3
    _T  = 4
    _9 = 5
    _8 = 6
    _7 = 7
    _6 = 8
    _5 = 9
    _4 = 10
    _3 = 11
    _2 = 12

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

    

def main1():
    #fname = 'ex.txt'
    #fname = 'ex2.txt'
    fname = 'input.txt'
    hands = get_input1(fname)

    rs = []

    for cards,bid in hands:
        hand_type = get_hand_type(cards)
        cts = [ get_card_type(card) for card in cards ]
        rs.append((hand_type, cts, cards, bid))
    
    rs = sorted(rs, key=lambda t: (t[0], t[1]))
    rs = reversed(rs)
    tot_winnings = 0
    for i, r in enumerate(rs):
        rank = i+1
        hand_type = r[0]
        cts       = r[1]
        cards     = r[2]
        bid       = r[3]
        handstr = ''.join(cards)
        ct_names = [ct.name for ct in cts]
        winning = rank*bid
        tot_winnings += winning

        print(f'{rank:2d} bid: {bid:3d} hand: {handstr} ',end='')
        print(f'hand_type: {hand_type.name:15s} card_types: {ct_names}, won: {winning:4d} winnings: {tot_winnings:4d}')

if __name__ == '__main__':
    main1()