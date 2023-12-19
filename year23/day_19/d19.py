
def get_wr(fname):
    line = open(fname).read()
    line = line.strip("\n")

    w, r = line.split("\n\n")

    wfs = w.split("\n") 
    rs = r.split("\n")

    workflows = {}
    for wf in wfs:
      name,rest = wf.split("{")
      rest = rest[:-1]
      rules = rest.split(",")
      workflows[name] = rules

    parts = []
    for rating in rs:
      rating = rating[1:-1]
      rating = rating.replace("x=", "").replace("m=","").replace("a=","").replace("s=", "")
      rns = rating.split(",")
      rns = [int(n) for n in rns]
      parts.append(('in', rns))

    return workflows, parts

def check_rule(loc, rule, x,m,a,s):
    if ":" in rule:
      # conditional
      xmas_cond,go_dir = rule.split(":")
      if "<" in xmas_cond:
        xmas_char,numstr = xmas_cond.split("<")
        num = int(numstr)
        if   xmas_char == "x": return go_dir if x < num else loc
        elif xmas_char == "m": return go_dir if m < num else loc
        elif xmas_char == "a": return go_dir if a < num else loc
        elif xmas_char == "s": return go_dir if s < num else loc
        else: assert False
      elif ">" in xmas_cond:
        xmas_char,numstr = xmas_cond.split(">")
        num = int(numstr)
        if   xmas_char == "x": return go_dir if x > num else loc
        elif xmas_char == "m": return go_dir if m > num else loc
        elif xmas_char == "a": return go_dir if a > num else loc
        elif xmas_char == "s": return go_dir if s > num else loc
        else: assert False
      else: assert False
    else:
      # unconditional jump
      return rule
    
def get_new_loc(loc, rules, x,m,a,s):
  newloc = loc
  for rule in rules:
    newloc = check_rule(loc, rule, x,m,a,s)
    if newloc != loc:
        return newloc
  return loc
      
def process_workflows(parts, wfs):
    mod_parts = []
    for loc,xmas in parts:
      rules = wfs[loc]
      x,m,a,s = xmas
      newloc = get_new_loc(loc, rules, x, m, a, s)
      mod_parts.append((newloc, xmas))
    return mod_parts


#fname = "ex.txt"
fname = "in.txt"
wfs,parts = get_wr(fname)


As = []
while len(parts) > 0:
    parts = process_workflows(parts, wfs)
    pas = [part for part in parts if part[0] == 'A']
    As += pas
    parts = [part for part in parts if part[0] != 'R' and part[0] != 'A']
 
a_vals = [v for _,v in As]

ans = 0
for vals in a_vals:
  ans += sum(vals)

print(f"{ans}")