def get_lines(f):
    lines = []
    with open(f,'r') as f:
        lines = f.readlines()
        lines = [line.strip('\n') for line in lines]
        return lines

def get_nums(line, goodchars):
    # find (idx, chars) of number chars in substrings of line
    nums = []
    for i in range(len(line)):
        substr = line[i:] # search substring to get all numbers
        for gc in goodchars: # check each number_string
            if gc in substr:
                j = substr.find(gc) # find index of good_num
                nums.append((i+j,gc))
    
    nums = sorted(list(set(nums))) # sorted tuple of (idx, num_str)
    return nums

def get_vals(lines, goodchars):

    vals = []
    for line in lines:
        nums = get_nums(line, goodchars)
        n1 = nums[ 0] # get first
        n2 = nums[-1] # get last
        n1 = n1[1]    # pick 2nd of tuple
        n2 = n2[1]    # pick 2nd of tuple
        n1 = name2val[n1] # convert to 0-9 char
        n2 = name2val[n2] # convert to 0-9 char
        
        strval = f'{n1}{n2}' # mash chars together
        intval = int(strval) # convert to a number
        vals.append(intval)

    return vals

name2val = {'one': '1','two': '2','three': '3','four': '4','five': '5','six': '6','seven': '7','eight': '8','nine': '9','1': '1','2': '2','3': '3','4': '4','5': '5','6': '6','7': '7','8': '8','9': '9',}
goodchars1 = ['0','1','2','3','4','5','6','7','8','9']
goodchars2 = ['0','1','2','3','4','5','6','7','8','9','one','two','three','four','five','six','seven','eight','nine']

#f = 'test_data.txt'
f = 'in1.txt'
#f = 'test_data2.txt'

lines = get_lines(f)

vs1 = get_vals(lines, goodchars1)
vs2 = get_vals(lines, goodchars2)

print(f'sum1 = {sum(vs1)}')
print(f'sum2 = {sum(vs2)}')
