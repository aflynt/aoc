"""
    +--+
    |  |
    |  |
    +--+

The digger starts in a 1 meter cube hole in the ground. 

They then dig specified_num_meters:
     up    (U) 
     down  (D) 
     left  (L) 
     right (R) 
     clearing full 1 meter cubes as they go. 

     Each trench is also listed with the color the edge of the trench should be painted
     as RGB hexadecimal color code

  VIEW FROM ABOVE
  #   # == dug
  #   . == gnd_level_terrain
     
INSTRUCTIONS: |[UDLR] n (#AABBCC)|
               DIR   N  COLOR

"""
def get_inside_ps(ps):
    maxR = max([r for r,_ in ps])
    maxC = max([c for _,c in ps])
    minR = min([r for r,_ in ps])
    minC = min([c for _,c in ps])
    ips = []
    
    for r in range(minR, maxR):
        for c in range(minC, maxC):
            if is_inside(r, c, ps, maxC):
                ips.append((r,c))
    
    ips = list(set(ips))
    return ips

def get_ps(ds: list[str],ns: list[int])-> list[tuple[int,int]]:
    # input ds: directions [U,D,L,R]
    #       ns: num steps in direction
    # output  : list of (r,c) hole positions 

    ps = [(0,0)]
    
    for d,n in zip(ds,ns):
        dps = mv(ps[-1], d,n)
        #print(f"d: {d}, n: {n}, -> dps: {dps}")
        ps += dps
    
    return list(set(ps))

def get_input(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    lines = [line.strip("\n") for line in lines]
    return lines

def parse_digs_p2(digs: list[str]):
    # input list of digs like "R 6 (#70c710)"

    #           dist  dir at end
    # 70c710 = 461937 R
    # first 5 chars == encode distance
    # last char encodes direction [0,1,2,3] = [R,D,L,U]
    # output ds: directions [U,D,L,R]
    #        ns: num steps in dir
    ds = []
    ns = []
    for dig in digs:
        _,_,c = dig.split()
        c = c.strip("#()")
        n = int(c[0:5],16)
        dstr = int(c[-1])
        if dstr == 0:
            d = "R"
        elif dstr == 1:
            d = "D"
        elif dstr == 2:
            d = "L"
        elif dstr == 3:
            d = "U"
        else:
            assert False

        ds.append(d)
        ns.append(n)
    return ds,ns

def parse_digs(digs: list[str]):
    ds = []
    ns = []
    for dig in digs:
        d,n,c = dig.split()
        n = int(n)
        ds.append(d)
        ns.append(n)
    return ds,ns

def mv(pos, dir, n):
    ps = []

    r = pos[0]
    c = pos[1]

    if dir == "R":
        dr =  0
        dc =  1
    elif dir == "L":
        dr =  0
        dc = -1
    elif dir == "U":
        dr = -1
        dc =  0
    elif dir == "D":
        dr =  1
        dc =  0
    while n > 0:
        n -= 1
        r += dr
        c += dc
        ps.append((r,c))
    return ps

def is_inside( r, c, ps, C):
    ps = set(ps)

    # in_hole
    if (r,c) in ps:
        return False

    hits = 0
    aih = False # already in hole ?

    # row doesnt change for ray cast on this row
    # check other cols from me to edge of grid
    for cc in range(c,C+1):
        tih = (r,cc) in ps # this is hole ?

        if tih and not aih:
            hits += 1

        aih = tih

    return hits % 2 != 0

def dbg(ps):
    maxR = max([r for r,_ in ps])
    maxC = max([c for _,c in ps])
    minR = min([r for r,_ in ps])
    minC = min([c for _,c in ps])

    print(f"rows = {minR} -> {maxR}")
    print(f"cols = {minC} -> {maxC}")

def shift_ps(ps):
    minR = min([r for r,_ in ps])
    minC = min([c for _,c in ps])-2
    # input possibly negative rows -> push them down
    # input possibly negative cols -> push them right
    shifted_ps = []
    for (r,c) in ps:
        shifted_ps.append((r-minR, c-minC))

    return shifted_ps

def print_ps(ps):
    maxR = max([r for r,_ in ps])
    maxC = max([c for _,c in ps])
    ps = set(ps)

    with open("grid.txt", "w") as f:

        for r in range(maxR+1):
            chars = []
            for c in range(maxC+1):
                if (r,c) in ps:
                    char = "#"
                else:
                    char = "."
                chars.append(char)
            chars.append("\n")
            linestr = "".join(chars)
            f.write(linestr)