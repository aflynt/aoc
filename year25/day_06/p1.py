import numpy as np


# read in a matrix from a text file
def get_input(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    matrix = []

    # last line has operator info, so skip it
    operators = lines[-1].strip().split()
    lines = lines[:-1]

    for line in lines:
        row = list(map(int, line.strip().split()))
        matrix.append(row)
    return operators, np.array(matrix)

# fname = "ex.txt"
fname = "in.txt"
operators, M = get_input(fname)
print("Matrix read from file:")
print(M)

# transpose the matrix
MT = M.T
print("Transposed matrix:")
print(MT)


print("Operators read from file:")
print(operators)

# zip the operators with the rows of the transposed matrix
zipped = list(zip(operators, MT))
print("Zipped operators with transposed matrix rows:")
ans = 0
for op, row in zipped:
    print(f"Operator: {op}, Row: {row}")
    if op == '+':
        ans += np.sum(row)
    elif op == '*':
        ans += np.prod(row)


print("Final answer after applying operators:")
print(ans)