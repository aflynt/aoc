#!/usr/bin/python3
import sys

x1 = int(sys.argv[1])
y1 = int(sys.argv[2])
x2 = int(sys.argv[3])
y2 = int(sys.argv[4])

p1 = (x1, y1)
p2 = (x2, y2)

#p1 = (100, 49)
#p2 = (149,  0)

x1,y1 = p1
x2,y2 = p2

dy = y2 - y1
dx = x2 - x1

m = dy / dx

b = y1 - m * x1

print(f'p1 = {p1}')
print(f'p2 = {p2}')
print(f'm = {m}')
print(f'b = {b}')
