import os

def parse_stacks(istacks, step):

    stack_chars = []
    for stack in istacks:
        chunks = [stack[i:i+step] for i in range(0, len(stack), step)]
        stack_chars.append(chunks)

    num_stacks = len(stack_chars[0])

    stacks = {}
    for i in range(1,num_stacks+1):
        istack = []
        for stack_height in stack_chars:
            ichars = stack_height[i-1]
            ichars = ichars.replace('[','')
            ichars = ichars.replace(']','')
            ichars = ichars.strip()
            #print (f'|{ichars}|')
            if len(ichars) > 0:
                istack.append(ichars)
        stacks[i] = list(reversed(istack))
    return stacks

def parse_instructions(instructions):
    
    instructions = instructions.splitlines(False)

    instruction_list = []

    for ins in instructions:

        rest = ins.split('move ')[1]
        nbox = rest.split('from')[0].strip()
        origin_dest = rest.split('from')[1].strip()
        origin = origin_dest.split('to')[0].strip()
        dest   = origin_dest.split('to')[1].strip()

        instruction_list.append({
            'nbox'   : int(nbox),
            'origin' : int(origin),
            'dest'   : int(dest),
        })
    
    return instruction_list

def read_input(fname):
    f = open(fname, 'r')
    data = f.read()

    return data

def print_stacks(stacks):
    for stack in stacks:
        values = stacks[stack]
        print(stack,' : ',values)

def move_box(onum, dnum, stacks):

    #print(f'moving from {onum} to {dnum}')
    #print_stacks(stacks)
    #print('----------')
    stack_origin = stacks[onum]
    stack_dest   = stacks[dnum]
    val = stack_origin.pop()
    stack_dest.append(val)
    #print_stacks(stacks)

def pop_n(alist, n):
    rearlist = []
    while n > 0:
        val = alist.pop()
        rearlist.append(val)
        n -= 1

    return list(reversed(rearlist))
        

def move_n_boxes(onum, dnum, stacks, nboxes):

    #print(f'moving {nboxes} from {onum} to {dnum}')
    #print_stacks(stacks)
    #print('----------')
    stack_origin = stacks[onum]
    stack_dest   = stacks[dnum]

    vals = pop_n(stack_origin, nboxes)
    stack_dest += vals
    #print_stacks(stacks)

def follow_instructions_1(ins, stacks):

    for i in ins:
        nbox   = i['nbox']
        origin = i['origin']
        dest   = i['dest']
        for n in range(nbox):
            move_box(origin, dest, stacks)
    
    topchars = []
    for i in range(1, len(stacks)+1):
        top_char = stacks[i][-1]
        topchars.append(top_char)
    
    top_str = ''.join(topchars)

    print(f'top chars = {top_str}')

def follow_instructions_2(ins, stacks):

    for i in ins:
        nbox   = i['nbox']
        origin = i['origin']
        dest   = i['dest']
        move_n_boxes(origin, dest, stacks, nbox)
    
    topchars = []
    for i in range(1, len(stacks)+1):
        top_char = stacks[i][-1]
        topchars.append(top_char)
    
    top_str = ''.join(topchars)

    print(f'top chars = {top_str}')

def current_path():
    print('current working dir: ', end='')
    dir = os.getcwd()
    print(dir)
    print()
    return dir