
def get_lines_from_file(filename):
    with open(filename, 'r') as file:
        return [line.rstrip('\n') for line in file]

class Grid2D:
    def __init__(self, lines ):
        self.C = len(lines[0]) if lines else 0
        self.R = len(lines)
        self.grid = [[c for c in line] for line in lines]
        self.startC = lines[0].index('S') if 'S' in lines[0] else -1 
        self.beamSplits = 0
        self.run_beam()

    def set_value(self, r, c, value):
        if 0 <= c < self.C and 0 <= r < self.R:
            self.grid[r][c] = value
        else:
            raise IndexError("Coordinates out of bounds")

    def get_value(self, r, c):
        if 0 <= c < self.C and 0 <= r < self.R:
            return self.grid[r][c]
        else:
            raise IndexError("Coordinates out of bounds")

    def __str__(self):
        return '\n'.join([''.join(map(str, row)) for row in self.grid])
    
    def run_beam(self):
        # beam running logic
        r = 1
        # place initial beam below start
        self.set_value(r, self.startC, '|')
        r += 1
        while r < self.R:
            for c in range(self.C):
                current_value = self.get_value(r, c)
                val_above = self.get_value(r - 1, c)
                if current_value == '^' and val_above == '|':
                    # beam hits a splitter and splits in two
                    #assert False, f"Beam split at ({r},{c})"
                    self.beamSplits += 1
                    self.set_value(r, c-1, '|')
                    self.set_value(r, c+1, '|')
                elif val_above == '|':
                    # beam continues down
                    self.set_value(r, c, '|')
            r += 1

if __name__ == "__main__":
    # lines = get_lines_from_file("ex.txt")
    lines = get_lines_from_file("in.txt")
    grid = Grid2D(lines)
    print("Initial Grid:")
    print(grid)

    print(f"Value at (0, {grid.startC}): {grid.get_value(0, grid.startC)}")
    print(f"Beam splits: {grid.beamSplits}")
