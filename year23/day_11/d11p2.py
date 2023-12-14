import copy

def get_lines(fname):
    with open(fname) as f:
        lines = f.readlines()
        lines = [line.strip("\n") for line in lines]
        return lines



def find_empty_rows(lines):
    erows = []

    for i,row in enumerate(lines):
        if "#" not in row:
            erows.append(i)
    return erows

def find_empty_cols(lines):

    allcols = list(range(len(lines[0])))
    for row in lines:
        for c,char in enumerate(row):
            if char == "#":
                if c in allcols:
                    allcols.remove(c)

    return allcols
                
def expand_rows(lines: list[str], erows: list[int], xtimes=1):

    # expand empties x-times

    erows = reversed(erows)

    erowstr = ["." for i in range(len(lines[0]))]
    erowstr = "".join(erowstr)

    for erow_idx in erows:
        for i in range(xtimes): 
            lines.insert(erow_idx, erowstr)

    return lines

def extend_line(linestr, ecols, xtimes):

    # expand empties x-times
    linechars = [c for c in linestr]

    for ci in ecols:
        for i in range(xtimes):
            linechars.insert(ci, ".")

    newstr = "".join(linechars)
    return newstr
        

def expand_cols(lines: list[str], ecols: list[int], xtimes=1):
    
    ecols = ecols[::-1]

    nlines = []

    for line in lines:
        nline = extend_line(line, ecols, xtimes)
        nlines.append(nline)
    return nlines

class Galaxy():
    def __init__(self, id, r, c):
        self.id = id
        self.r = r
        self.c = c
    def __sub__(self, other):
        x1 = self.r
        y1 = self.c
        x2 = other.r
        y2 = other.c
        return abs(x1 - x2) + abs(y1 - y2)
    def __str__(self):
        return f"{self.id:02d}_{self.r:02d}_{self.c:02d}"
    def __repr__(self):
        mestr = self.__str__()
        return f"Galaxy({mestr})"
        
def get_galaxies(lines):
    id = 1

    Gs = []

    for r,line in enumerate(lines):
        for c,char in enumerate(line):
            if char == "#":
                g = Galaxy(id,r,c)
                id += 1
                Gs.append(g)
    return Gs

def get_pairs(Gs):

    ps = []
    
    for i in range(len(Gs)):
        for j in range(i+1, len(Gs)):
            g0 = Gs[i]
            g1 = Gs[j]
            ps.append((g0, g1))
    return ps

def expand_xtimes(lines, erows, ecols, xtimes):

    lines = expand_rows(lines, erows, xtimes)
    lines = expand_cols(lines, ecols, xtimes)
    
    Gs = get_galaxies(lines)
    ps = get_pairs(Gs)
    
    sumd = sum([p0-p1 for p0,p1 in ps])
    return sumd
    
#fname = "ex.txt"
fname = "input.txt"
lines = get_lines(fname)
og_lines = copy.deepcopy(lines)

og_erows = find_empty_rows(lines)
og_ecols = find_empty_cols(lines)


xts = [1, 10, 100, 1000]
xts = [1, 10-1, 100-1, 1000-1]
for xtimes in xts:
    lines = copy.deepcopy(og_lines)
    erows = copy.deepcopy(og_erows)
    ecols = copy.deepcopy(og_ecols)

    print(f"xtimes: {xtimes:4d} sum: {expand_xtimes(lines, erows, ecols, xtimes)}")
