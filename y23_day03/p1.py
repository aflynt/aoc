
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

gears = []
for r,line in enumerate(lines):
    for c,char in enumerate(line):
        if char != '.' and char not in numchars:
            gears.append(( r,  c ))


good_nums = []

for num in nums:
    row = num[0]
    col = num[1]
    k   = num[2]
    klen = len(str(k))

    ics = list(range(col-1,col+klen+1))
    irs = list(range(row-1,row+2))
    print(f'{k:3d}: r = {row} c = {col}, len: {klen}, cs: {ics}, rs: {irs}')

    for ir in irs:
        for ic in ics:
            value = (ir,ic)
            if value in gears:
                good_nums.append(k)
                #print(f'bingo for value: {value} & num: {k}')

for num in good_nums[:13]:
    print(num)



print(f'sum: ',sum(good_nums))
'''
'''