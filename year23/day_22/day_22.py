from lib import *
#fname = "ex.txt"
fname = "in.txt"

lines = get_lines(fname)

vmap,XMAX,YMAX,ZMAX = get_voxels(lines)

CUBE = mk_cube(vmap, XMAX, YMAX, ZMAX)

compress_chunks(vmap, CUBE)

res = 0
for XID in vmap.keys():
    vmapcp,CUBECP = rm_chunk(XID, vmap, CUBE)
    
    nmv = compress_chunks(vmapcp, CUBECP)
    res += nmv
    print(f"--- RM: {XID} moves: {nmv} -> res: {res} -------")

print(f"final sum: {res}")
#get_num_removables(vmap)

