
from aoclib import *
from collections import defaultdict

num_chars = ["0","1","2","3","4","5","6","7","8","9",]
lo_chars = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",]
hi_chars = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",]
antenna_chars = set(num_chars+lo_chars+hi_chars)

def get_antennas(g:Grid) -> list[Antenna]:
    as_ = []
    for r in range(g.R):
        for c in range(g.C):
            v = g.G[r][c]
            if v in antenna_chars:
                as_.append(Antenna(r,c,v))
    return as_
                
def get_atype_map(g: Grid) -> map:
    a_val_map = defaultdict(set)
    
    as_ = get_antennas(g)
    for a in as_:
        v = a.v
        # get all antennas matching this val
        other_as = set([oa for oa in as_ if oa.v == v])
        a_val_map[v] |= other_as
    
    return a_val_map

def get_antinodes(g: Grid, atype_map: map) -> set[Antinode]:

    ans = set()

    for atype,ants in atype_map.items():
        print(f"looking for antinodes tied to: {atype} -> {ants}")
        for ant in ants:
            # get other antennas of this type
            oants = ants - set([ant])
            for oant in oants:
                #print(f" -me: {ant} , other: {oant}")
                dr = ant.r - oant.r
                dc = ant.c - oant.c
                ans.add((oant.r,oant.c))
                ans.add((ant.r,ant.c))
                for i in range(100):
                    rr = ant.r + (i * dr)
                    cc = ant.c + (i * dc)
                    if 0 <= rr < g.R and 0 <= cc < g.C:
                        ans.add((rr,cc))
                        #ans.add(Antinode(rr, cc))
    
    return ans



######################################
#lines = parse_input("day08ex1.txt")
lines = parse_input("day08in.txt")
g = Grid(lines)

atype_map = get_atype_map(g)

ans = get_antinodes(g, atype_map)



# print
#print()
for an in ans:
    r,c = an
    g.add_char((r,c), "x")
    #print(an)
g.prn()
#
#nans = len(ans)
#print(nans)

print(len(ans))


