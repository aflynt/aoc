from queue import Queue
from collections import defaultdict
import numpy as np

def get_lines(fname):
    lines = open(fname, "r").read().strip("\n").split("\n")
    return lines

def mk_voxels(bx,by,bz,H,W,D):
    
    if H == 1 and D == 1: # extrude in x
        return [(bi,by,bz) for bi in range(bx,bx+W)]
    elif H == 1 and W ==1: # extrude in y
        return [(bx,bj,bz) for bj in range(by,by+D)]
    else: # extrude in z
        return [(bx,by,bk) for bk in range(bz,bz+H)]


def get_voxels(lines):
    vmap = {}
    XMAX = 0
    YMAX = 0
    ZMAX = 1

    for i, line in enumerate(lines):

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


def find_supporters(i_name, i_vd, vmap):

    # Who supports me
    supporters = set()

    bz,bx,by,H,W,D = i_vd

    if bz == 1:
        supporters.add("gnd")

    z_chk = bz-1
    ivs = mk_voxels(bx,by,z_chk,1,W,D)

    for k,v in vmap.items():
        if k == i_name:
            continue
        oz,ox,oy,oH,oW,oD = v
        ozmax = oz+oH-1
        if ozmax != z_chk:
            continue
        ovs = mk_voxels(ox,oy,ozmax,1,oW,oD)
        FOUND = False
        for ovi in ovs:
            if not FOUND:
                for ivi in ivs:
                    if ovi == ivi:
                        supporters.add(k)
                        FOUND = True
                        break

    return supporters


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


def push_down_floaters(floaters, vmap, CUBE):
    
    Q = Queue()
    Q = enqueue_floaters(floaters,Q)
    
    while not Q.empty():
        chunk_name = Q.get()
    
        mv_chunk_dn(chunk_name, vmap, CUBE)
    

def compress_chunks(vmap, CUBE):

    floaters = get_cube_floaters(vmap, CUBE)
    pushed = floaters
    
    while len(floaters) > 0:
        push_down_floaters(floaters, vmap, CUBE)
        floaters = get_cube_floaters(vmap, CUBE)
        pushed |= floaters
    return len(pushed)


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

def rm_chunk(xid: int, vmap: dict[int,tuple[int,int,int,int,int,int]], CUBE):

    # make copies
    vmapcp = vmap.copy()
    CUBECP = np.copy(CUBE)

    # remove from vmap
    del vmapcp[xid]

    # remove from CUBE
    bz,bx,by,H,W,D = vmap[xid]
    ivs = mk_voxels(bx,by,bz,H,W,D)
    for ivx,ivy,ivz in ivs:
        CUBECP[ivz,ivx,ivy] = 0

    return vmapcp, CUBECP