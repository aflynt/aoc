
from mylib import get_input, Battery


# data = get_input('ex.txt')
data = get_input('in.txt')

bank_charges = []

for line in data:
    print(line, end=' => ')
    b = len(line) # number of batteries
    p = 12 # number of battery picks
    d = b - p # number of batteries to discard
    bank = [int(x) for x in line]
    min_idx = 0
    bats = []
    for i in range(p):
        # make a battery with max index of i+d
        bat = Battery(bank=bank, min_idx=min_idx, max_idx=i+d)
        # print(bat, end=' ')        # update min_idx to one more than the max_charge_idx
        min_idx = bat.max_charge_idx + 1
        bats.append(bat)

    # concatenate the max charges
    total_charge = int(''.join([str(bat.max_charge) for bat in bats]))
    bank_charges.append(total_charge)
    print(total_charge)

# add up all the bank charges
final_total = sum(bank_charges)
print(f"Final total: {final_total}")