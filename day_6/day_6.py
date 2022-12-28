from aoc_lib import *
        
def unique_count(x, n):

    y = set(x)
    if len(y) != n:
        return False
    return True

def find_first_marker_index(data, n=4):

    is_ = 0
    ie_ = n-1

    x = data[is_:ie_+1]
    u = unique_count(x, n)

    while not u:
        is_ += 1
        ie_ += 1
        x = data[is_:ie_+1]
        u = unique_count(x, n)
        #print(f'uniq? = {u} for x = {x}, se = {is_}-{ie_}')
    
    return ie_ + 1

def solve(fname, mchars):
    data = read_input(fname)
    data_list = data.split('\n')
    for data in data_list:
        n = find_first_marker_index(data, mchars)
    return n


fname = 'input_test.txt'
fname = 'input_real.txt'

#n1 = solve(fname,  4)
#n2 = solve(fname, 14)

#print(n1)
#print(n2)
