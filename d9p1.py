import numpy as np

def get_input(fname):
    with open(fname) as f:
        lines = f.readlines()
    
    hs = [line.strip('\n') for line in lines]

    shs = []

    for h in hs:
        hvals = h.split()
        hvals = [int(hval) for hval in hvals]
        shs.append(hvals)

    return shs



def predict_next(hvals):

    diffs = np.diff(np.array(hvals), 1)
    return diffs


def extrapolate(h):

    diffs = predict_next(h)
    all_zero = not any(diffs)
    
    h_lists = [h, list(diffs)]
    
    while not all_zero:
        diffs = predict_next(diffs)
        h_lists.append(list(diffs))
        all_zero = not any(diffs)

    h_lists[-1].append(0)

    for h_list in h_lists[0:len(h_lists)-1]:
        h_list.append(0)

    for i,h_list in enumerate(reversed(h_lists[0:len(h_lists)-1])):
        left_val = h_list[-2]
        val_below = h_lists[len(h_lists)-1-i][-1]
        h_list[-1] = left_val + val_below

    return h_lists[0]

def get_lastvals(rhs):
    lastvals = []
    
    for h in rhs:
        h = extrapolate(h)
        lastval = h[-1]
        lastvals.append(lastval)
        #print(f"- |{h}|")
    return lastvals

#fname = 'ex_09.txt'
fname = 'in_09.txt'

hs  = get_input(fname)
rhs = [h[::-1] for h in hs]

lastvals_p1 = get_lastvals(hs)
lastvals_p2 = get_lastvals(rhs)

print(sum(lastvals_p1))
print(sum(lastvals_p2))