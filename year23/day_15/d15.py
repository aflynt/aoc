from enum import Enum
from collections import defaultdict

class OP(Enum):
    EQ = 1
    RM = 2

def get_lines(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    lines = [line.strip("\n") for line in lines]

    lines = lines[0]
    steps = lines.split(",")

    return steps

def run_hash(line):
    val = 0
    for char in line:
        val = (17*(val + ord(char))) % 256
    return val
    
def parse_step(step):
    other_chars = set( ["0","1","2","3","4","5","6","7","8","9","=", "-"] )
    label_chars = [char for char in step if char not in other_chars]
    label = "".join(label_chars)
    if "=" in step:
        flen = int(step[-1])
        op = OP.EQ
    else:
        flen = 0
        op = OP.RM
    return (label, op, flen)
    
def print_boxes(boxes: dict[list[str]]):
    for k,v in boxes.items():
        if len(v)>0:
            print(f"box: {k}: {v}")


#fname = "ex.txt"
fname = "in.txt"

steps = get_lines(fname)

#boxes = defaultdict(list)
boxes = {}
for i in range(256):
    boxes[i] = {}

for step in steps:
    label, op, flen = parse_step(step)
    label_hash = run_hash(label)
    if op == OP.EQ:
        lens_mark = label
        lens_flen = flen
        target_box = label_hash
        target_box_key = lens_mark
        target_box_val = lens_flen
        if target_box_key not in boxes[target_box]:
            boxes[target_box][target_box_key] = target_box_val
        else:
            boxes[target_box][target_box_key] = target_box_val
    else:
        # OP = OP.RM
        target_box = label_hash
        lens_mark = label
        target_box_key = lens_mark
        if target_box_key in boxes[target_box]:
            del boxes[target_box][target_box_key]
        
    #print(f"label: {label:2s}, op: {op}, focal len: {flen}, label_hash: {label_hash}")
    #print_boxes(boxes)
    #x = input()

fp = 0

power = 0
for boxnum,lenses_dict in boxes.items():
    slotnum = 1
    for label, flen in lenses_dict.items():
        ipower = (1+boxnum)*slotnum*flen
        slotnum += 1
        power += ipower
        #print(ipower)

print(power)
