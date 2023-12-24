from lib import *
#fname = "ex.txt"
fname = "in.txt"

lines = get_lines(fname)

vmap,XMAX,YMAX,ZMAX = get_voxels(lines)

CUBE = mk_cube(vmap, XMAX, YMAX, ZMAX)

compress_chunks(vmap, CUBE)

get_num_removables(vmap)

