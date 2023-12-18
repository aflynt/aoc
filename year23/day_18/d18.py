from lib import *

            
    
fname = "ex.txt"
#fname = "in.txt"

digs = get_input(fname)

#ds,ns = parse_digs(digs)

ds,ns = parse_digs_p2(digs)

for d,n in zip(ds,ns):
    print(f"{d} -> {n}")

#ps = get_ps(ds,ns)

#ps = shift_ps(ps)

#print_ps(ps)

#ips = get_inside_ps(ps)

#nperim = len(ps)
#nfill = len(ips)
#ntot = nfill + nperim

#print(f"nperim: {nperim}")
#print(f"nfill : {nfill}")
#print(f"ntotal: {ntot}")

#print(ps)
#print(ips)