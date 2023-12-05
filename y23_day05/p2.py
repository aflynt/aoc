import sys
import matplotlib.pyplot as plt
import numpy as np

def parse_input(fname):
    seed_list = []

    with open(fname, 'r') as f:
        lines = f.readlines()
    
    lines = [line.strip() for line in lines]

    seed_list = lines[0].split(':')[1].strip().split()
    seed_list = [int(i) for i in seed_list]
    lines = lines[2:]
    Ms = {}
    map_name = ''
    map_lists = []
    for i,line in enumerate(lines):
        if 'map' in line:
            map_name = line.split(' map:')[0]
            continue
        elif len(line) == 0:
            smlist = sorted(map_lists)
            Ms[map_name] = smlist
            map_lists.clear()
        else:
            rng = line.strip().split()
            rng = [int(i) for i in rng]
            dst_rng_start = rng[0]
            src_rng_start = rng[1]
            rng_len = rng[2]
            src_rng_end = src_rng_start + rng_len - 1
            dst_rng_end = dst_rng_start + rng_len - 1
            map_lists.append((src_rng_start, src_rng_end, dst_rng_start, dst_rng_end))

    # one last value
    Ms[map_name] = map_lists.copy()

    return seed_list, Ms

def convert_val(sval, rng_lists):
    dval = sval
    for rng in rng_lists:
        s0, sf,d0,_ = rng

        val_in_rng = sval >= s0 and sval <= sf
        if val_in_rng:
            dval = sval - s0 + d0
            return dval
    return dval

def get_src(dst, rngs):
    for rng in rngs:
        (src0, srcf, dst0, dstf) = rng
        if (dst0 <= dst and dst <= dstf):
            src = dst + src0 - dst0
            return src
    return dst


'''
Ms = {
    
    'mapname' : [
        (s0, sf, d0, df ),
        (s0, sf, d0, df ),
    ]
}

'''
fname = 'ex.txt'
#fname = 'input.txt'
#seed_list,tomaps = parse_input(fname)
svals,Ms = parse_input(fname)


dsts = [i for i in range(101)]
key_dsts = [0,55,56,59,60,96]
#

path = []

back_ms = [
    'humidity-to-location',
    'temperature-to-humidity',
    'light-to-temperature',
    'water-to-light',
    'fertilizer-to-water',
    'soil-to-fertilizer',
    'seed-to-soil',
]

for map_name in back_ms:
    rngs = Ms[map_name]
    srcs = [get_src(d, rngs) for d in key_dsts]
    #path.append(srcs)
    print(f'stage: {map_name:40s}: dest: {key_dsts} -> src: {srcs}')

#for p in path:
#    print(p)

#rngs = Ms['temperature-to-humidity']
#srcs = [get_src(d, rngs) for d in dsts]
#rngs = Ms['light-to-temperature']
#srcs = [get_src(d, rngs) for d in dsts]
#rngs = Ms['water-to-light']
#srcs = [get_src(d, rngs) for d in dsts]
#rngs = Ms['fertilizer-to-water']
#srcs = [get_src(d, rngs) for d in dsts]
#rngs = Ms['soil-to-fertilizer']
#srcs = [get_src(d, rngs) for d in dsts]
#rngs = Ms['seed-to-soil']
#srcs = [get_src(d, rngs) for d in dsts]
#
#plt.plot(dsts,srcs,'*')
##
#plt.show()

#seeds = svals

#seed_list = set()

#for i,seed in enumerate(seeds):
#    if i%2 == 0:
#        start = seeds[i]
#        cnt = seeds[i+1]
#        svals = set(range(start, start+cnt))
#        seed_list |= svals
#
##seed_list = sorted(list(seed_list))
#seed_list = [i for i in range(101)]
#seeds = seed_list
#svals = seed_list
#
#dvals = svals

#for map_name,rng_lists in Ms.items():
#
#    print(f'checking: {map_name}')
#    for rng in rng_lists:
#        print(f' - {rng}')
#
#    dvals = [convert_val(sval, rng_lists) for sval in svals]
#
#    #print(f'map: {map_name}')
#    #for sval,dval in zip(svals, dvals):
#    #    print(f' - {sval} -> {dval}')
#    svals = dvals


#print(f'final: ')
#minloc = sys.maxsize
#for sval,dval in zip(seeds, dvals):
#    minloc = min(minloc, dval)
#    print(f' - {sval:12d} -> {dval:12d}, min = {minloc:12d}')


# ANSWER: 486613012
'''
'''

