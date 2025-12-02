import re

lines = open('in.txt', 'r').readlines()
# lines = open('ex.txt', 'r').readlines()

p1_id_sum = 0
p2_id_sum = 0

hit_count = 0

for line in lines:
    # print(line.strip())

    # split on dashes
    parts = line.strip().split('-')
    begin = int(parts[0])
    end   = int(parts[1])
    count = end - begin + 1
    print(f'\nCount from {begin} to {end} is {count}')

    # loop through range
    for i in range(begin, end + 1):
        # print(f'  Number: {i}')
        # convert to string
        s = str(i)

        # find the invalid IDs by looking for any ID 
        # which is made only of some sequence of digits repeated twice. 
        # So, 55 (5 twice), 6464 (64 twice), and 123123 (123 twice) would all be invalid IDs.

        repeat_regex = re.compile(r'^(.*)\1$')
        if repeat_regex.match(s):
            # print(f'    Invalid ID (p1): {s}')
            print("_", end="")
            p1_id_sum += i
            hit_count += 1

        # Now, an ID is invalid if it is made only of some sequence
        # of digits repeated at least twice. 
        # So, 12341234 (1234 two times), 
        # 123123123 (123 three times), 
        # 1212121212 (12 five times), 
        # and 1111111 (1 seven times) are all invalid IDs

        sequence_regex = re.compile(r'^(.*?)(\1+)$')

        # if repeat_regex.match(s):
        if sequence_regex.match(s):
            # print(f'    Invalid ID (p2): {s}')
            print(".", end="")
            p2_id_sum += i
            hit_count += 1

        if hit_count >= 50:
            print()
            hit_count = 0

# sum the bad IDs
print(f'Total sum of bad IDs (p1): {p1_id_sum}')
print(f'Total sum of bad IDs (p2): {p2_id_sum}')


