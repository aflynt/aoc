
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
                
def expand_rows(lines: list[str], erows: list[int]):

    erows = reversed(erows)

    erowstr = ["." for i in range(len(lines[0]))]
    erowstr = "".join(erowstr)

    for erow_idx in erows:
        lines.insert(erow_idx, erowstr)

    return lines

def extend_line(linestr, ecols):

    linechars = [c for c in linestr]

    for ci in ecols:
        linechars.insert(ci, ".")

    newstr = "".join(linechars)
    return newstr
        

def expand_cols(lines: list[str], ecols: list[int]):
    
    ecols = ecols[::-1]

    nlines = []

    for line in lines:
        nline = extend_line(line, ecols)
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
    
#fname = "ex.txt"
fname = "input.txt"
lines = get_lines(fname)

erows = find_empty_rows(lines)
ecols = find_empty_cols(lines)

lines = expand_rows(lines, erows)
lines = expand_cols(lines, ecols)

Gs = get_galaxies(lines)
ps = get_pairs(Gs)

sumd = sum([p0-p1 for p0,p1 in ps])
print(sumd)
