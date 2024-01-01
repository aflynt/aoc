from lib import *

fname = ["ex.txt", "in.txt"][-1]

gd = get_input(fname, False)
gu = get_input(fname, True)

print(run_dfs(gd))
print(run_dfs(gu))