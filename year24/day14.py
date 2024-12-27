import matplotlib.pyplot as plt
import numpy as np
from math import prod

class Robot:
    def __init__(self,pr,pc,vr,vc, R=7,C=11):
        self.m_r = pr
        self.m_c = pc
        self.m_dr = vr
        self.m_dc = vc
        self.m_R = R
        self.m_C = C
    def step(self):
        r = self.m_r
        c = self.m_c
        dr = self.m_dr
        dc = self.m_dc
        rr = r + dr
        cc = c + dc
        if rr < 0: rr += self.m_R
        if cc < 0: cc += self.m_C
        if rr >= self.m_R: rr -= self.m_R
        if cc >= self.m_C: cc -= self.m_C
        self.m_r = rr
        self.m_c = cc
    def __str__(self):
        return f"R({self.m_r:3d}, {self.m_c:3d}, {self.m_dr:3d}, {self.m_dc:3d})"
    def __repr__(self):
        return f"Robot({self.m_r:3d}, {self.m_c:3d}, {self.m_dr:3d}, {self.m_dc:3d}, {self.m_R}, {self.m_C})"

class Grid:
    def __init__(self, R, C):
        self.R = R
        self.C = C
        self.G = []
        for r in range(R):
            chars = []
            for c in range(C):
                #char = " "
                char = 0
                chars.append(char)
            self.G.append(chars)
    def prn(self):
        for r in range(self.R):
            for c in range(self.C):
                print(self.G[r][c],end='')
            print()
    def clear(self):
        for r in range(self.R):
            for c in range(self.C):
                #self.G[r][c] = " "
                self.G[r][c] = 0
    def add_robots(self, rs: list[Robot]):
        for rb in rs:
            r = rb.m_r
            c = rb.m_c
            #self.G[r][c] = '*'
            self.G[r][c] = 1

    def write_grid(self, fname_ldr, rs, i):
        ofname = f"{fname_ldr}_{i:05d}.png"
        self.clear()
        self.add_robots(rs)


        plt.figure()
        plt.imshow(self.G)
        plt.savefig(ofname)
        plt.close()
        #plt.show()

        # with open(ofname, "w") as f:
        #     f.write(f"{i:05d}\n")
        #     for r in range(self.R):
        #         for c in range(self.C):
        #             f.write(self.G[r][c])
        #         f.write("\n")
    

def get_lines(fname:str)->list[str]:
    with open(fname, "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines

def get_robots(lines:list[str], R:int, C:int)-> list[Robot]:
    rs = []

    for line in lines:
        a,vs = line.split(" v=")
        _,ps = a.split("p=")

        pc,pr = ps.split(",")
        vc,vr = vs.split(",")
        pr = int(pr)
        pc = int(pc)
        vr = int(vr)
        vc = int(vc)
        r = Robot(pr,pc, vr,vc, R, C)
        rs.append(r)
    return rs

def get_robot_stats(rs: list[Robot]):
    nbots = len(rs)
    r_s = [rb.m_r for rb in rs]
    c_s = [rb.m_c for rb in rs]

    r_std = np.std(r_s)
    c_std = np.std(c_s)
    r_ave = sum(r_s)/nbots
    c_ave = sum(c_s)/nbots
    return r_ave,c_ave,r_std,c_std

def p1():
    #R,C,fname = (7,11, "ex14.txt")
    R,C,fname = (103,101, "in14.txt")
    #R = 7    # R-Tall
    #C = 11   # C-Wide
    mr = (R-1)//2
    mc = (C-1)//2
    NSTEPS = 100

    lines = get_lines(fname)
    rs = get_robots(lines,R,C)


    for i in range(NSTEPS):
        for r in rs:
            r.step()

    nq1 = 0
    nq2 = 0
    nq3 = 0
    nq4 = 0

    for r in range(R):
        for c in range(C):
            for rb in rs:

                if r == rb.m_r and c == rb.m_c:

                    if   r < mr and c < mc: nq1 += 1
                    elif r < mr and c > mc: nq2 += 1
                    elif r > mr and c < mc: nq3 += 1
                    elif r > mr and c > mc: nq4 += 1
    
    res = prod([nq1,nq2,nq3,nq4])
    print(res)




def p2():
    stats = []
    #R,C,fname = (7,11, "ex14.txt")
    R,C,fname = (103,101, "in14.txt")
    g = Grid(R,C)

    lines = get_lines(fname)
    rs = get_robots(lines,R,C)

    for i in range(R*C):
        ii = i+1

        for r in rs:
            r.step()
        
        r_ave,c_ave,r_std,c_std = get_robot_stats(rs)
        stats.append((i,r_ave,c_ave,r_std, c_std))
        if r_std < 25 and c_std < 25:
            print(f"{ii}: {r_std}, {c_std}")

        #g.clear()
        #g.add_robots(rs)
        #g.prn()
        #if 6600 < i < 6700:
        #    g.write_grid("res", rs, i)
                
        #print(f"{i}")

    i_s = [i for i,r,c,a,b in stats  if i > 6500 and i < 7000]
    r_s = [r for i,r,c,a,b in stats  if i > 6500 and i < 7000]
    c_s = [c for i,r,c,a,b in stats  if i > 6500 and i < 7000]
    rs_s = [a for i,r,c,a,b in stats if i > 6500 and i < 7000]
    cs_s = [b for i,r,c,a,b in stats if i > 6500 and i < 7000]
    
    plt.plot(i_s, r_s, "k*", markersize=4)
    plt.plot(i_s, c_s, "b*", markersize=4)
    plt.plot(i_s, rs_s, "m*", markersize=4)
    plt.plot(i_s, cs_s, "y*", markersize=4)
    #plt.show()

if __name__ == "__main__":
    p1()
    p2()