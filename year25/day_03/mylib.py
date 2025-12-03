

def get_input(fname):
    with open(fname, 'r') as f:
        data = f.read().strip().split('\n')
    return data

class Battery:
    def __init__(self, bank=[], min_idx=0, max_idx=0):
        self.bank = bank
        self.min_idx = min_idx
        self.max_idx = max_idx
        self.max_charge, self.max_charge_idx = self.find_max_charge()

    def find_max_charge(self):
        max_charge = 0
        max_charge_idx = -1

        for idx in range(self.min_idx, self.max_idx + 1):
            charge = self.bank[idx]

            if charge > max_charge:
                max_charge = charge
                max_charge_idx = idx

        return max_charge, max_charge_idx
    def __repr__(self) -> str:
        return f"Battery(bank={self.bank}, min_idx={self.min_idx}, max_idx={self.max_idx}, max_charge={self.max_charge}, max_charge_idx={self.max_charge_idx})"
    def __str__(self) -> str:
        bstr = f"<{self.max_charge_idx}:{self.max_charge}>"
        return bstr