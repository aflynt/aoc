import re
import sys
def ints(s):
    return [int(x) for x in re.findall('-?\d+', s)]
infile = sys.argv[1] if len(sys.argv)>=2 else 'in17.txt'
ans = 0
D = open(infile).read().strip()

regs, program = D.split('\n\n')
A,B,C = ints(regs)
program = program.split(':')[1].strip().split(',')
program = [int(x) for x in program]

class Computer:
    def __init__(self, A=0, B=0, C=0, IP=0,
                 program:list[int]=[], part2=True) -> None:
        self.A = A
        self.B = B
        self.C = C
        self.IP = IP
        self.outs = []
        self.P = program
        self.part2 = part2
    def run(self):
        while self.IP < len(self.P)-1:
            self.step()
            #self.print_state()
        return self.outs

    def step(self):
        opcode  = self.P[self.IP]
        operand = self.P[self.IP+1]
        n,v = self.decode_opcode(opcode, operand)
        #print(f"oc,ov = {opcode:1d} {operand:1d} -> {n:3s} {v:1d} -> ", end="")
        match n:
            case 'adv': self.apply_adv(v)
            case 'bxl': self.apply_bxl(v)
            case 'bst': self.apply_bst(v)
            case 'jnz': self.apply_jnz(v)
            case 'bxc': self.apply_bxc(v)
            case 'out': self.apply_out(v)
            case 'bdv': self.apply_bdv(v)
            case 'cdv': self.apply_cdv(v)

    def print_state(self):
        print(f"ABCI = ", end='')
        print(f"{self.A:5d} ", end='')
        print(f"{self.B:5d} ", end='')
        print(f"{self.C:5d} ", end='')
        print(f"{self.IP:5d} ", end='')
        print(f"{self.outs}")

    def decode_opcode(self, opcode, operand):
        opname = "adv"
        optype = "COMBO_OP"
        opval = operand
        match opcode:
            case 0: opname = 'adv'
            case 1: opname = 'bxl'
            case 2: opname = 'bst'
            case 3: opname = 'jnz'
            case 4: opname = 'bxc'
            case 5: opname = 'out'
            case 6: opname = 'bdv'
            case 7: opname = 'cdv'
        match opname:
            case 'adv': optype = "COMBO_OP"
            case 'bxl': optype = "LITERAL_OP"
            case 'bst': optype = "COMBO_OP"
            case 'jnz': optype = "LITERAL_OP"
            case 'bxc': optype = "LITERAL_OP"
            case 'out': optype = "COMBO_OP"
            case 'bdv': optype = "COMBO_OP"
            case 'cdv': optype = "COMBO_OP"
        match optype:
            case "COMBO_OP":
                match operand:
                    case i if i in range(0,4): opval = operand
                    case 4: opval = self.A
                    case 5: opval = self.B
                    case 6: opval = self.C
                    case 7: assert False, "reserved operand 7"
            case "LITERAL_OP":
                opval = operand
        return opname,opval

    def apply_adv(self, opval):
        # perform division -> A
        numer = self.A
        denom = 2**opval
        res = numer // denom
        self.A = res
        self.IP += 2
    def apply_bxl(self, opval):
        # calc bitwise XOR of reg B and LITERAL_OP -> B
        x = self.B
        y = opval
        res = x ^ y
        self.B = res
        self.IP += 2
    def apply_bst(self, opval):
        # calc val of combo_op % 8 -> B
        res = opval % 8
        self.B = res
        self.IP += 2
    def apply_jnz(self, opval):
        if self.A != 0:
            # jump by setting IP to val of LITERAL_OP (IP != 2 + IP)
            self.IP = opval
        else:
            self.IP += 2
    def apply_bxc(self, _):
        # calc bitwise xor of B and C -> B (reads and ignore operand)
        res = self.B ^ self.C
        self.B = res
        self.IP += 2
    def apply_out(self, opval):
        # calc combo_op % 8 -> output value (sep multiple vals by comma)
        res = int(opval % 8)
        # output value
        self.outs.append(res)
        if self.part2 and len(self.outs) > 0:
          last_out = self.outs[len(self.outs)-1]
          last_p   = self.P[   len(self.outs)-1]
          if last_out != last_p:
            return self.outs
        self.IP += 2
    def apply_bdv(self,opval):
        # like adv but store result in B
        # perform division -> B
        numer = self.A
        denom = 2**opval
        res = numer // denom
        self.B = res
        self.IP += 2
    def apply_cdv(self, opval):
        # like adv but store result in C
        # perform division -> C
        numer = self.A
        denom = 2**opval
        res = numer // denom
        self.C = res
        self.IP += 2



def p1():

    R_A= 51342988
    P = [2,4,1,3,7,5,4,0,1,3,0,3,5,5,3,0]
    c = Computer(R_A, 0, 0, 0, P)

    outs = c.run()

    outs = [f"{o}" for o in outs]
    res = ",".join(outs)
    print(res)

#p1()

def px(a,b,c):

    R_A = a
    R_B = b
    R_C = c
    P = [2,4,1,3,7,5,4,0,1,3,0,3,5,5,3,0]
    c = Computer(R_A, R_B, R_C, 0, P)

    outs = c.run()

    print(f"{R_A:5d} {R_B:5d} {R_C:5d} -> outs:{outs} ")
          #{outs} len= {len(outs)} vs {P} len: {len(P)}")

def p2():
    P = [2,4,1,3,7,5,4,0,1,3,0,3,5,5,3,0]
    #P = program
    #P = [0,3,5,4,3,0]


    print(f"prgm = {P} len= {len(P)}")

    is_out_same = False
    #R_A= int(4e6)
    #R_A= int(3.515e13)
    #R_A = 35184374000000
    Ast = 0

    best = 0

    while not is_out_same:
        Ast += 1
        #R_A = Ast * 8**9 + 0o6762360173
        R_A = Ast

        c = Computer(R_A, 0, 0, 0, P)
        outs = c.run()
        is_out_same = outs == P

        #if R_A % 10000 == 0:
        #print(f"{R_A:10d} -> outs: {outs} len= {len(outs)}")
        if len(outs) > best:
            print(R_A, oct(R_A), best, len(P))
            #print(f"{R_A:10d} {oct(R_A):10s} {best} {len(P)}")
            best = len(outs)

    c = Computer(R_A, 0, 0, 0, P)
    outs = c.run()
    print(f"found R_A: {R_A}")
    print(f"outs = {outs}")
    print(f"prgm = {P}")

p2()


#px(int(335184374000000))
#px(int(3.52e13))
#px(int(3.55e13))
#px(int(3.6e13))
#px(int(3.7e13))


'''
for a in range(8):
  print(f"A = {a} ------")
  for b in range(8):
    print(f" - B = {b} ====")
    for c in range(8):
      px(a, b, c)
'''
