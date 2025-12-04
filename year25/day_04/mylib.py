def get_input(fname):
    with open(fname, 'r') as f:
        data = f.read().strip().splitlines()
    return data

class Grid2D:
    def __init__(self, grid):
        self.grid = grid
        self.X = len(grid[0]) if grid else 0
        self.Y = len(grid)

    def get(self, x, y):
        if x < 0 or y < 0 or y >= self.Y or x >= self.X:
            return "."
        return self.grid[y][x]

    def set(self, x, y, value):
        self.grid[y][x] = value

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)

    def clear_x_chars(self):
        for y in range(self.Y):
            for x in range(self.X):
                if self.get(x, y) == 'x':
                    self.set(x, y, '.')
    
    def copy(self):
        new_grid = [row[:] for row in self.grid]
        return Grid2D(new_grid)
