
def mult(old, val):
    return old * val
    
def add(old, val):
    return old + val

def pow(old, val):
    return old ** val

lcm = 7*2*19*3*13*11*5*17

class monkey:
    def __init__(self, id:int, op:str, operand:int, divnum:int, true_monkey_id:int, false_monkey_id:int, items:list[int]):
        self.id = id
        self.operand = operand
        self.divnum = divnum
        self.items = items
        self.TM = true_monkey_id
        self.FM = false_monkey_id
        self.items_inspected = 0

        if op == '*':
            self.op = mult
        elif op == '+':
            self.op = add
        else:
            self.op = pow

        #self.op = op # new = "old * old" or "old * 19"

    def do_op(self):

        monkey_vals = [] 

        #print(f'Monkey {self.id}:')

        for item in self.items:
            #print(f'  monkey inspects an item with a worry level of {item}')
            new = self.op(item, self.operand)
            #new = eval(self.op_fn)
            #print(f'  worry level operation: {self.op_fn} sets worry level to : {new}')
            # ROUND 1 ONLY
            #______________________________
            #______________________________
            #______________________________
            #new = new // 3
            #______________________________
            #______________________________
            #print(f'  monkey gets bored with item. worry level is divided by 3 to: {new}')

            divnum = self.divnum
            self.items_inspected += 1

            new %= lcm

            if new % divnum == 0:
                #print(f'  current worry level is ___ divisible by {divnum}')
                monkey_vals.append((self.TM, new))
                #print(f'  item with worry level {new} is thrown to monkey {self.TM}')
            else:
                #print(f'  current worry level is NOT divisible by {divnum}')
                monkey_vals.append((self.FM, new))
                #print(f'  item with worry level {new} is thrown to monkey {self.FM}')

        
        self.items = []

        return monkey_vals
                
                
m_dict = {
    #0 : monkey(0, '*', 19, 23, 2, 3, [79, 98]),
    #1 : monkey(1, '+',  6, 19, 2, 0, [54, 65, 75, 74]),
    #2 : monkey(2, '^',  2, 13, 1, 3, [79, 60, 97]),
    #3 : monkey(3, '+',  3, 17, 0, 1, [74]),
    #-1: monkey( id=0, op='*', operand=19, divnum=7, )
    0 : monkey( 0, '*', 19 ,  7, 6, 2, [ 59, 74, 65, 86]),
    1 : monkey( 1, '+',  1 ,  2, 2, 0, [ 62, 84, 72, 91, 68, 78, 51]),
    2 : monkey( 2, '+',  8 , 19, 6, 5, [ 78, 84, 96]),
    3 : monkey( 3, '^',  2 ,  3, 1, 0, [ 97, 86]),
    4 : monkey( 4, '+',  6 , 13, 3, 1, [ 50]),
    5 : monkey( 5, '*', 17 , 11, 4, 7, [ 73, 65, 69, 65, 51]),
    6 : monkey( 6, '+',  5 ,  5, 5, 7, [ 69, 82, 97, 93, 82, 84, 58, 63]),
    7 : monkey( 7, '+',  3 , 17, 3, 4, [ 81, 78, 82, 76, 79, 80]),
}

#NROUNDS = 20
NROUNDS = 10000

for i in range(NROUNDS):

    for m_id,m in m_dict.items():
    
        monkey_vals = m.do_op()
    
        for m_id, val in monkey_vals:
            m = m_dict[m_id]
            m.items.append(val)



mi = [ m_dict[i].items_inspected  for i in range(len(m_dict.keys())) ]

mi.sort()

mb = mi[-1] * mi[-2]
print(mb)


    