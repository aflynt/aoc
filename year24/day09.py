
#from aoclib import *
import aoclib as xl

def count_disk(disk):
    p1 = 0
    for i,c in enumerate(disk):
        if c == ".":
            break
        else:
            n = int(c)
            p1 += i*n

    return p1

def get_bs(nums):

    bs = []
    ss = []

    for i,sz in enumerate(nums):

        if i%2 == 0:
            blkid = i//2
            bs.append((blkid, sz))
        else:
            ss.append(sz)

    return bs,ss

def print_disk(disk):
    dstr = ''.join(disk)
    print(dstr)

def pop_front_block(bs):
    blk = bs[0]
    bs = bs[1:]
    blkid, bsz = blk
    return blkid, bsz, bs

def pop_front_space(ss):
    sz = ss[0]
    ss = ss[1:]
    return sz,ss

def write_block_ids(disk, j, bsz, blkid):
    while bsz > 0:
        disk[j] = str(blkid)
        j += 1
        bsz -= 1

    return j

def push_back_block(bs, rblkid, rbsz):
    if rbsz > 0:
        bs.append((rblkid, rbsz))
    return bs

def push_block_into_space(j, disk, space_sz, rbsz, rblkid ):
    while space_sz > 0 and rbsz > 0:
        disk[j] = str(rblkid)
        j += 1
        rbsz -= 1
        space_sz -= 1
    return j,disk,rbsz,space_sz

def write_next_space(j, disk, bs, ss):

    if len(ss) > 0:
        space_sz,ss = pop_front_space(ss)
        
        while space_sz > 0 and len(bs) > 0:

            rblkid, rbsz = bs.pop()

            j,disk,rbsz,space_sz = push_block_into_space(j,disk,space_sz, rbsz, rblkid)
            
            bs = push_back_block(bs, rblkid, rbsz)

    return j,disk,bs,ss

def write_next_block(j, disk, bs):
    if len(bs) > 0:
        blkid, bsz, bs = pop_front_block(bs) # get block
        j = write_block_ids(disk, j, bsz, blkid) # lay down block ids
    return j,disk,bs

class File:
    def __init__(self, sz, addr, id):
        self.sz = sz
        self.addr = addr
        self.id = id
    def __str__(self):
        #return f"F id: {self.id:2d} sz: {self.sz:2d} addr: {self.addr:2d} "
        return f"F({self.id:2d},{self.sz:2d},{self.addr:2d})"
    def __lt__(self, other):
        return self.id < other.id
    def __gt__(self, other):
        return self.id > other.id
    def __ge__(self, other):
        return self.id >= other.id
    def __le__(self, other):
        return self.id <= other.id
    def __repr__(self):
        return f"F({self.id:2d},{self.sz:2d},{self.addr:2d})"

class Mem:
    def __init__(self, sz, addr):
        self.sz = sz
        self.addr = addr
    def __str__(self):
        #return f"M sz: {self.sz:2d} addr: {self.addr:2d}"
        return f"M({self.sz:2d},{self.addr:2d})"
    def __repr__(self):
        return f"M({self.sz:2d},{self.addr:2d})"
    def __lt__(self, other):
        return self.addr < other.addr
    def __le__(self, other):
        return self.addr <= other.addr
    def __eq__(self, other):
        return self.sz == other.sz and self.addr == other.addr
    def __hash__(self):
        return hash(1000000000*self.sz+self.addr)

def part1(nums):
    bs,ss = get_bs(nums)
    disk_sz = sum(nums)
    disk = ['.' for i in range(disk_sz)]

    j = 0
    for i in range(disk_sz):

        j,disk,bs = write_next_block(j, disk, bs)
        j,disk,bs,ss = write_next_space(j, disk, bs, ss)

    #print_disk(disk)
    p1 = count_disk(disk)
    print(p1)

def get_FM(mem_sizes)-> tuple[list[File], list[Mem]]:

    fs = []
    ms = []

    addr = 0

    for i,mem_sz in enumerate(mem_sizes):
        if i % 2 == 0:
            # we have a file at this addr
            # make a file
            id = i // 2
            fs.append(File( mem_sz, addr, id))
        else:
            # we have free mem at this addr
            ms.append(Mem( mem_sz, addr))
        addr += mem_sz

    ms = [m for m in ms if m.sz > 0]

    return fs,ms


# ----------------------------------------
#line = xl.parse_input("ex09.txt")[0]
line = xl.parse_input("in09.txt")[0]
nums = [ int(c) for c in line]

fs,ms = get_FM(nums)

disk = ['.' for _ in range(sum(nums))]

fs.sort()
fs.reverse()
ms = set(ms)
for f in fs:
    okms = [mm for mm in ms if mm.addr < f.addr and mm.sz >= f.sz]
    okms.sort()
    if len(okms):
        # ok this is the lowest addr to fit
        mmtarget = okms[0]
        newaddr = mmtarget.addr
        f.addr = newaddr

        newm = Mem(mmtarget.sz - f.sz, mmtarget.addr + f.sz)
        ms.discard(mmtarget)
        ms.add(newm)

        print(f" -> f = {f}, found ok ms: {mmtarget}")

    
def write_files(fs: list[File]):
    ans = 0
    for f in fs:
        j = f.addr
        for dj in range(f.sz):
            ans += (j+dj)*(f.id)
    print(ans)

write_files(fs)
