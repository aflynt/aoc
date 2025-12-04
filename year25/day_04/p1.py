from mylib import get_input, Grid2D

# input_data = get_input('ex.txt')
input_data = get_input('in.txt')

grid = Grid2D([list(line) for line in input_data])

# print(grid)

def count_at_chars_around(grid, x, y):
    directions = [(-1, -1), (0, -1), (1, -1),
                  (-1, 0),          (1, 0),
                  (-1, 1),  (0, 1),  (1, 1)]
    count = 0
    for dx, dy in directions:
        if grid.get(x + dx, y + dy) == '@':
            count += 1
    return count

def count_x_chars(grid):
    out_grid = grid.copy()

    count_x_chars = 0

    for y in range(grid.Y):
        for x in range(grid.X):
            if grid.get(x, y) == '@':
                at_count = count_at_chars_around(grid, x, y)
                if at_count < 4:
                    count_x_chars += 1
                    out_grid.set(x, y, 'x')
    
    return count_x_chars, out_grid

full_count = 0

print("Initial Grid:")
print(grid)

count, new_grid = count_x_chars(grid)
full_count += count
# Remove 'x' chars found.
print(f"\nGrid after placing 'x' chars: {count}")
print(new_grid)

print("\nGrid after clearing 'x' chars:")
new_grid.clear_x_chars()
print(new_grid)

iteration = 1

while count > 0:
    grid = new_grid.copy()
    count, new_grid = count_x_chars(grid)
    full_count += count
    print(f"\nGrid after placing 'x' chars: {count}")
    print(new_grid)
    print("\nGrid after clearing 'x' chars:")
    new_grid.clear_x_chars()
    print(new_grid)
    # write each new_grid to a file
    # iteration += 1
    # with open(f"grid_iteration_{iteration}.txt", "w") as f:
    #     f.write(str(new_grid))


print(f"\nTotal 'x' chars placed: {full_count}")
