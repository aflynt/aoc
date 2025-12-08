# read in a matrix from a text file
def get_input(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # find all column indices with an operator in the last line
    op_line = lines[-1]
    operator_indices = [i for i, val in enumerate(op_line) if val in ('+', '*')]

    operators = [op_line[i] for i in operator_indices]

    lines = lines[:-1]
    # strip newline characters
    lines = [line.rstrip('\n') for line in lines]

    # split lines at operator indices
    matrix = []
    for line in lines:
        row = []
        last_index = 0
        for index in operator_indices:
            segment = line[last_index-1:index]
            if segment:
                row.append(segment)
            last_index = index + 1
        # add the last segment after the last operator
        segment = line[last_index-1:]
        if segment:
            row.append(segment)
        matrix.append(row)
    return matrix, operators



fname = "in.txt"
matrix, operators = get_input(fname)


# zip the operators with the columns of the matrix
zipped = list(zip(operators, zip(*matrix)))

ans = 0
for op, op_list in zipped:

    # for each string in col, split into characters and convert to integers
    max_len = max(len(s) for s in op_list)

    M = []
    for j in range(max_len):
        nstr = ''
        for i,c in enumerate(op_list):
            n = c[j]
            nstr += n
        if nstr.strip():
            M.append(int(nstr.strip()))

    if op == '+':
        ans += sum(M)
    elif op == '*':
        prod = 1
        for num in M:
            prod *= num
        ans += prod
print("Final answer after applying operators:")
print(ans)