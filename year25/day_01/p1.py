
class Dial:
    def __init__(self, size=100, start=50):
        self.size = size
        self.pos = start % size
        # count how many times pos has been zero (include initial position)
        self.zero_count = 1 if self.pos == 0 else 0

    def step(self, dir, n):
        # if dir == "R", we add n, else we subtract n
        if dir == "R":
            # if new pos > size, wrap around
            self.pos = (self.pos + n) % self.size
        else:
            # if new pos < 0, wrap around
            self.pos = (self.pos - n) % self.size

        # increment counter whenever pos is zero
        if self.pos == 0:
            self.zero_count += 1

        return self.pos

    def __str__(self):
        return f"Dial(pos={self.pos:02d}, size={self.size:03d}, zeros={self.zero_count:d})"

class HexDial:
    def __init__(self, size=100, start=50):
        self.size = size
        self.pos = start % size
        # count how many times pos has been zero (include initial position)
        self.zero_count = 1 if self.pos == 0 else 0

    def step(self, dir, n):
        # count every intermediate click that lands on 0
        for _ in range(n):
            if dir == "R":
                self.pos = (self.pos + 1) % self.size
            else:
                self.pos = (self.pos - 1) % self.size
            if self.pos == 0:
                self.zero_count += 1
        return self.pos

    def __str__(self):
        return f"HexDial(pos={self.pos:02d}, size={self.size:03d}, zeros={self.zero_count:d})"


def print_nums(mem):
    # print a list of numbers 
    for i in range(0,80):
        if i%10 == 0:
            pstr = "_"
        else:
            pstr = f"{i%10:d}"
        print(pstr, end="")
    print()

def get_input(fname):
    lines = open(fname, "r").read().strip("\n").split("\n")
    return lines


def p1(lines, debug=False):

    dial = Dial()

    for line in lines:
        # split into direction and number
        dir = line[0]
        n = int(line[1:])
        pos = dial.step(dir, n)
        if debug:
            print(f"dial = {dial}, step {dir}{n:03d} -> pos={pos:02d}")
        
    # answer is how many times pos was zero
    print(f"Part 1: dial zeroed {dial.zero_count:d} times")

def p2(lines, debug=False):

    dial = HexDial()

    for line in lines:
        # split into direction and number
        dir = line[0]
        n = int(line[1:])
        pos = dial.step(dir, n)
        if debug:
            print(f"dial = {dial}, step {dir}{n:03d} -> pos={pos:02d}")
        
    # answer is how many times pos was zero
    print(f"Part 2: dial zeroed {dial.zero_count:d} times")


#lines = get_input('ex.txt')
lines = get_input('in.txt')

p1(lines, debug=False)
p2(lines, debug=False)