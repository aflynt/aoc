#from itertools import repeat
from itertools import cycle
from lib import *


rocks = [ 
     rock('-'),
     rock('+'),
     rock('J'),
     rock('I'),
     rock('O'),
]

jets = get_data('part1_input.txt')
#jets = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
jet_cycle = cycle(jets)
rock_cycle = cycle(rocks)

ch = chamber(jet_cycle)

NMAX = 1_000_000_000_000
NMAX = 10000
NMAX = 2022
NMAX = 1000

with open('deb.dat', 'w') as f:

    for i in range(NMAX):
       rock = next(rock_cycle) 
       ch.add_rock(rock)
       #seen = ch.drop_rock()
       #seen = ch.drop_rock(f, True)
       seen = ch.drop_rock(f, False)
       if seen:
            #print(f'hit at i = {i+1}')
            f.write(f'hit at i = {i+1}\n')
            break
       #if i % 1_000 == 0:
       rep_str = f'\n{i+1:2d} h = {ch.HGRID-1}, dropped {rock.type}\n' 
       #x = input(rep_str)
       #print(rep_str)
       f.write(rep_str)

print(f'{i+1:2d} h = {ch.HGRID-1}')

#ch.add_rock(rocks[0])
#ch.drop_rock()
#ch.add_rock(rocks[1])
#ch.drop_rock()
#ch.add_rock(rocks[2])
#ch.drop_rock()
#ch.add_rock(rocks[3])
#ch.drop_rock()
#ch.add_rock(rocks[4])
#ch.drop_rock()

'''
ch.add_rock(rock('+'))
ch.plot()

mv_ok = True

while mv_ok:

     jet_char = next(jet_cycle)

     print(f'blow {jet_char}')
     ch.move_rock(jet_char)

     ch.plot()

     mv_ok = ch.move_rock('v')
     if mv_ok:
          print(f'fall down 1 unit')
     else:
          print(f'rock came to a rest')

     ch.plot()



'''