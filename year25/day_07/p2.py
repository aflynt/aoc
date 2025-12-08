from collections import defaultdict

def get_lines_from_file(filename):
    with open(filename, 'r') as file:
        return [line.rstrip('\n') for line in file]

class Grid2D:
    def __init__(self, lines):
        self.C = len(lines[0]) if lines else 0
        self.R = len(lines)
        self.grid = [[c for c in line] for line in lines]
        self.startC = lines[0].index('S') if 'S' in lines[0] else -1
        self.beamSplits = 0
        self.timelines = set()
        self.run_quantum_beam()

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
    
    def run_quantum_beam(self):
        """
        Simulate quantum tachyon splitting using many-worlds interpretation.
        Each splitter creates two timelines (left and right paths).
        
        Key insight: We need to track which (row, col) combinations are reachable.
        Multiple paths can lead to the same (row, col), but they count as different timelines
        only if they represent different final states.
        
        Actually, the problem asks for the number of different timelines - meaning we count
        the number of unique endpoints where a particle can end up.
        """
        
        # For each row, track which columns have particles in this iteration
        # Key: (row, col) -> number of ways to reach it (for counting different timelines)
        current_state = defaultdict(int)
        current_state[(1, self.startC)] = 1
        
        # Process row by row
        r = 1
        while r < self.R - 1:
            next_state = defaultdict(int)
            
            for (curr_r, curr_c), count in current_state.items():
                if curr_r != r:
                    # This shouldn't happen if we're processing sequentially
                    next_state[(curr_r, curr_c)] += count
                    continue
                
                next_r = r + 1
                next_cell = self.get_value(next_r, curr_c)
                
                if next_cell == '^':
                    # Splitter - each timeline splits into 2
                    # Left path
                    if 0 <= curr_c - 1 < self.C:
                        next_state[(next_r, curr_c - 1)] += count
                    # Right path
                    if 0 <= curr_c + 1 < self.C:
                        next_state[(next_r, curr_c + 1)] += count
                else:
                    # Continue straight down
                    next_state[(next_r, curr_c)] += count
            
            current_state = next_state
            r += 1
        
        # The number of timelines is the sum of all ways to reach any endpoint
        self.timelines = sum(current_state.values())


if __name__ == "__main__":
    # lines = get_lines_from_file("ex.txt")
    lines = get_lines_from_file("in.txt")
    grid = Grid2D(lines)
    
    print(f"Number of different timelines: {grid.timelines}")