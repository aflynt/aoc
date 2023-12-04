
def get_grid(fname):
    lines = []
    with open(fname,'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    return lines
    
    
#fname = 'ex.txt'
fname = 'input.txt'

lines = get_grid(fname)

numchars  = ['0','1','2','3','4','5','6','7','8','9',]

nums = []

row = 0
col = 0

for r,line in enumerate(lines):
    innum = False
    numlist = []
    row = r
    col = 0
    for c,char in enumerate(line):
        if char in numchars:
            if innum == False:
                # first char seen
                innum = True
                row = r
                col = c
                numlist.append(char)
            else:
                numlist.append(char)
        else:
            if innum == True:
                numstr = ''.join(numlist)
                numstr = int(numstr)
                nums.append(( row, col, numstr ))
                numlist.clear()
                innum = False

'''
for num in nums[:13]:
    row = num[0]
    col = num[1]
    numstr = num[2]
    print(f'{numstr:3d}: ({row:3d} {col:3d})')
'''

gear_options = []
for r,line in enumerate(lines):
    for c,char in enumerate(line):
        if char == '*':
            gear_options.append(( r,  c ))



L = []

for num in nums:
    row = num[0]
    col = num[1]
    k   = num[2]
    klen = len(str(k))

    ics = list(range(col-1,col+klen+1))
    irs = list(range(row-1,row+2))
    #print(f'{k:3d}: r = {row} c = {col}, len: {klen}, cs: {ics}, rs: {irs}')
    GL = []

    for ir in irs:
        for ic in ics:
            value = (ir,ic)
            if value in gear_options:
                GL.append(value)
    L.append({'row': row, 'col':col, 'val': k, 'gears': GL})


gmap ={}

for l in L:
    val = l['val']
    gears = l['gears']
    row = l['row']
    col = l['col']
    for gear in gears:
        if gear in gmap:
            nlist = gmap[gear]
            nlist.append(val)
        else:
            gmap[gear] = [val]

gear_ratios = []

for k,v in gmap.items():
    true_gear = len(v) == 2
    if true_gear:
        gear_ratio = v[0] * v[1]
        gear_ratios.append(gear_ratio)
    tgstr = '1' if true_gear else '0'
    print(f'{tgstr}| {k}: {v} ')


gsum = sum(gear_ratios)
print(f'sum: {gsum}')
