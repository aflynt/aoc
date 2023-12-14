from itertools import combinations
from typing import Tuple, List
from functools import cache


def get_records(fname):
    with open(fname) as f:
        records = f.readlines()
        records = [r.strip('\n') for r in records]
        return records

def parse_records(records):
    crs = []
    for record in records:
        c,r = record.split(" ")
        r = r.split(",")
        r = [int(ri) for ri in r]
        crs.append((c,r))
    return crs

def count_hashes(condstr: str):
    hashes = condstr.split(".")
    hashes = [h for h in hashes if len(h) > 0]
    counts = [len(h) for h in hashes]
    return counts

@cache
def is_combo_ok(combo, cond: str, hashlens):
    
    # place hashes at combo indexes into condition string
    # check against hashlens
    cond = cond.replace("?",".")
    cond = [c for c in cond]
    for c_idx in combo:
        cond[c_idx] = "#"
    condstr = "".join(cond)

    hcs = count_hashes(condstr)
    ok = hcs == hashlens

    #print(f"ending str: {condstr}, hashes: {hcs}, ok?: {ok}")

    if ok:
        return 1
    return 0


def count_arrangements(record):

    cond = record[0]
    hashlens = record[1]
    sum_hashes = sum(hashlens)
    
    hash_idxs = [i for i,char in enumerate(cond) if char == "#"]
    idk_idxs  = [i for i,char in enumerate(cond) if char == "?"]

    n_hashes_to_place = sum_hashes - len(hash_idxs)

    combos = combinations(idk_idxs, n_hashes_to_place) # indexs to place n_hashes
    #oks = [ is_combo_ok(combo, cond, hashlens) for combo in combos]

    n_oks = 0
    for combo in combos:
        combo = tuple(combo)
        hashlens = tuple(hashlens)
        n_oks += is_combo_ok(combo, cond, hashlens)

    return n_oks

def count_folded_arrangements(crs):
    res = 0
    for cr in crs:
        n = count_arrangements(cr)    
        res += n
    return res

def unfold_record(cr: Tuple[str,List[int]]):
    ntimes = 5
    cond = cr[0]
    condlist = [cond for i in range(ntimes)]
    condlist = "?".join(condlist)
    hashlens = cr[1]

    unfolded_hashlens = []
    for _ in range(ntimes):
        for val in hashlens:
            unfolded_hashlens.append(val)

    return (condlist, unfolded_hashlens)


#-----------------------------------------------------
#fname = "input.txt"
fname = "ex.txt"
records = get_records(fname)
crs = parse_records(records)

crs = [unfold_record(cr) for cr in crs]
crs = [crs[2]]

#-----------------------------------------------------
#print(f" p1: {count_folded_arrangements(crs)}")
print(f" p2: {count_folded_arrangements(crs)}")




#-----------------------------------------------------