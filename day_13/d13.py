import functools  as ft

def get_lines(fname):
    lines = []

    with open(fname, 'r') as f:
        lines = f.readlines()
    
    lines = [ line.strip() for line in lines]
    return lines


def get_packet_pair_map(lines):

    # get list of pairs by splitting on empty line
    line_str = '|'.join(lines)
    lines = line_str.split('||')
    
    
    # get list of packet pairs by splitting on |
    pps = [ line.split('|') for line in lines ]
    
    # make map of packet_num : packet_pairs
    i = 1
    pp_map = {}
    
    for pp in pps:
        p0 = pp[0]
        p1 = pp[1]
        pp_map[i] = {
              'left'  : p0, 
              'right' : p1
            }
        i += 1
    
    return pp_map


def is_right_order_ints(left:int, right:int, i=0):

    ldr = '  '*i
    #print(f'{ldr}- Compare {left} vs {right}')

    # lower int should come first
    order = 0

    if left < right:
        #print(f'{ldr} - Left side is smaller, so inputs are __IN THE RIGHT ORDER__')
        order = 1
    elif left > right:
        #print(f'{ldr} - Left side is larger, so inputs are __NOT__ in the right order')
        order = -1
    else:
        order = 0
    return order

def is_right_order_lists(left:list, right:list, i=0):

    ldr = '  '*i
    #print(f'{ldr}- Compare {left} vs {right}')

    order = 0
    # Compare the first value of each list, then the second value, and so on.
    for L,R in zip(left, right ):
        order = is_right_order(L, R, i+1)
        if order in [1, -1]:
            # found result
            return order

    # no order yet. check list lengths
    # If the left list runs out of items first, the inputs are in the right order. 
    len_L = len(left)
    len_R = len(right)
    if len_L < len_R:
        #print(f'{ldr}- Left side ran out of items, so inputs are __IN THE RIGHT ORDER__')
        order =  1
    #If the right list runs out of items first, the inputs are not in the right order. 
    elif len_L > len_R:
        #print(f'{ldr}- Right side ran out of items, so inputs are __NOT__ in the right order')
        order = -1
    #If the lists are the same length and no comparison makes a decision about the order, 
    #continue checking the next part of the input.
    else:
        order = 0

    return order

def is_right_order(left, right, i=0):

    ldr = '  '*i

    #print(f'{ldr}- Compare {left} vs {right}')

    '''
    * packet is a list
    * packet data is list or int
    * list starts with [
    * list contains 0+ comma-sep values
    * list ends   with ]

    *  1 = right order
    *  0 = check next
    * -1 = wrong order
    '''
    order = 0

    if   isinstance(left, int ) and isinstance(right, int ): return is_right_order_ints(left, right, i)
    elif isinstance(left, list) and isinstance(right, list): return is_right_order_lists(left, right, i)
    elif isinstance(left, int ) and isinstance(right, list): return is_right_order_lists([left], right, i)
    elif isinstance(left, list) and isinstance(right, int ): return is_right_order_lists(left, [right], i)
    else:
        #print('idk for: ', left, right)
        assert False
    
    return order

def solve_part1(pp_map):
    in_order_indices = []
    
    for i,v in pp_map.items():
        #print(f'== Pair {i} ==')
        L = v['left']
        R = v['right']
        order = 1
        L = eval(L)
        R = eval(R)
        order = is_right_order(L, R)
        if order == 1:
            in_order_indices.append(i)
            #print(f'{i:2d}: {order}')
    
    print(in_order_indices)
    
    sum_indices = sum(in_order_indices)
    print(f'sum : {sum_indices}')


def solve2(pp_map):

    sent1 = [[2]]
    sent2 = [[6]]
    
    ps =  [ eval(pp['left']) for k,pp in pp_map.items()]
    ps += [ eval(pp['right']) for k,pp in pp_map.items()]
    ps.append(sent1)
    ps.append(sent2)
    
    ps = sorted(ps, key=ft.cmp_to_key(is_right_order), reverse=True)

    idx1 = 0
    idx2 = 0
    for i,P in enumerate(ps):
    
        if P == sent1: idx1 = i+1
        if P == sent2: idx2 = i+1
        #print(P)
    
    key = idx1 * idx2
    print(f'{idx1} * {idx2} = {key}')

                

###################################

fname = 'ex.txt'
fname = 'real.txt'

lines  = get_lines(fname)
pp_map = get_packet_pair_map(lines)
# pp_map = { 1: {'left': ..., 'right': ... } ...}
    
#solve_part1(pp_map)
solve2(pp_map)

