from queue import Queue
from collections import Counter, defaultdict
import sympy as sympy
import numpy as np

def get_lines(fname):
    lines = open(fname, "r").read().strip("\n").split("\n")
    return lines

def mk_voxels(bx,by,bz,H,W,D):
    vs = []
    #print(f"H,W,D = {H},{W},{D}")
    if H == 1 and D == 1: # extrude in x
        return [(bi,by,bz) for bi in range(bx,bx+W)]
    elif H == 1 and W ==1: # extrude in y
        return [(bx,bj,bz) for bj in range(by,by+D)]
    else: # extrude in z
        return [(bx,by,bk) for bk in range(bz,bz+H)]

    #for i in range(bx, bx+W):
    #    for j in range(by, by+D):
    #        for k in range(bz, bz+H):
    #            val = (i,j,k)
    #            vs.append(val)
    #return vs

def get_voxels(lines):
    vmap = {}
    XMAX = 0
    YMAX = 0
    ZMAX = 1

    for i, line in enumerate(lines):
        vs = []

        b,e = line.split("~")
        bx,by,bz = b.split(",")
        ex,ey,ez = e.split(",")
        bx = int(bx)
        by = int(by)
        bz = int(bz)
        ex = int(ex)
        ey = int(ey)
        ez = int(ez)
        H = ez-bz+1
        W = ex-bx+1
        D = ey-by+1
        XMAX = max(XMAX,ex) 
        YMAX = max(YMAX,ey) 
        ZMAX = max(ZMAX,ez) 

        vmap[i] = (bz,bx,by,H,W,D)

    return vmap, XMAX,YMAX, ZMAX

def get_z_chunks(vmap, z):
    local_chunks = {}

    for k,v in vmap.items():
        bz,bx,by,H,W,D = v
        if bz == z:
            local_chunks[k] = (bz,bx,by,H,W,D)

    return local_chunks


def find_supportees(i_name, i_vd, vmap):

    # Who do i support
    supportees = set()

    bz,bx,by,H,W,D = i_vd
    z_sup = bz+H
    ivs = mk_voxels(bx,by,z_sup,1,W,D)

    local_chunks = get_z_chunks(vmap, z_sup)

    for k,v in local_chunks.items():
        if k == i_name:
            continue
        oz,ox,oy,oH,oW,oD = v
        if oz != z_sup:
            continue

        ovs = mk_voxels(ox,oy,oz,1,oW,oD)
        done = False
        for ovi in ovs:
            if not done:
                for ivi in ivs:
                    if ovi == ivi:
                        supportees.add(k)
                        done = True
                        break

    return tuple(sorted(list(supportees)))

def is_ground_supported(i_vs):
    for ix,iy,iz in i_vs:
        if iz == 1:
            return True
    return False


def find_supporters(i_name, i_vd, vmap):

    # Who supports me
    supporters = set()

    bz,bx,by,H,W,D = i_vd

    if bz == 1:
        supporters.add("gnd")

    ivs = mk_voxels(bx,by,bz-1,1,W,D)
    MAX_H = 9
    touchable_z_lo = bz - MAX_H
    touchable_z_hi = bz + 1
    tzrange = range(touchable_z_lo, touchable_z_hi)

    for z in tzrange:
        for k,v in vmap.items():
            if k == i_name:
                continue
            oz,ox,oy,oH,oW,oD = v
            ovs = mk_voxels(ox,oy,oz,oH,oW,oD)
            for ovi in ovs:
                for ivi in ivs:
                    if ovi == ivi:
                        supporters.add(k)

    #supporters = sorted(list(supporters))

    return supporters

def get_floaters(vmap):
    floaters = []
    for chunk_name,chunk_vals in vmap.items():
        #print(f"{c}: {v}")
        sers = find_supporters(chunk_name,chunk_vals, vmap)
        if len(sers) == 0:
            floaters.append(chunk_name)
        print(f"{chunk_name}:  sers: {sers}")
    return floaters

def enqueue_floaters(flist: list[tuple[int,int,int]], Q: Queue):
    for f in flist:
        Q.put(f)
    return Q
        

def mv_chunk_dn(chunk_name, vmap, CUBE):

    # change vmap
    bz,bx,by,H,W,D = vmap[chunk_name]
    vmap[chunk_name] = (bz-1,bx,by,H,W,D)

    # change cube
    ivs = mk_voxels(bx,by,bz,H,W,D)

    for ivx,ivy,ivz in ivs:
        CUBE[ivz,ivx,ivy] = 0
        CUBE[ivz-1,ivx,ivy] = 1
    #for ivx,ivy,ivz in ivs:


def push_down_floaters(floaters, vmap, CUBE):
    
    #print(f"floaters = {floaters}")
    
    Q = Queue()
    Q = enqueue_floaters(floaters,Q)
    
    while not Q.empty():
        chunk_name = Q.get()
    
        mv_chunk_dn(chunk_name, vmap, CUBE)
    
#def filter_non_unique(lst):
#    return [i for i,cnt in Counter(lst).items() if cnt == 1]

def compress_chunks(vmap, CUBE):

    floaters = get_cube_floaters(vmap, CUBE)
    
    i = 0
    while len(floaters) > 0:
        i += 1
        print(f".",end="")
        if i == 80:
            print()
            i = 0
        push_down_floaters(floaters, vmap, CUBE)
        floaters = get_cube_floaters(vmap, CUBE)


def mk_cube(vmap, XMAX, YMAX, ZMAX):
    CUBE = np.zeros((ZMAX+1,XMAX+1,YMAX+1))
    CUBE[0,...] = 1
    
    for k,v in vmap.items():
        bz,bx,by,H,W,D = v
        ivs = mk_voxels(bx,by,bz,H,W,D)
        for ivx,ivy,ivz in ivs:
            CUBE[ivz,ivx,ivy] = 1
        
    return CUBE

def get_cube_floaters(vmap, CUBE):

    floaters = set([chunk for chunk in vmap.keys()])

    # floater if nobody below me
    for k,v in vmap.items():
        bz,bx,by,H,W,D = v
        ivs = mk_voxels(bx,by,bz-1,1,W,D)
        for x,y,z in ivs:
            if CUBE[z,x,y] == 1:
                floaters.remove(k)
                break

    return floaters


def find_removables(vmap):

    ss_map = defaultdict(set)
    
    for k,v in vmap.items():
        sers = find_supporters(k,v,vmap)
        ss_map[k] |= sers

    return ss_map

def get_num_removables(vmap):
    uniqs = set()
    
    ss_map = find_removables(vmap)
    for k,v in ss_map.items():
        if len(v) == 1:
            v = list(v)[0]
            if v != "gnd":
                uniqs.add(v)
    
    NT = len(vmap)
    NKEEP = len(uniqs)
    NRM = NT - NKEEP
    print(f"N Chunks: {NT}")
    print(f"N_uniqus: {NKEEP}")
    print(f"N rm    : {NRM}")