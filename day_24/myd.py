from collections import deque

def find_just_over(d:int):

    for i in range(13):
        val1 = 1 * 5**i
        val2 = 2 * 5**i
        if val1 >=d:
            return i,1
        elif val2 >= d:
            return i,2

def to_decimal(snafu):
    
    map_sd = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}

    val = 0

    for i,x in enumerate(list(reversed(snafu))):
        x = map_sd[x]
        val += x * 5**i

    return val





    
def add1(y, s):

    




def to_snafu(d:int, s:deque[str], i=0):

    #push a 1






#     Decimal          SNAFU
dss = [
    (         1,             '1'),
    (         2,             '2'),
    (         3,            '1='),
    (         4,            '1-'),
    (         5,            '10'),
    (         6,            '11'),
    (         7,            '12'),
    (         8,            '2='),
    (         9,            '2-'),
    (        10,            '20'),
    (        15,           '1=0'),
    (        20,           '1-0'),
    (      2022,        '1=11-2'),
    (     12345,       '1-0---0'),
    ( 314159265, '1121-1110-1=0'),
]

#for d,s in dss:
#    s = deque()
#    s = to_snafu(d,s)
#    #print(f'final s = {s}')


for i in range(1,21):
    s = deque()
    s=to_snafu(i,s)


#s = '1=2-02'
#
#d = to_decimal(s)
#print(d)

#for i in range(13):
#    val = 5**i
#    print(f'{i:>10d} {val:>15d}')