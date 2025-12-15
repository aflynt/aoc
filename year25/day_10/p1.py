from itertools import product

class Machine:
    def __init__(self, ans, buttons):
        self.state = [ 0 for _ in range(len(ans)) ]
        self.ans = ans
        self.buttons = buttons
    def press(self, button_index):
        if button_index < 0 or button_index >= len(self.buttons):
            raise ValueError("Invalid button index")

        button = self.buttons[button_index]
        for state_idx in button:
            # toggle state at index i
            curr_state = self.state[state_idx]
            if curr_state == 1:
                self.state[state_idx] = 0
            else:
                self.state[state_idx] = 1
    def print_state(self):
        print(self.state)
    
    def is_solved(self):
        return self.state == self.ans


def read_file(file_path):
    

    with open(file_path, 'r') as file:
        content = file.read().splitlines()

        ms = []
        for line in content:
            f,e = line.split(']')
            f = f[1:]
            e,j = e.split("{")
            e = e.strip()
            j = j[:-1]
            f = [1 if x == '#' else 0 for x in f]
            # ignore j for now

            buttons = []
            bs = e.split(' ')
            for b in bs:
                estr = b.strip("(")
                estr = estr.strip(")")
                nums = [int(x) for x in estr.split(',')]
                buttons.append(nums)
            ms.append((f,buttons))
        return ms


def main():
    # file_path = "ex.txt"
    file_path = "in.txt"
    ms = read_file(file_path)

    # ms = [ms[0]]  # only use first machine for now
    all_sum = 0

    for m in ms:
        ans, buttons = m

        ok_combos = []

        for button_indices in product(range(2), repeat=len(buttons)):
            machine = Machine(ans, buttons)
            # print("Button indices:", button_indices)
            for b, pressed in enumerate(button_indices):
                if pressed:
                    machine.press(b)

                    if machine.is_solved():
                        # print("Solved with button indices:", button_indices)
                        ok_combos.append(button_indices)

        
        min_sum = min([sum(x) for x in ok_combos])
        print("Minimum sum of button presses:", min_sum, "for machine with answer:", ans)
        all_sum += min_sum

    print("Total sum of minimum button presses for all machines:", all_sum)




if __name__ == "__main__":
    main()