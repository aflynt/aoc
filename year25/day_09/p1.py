from itertools import combinations, permutations

def get_input(fname):
    coords = []
    with open(fname, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                coords.append(tuple(map(int, line.split(','))))
    return coords

def get_largest_area_part1(coords):
    # Part 1: largest rectangle that can be formed by any two coordinates
    if not coords:
        return 0
    
    largest_area = 0
    for i, ps in enumerate(combinations(coords, 2)):
        p1, p2 = ps
        p1x = p1[0]
        p1y = p1[1]
        p2x = p2[0]
        p2y = p2[1]
        dx = abs(p2x - p1x) + 1
        dy = abs(p2y - p1y) + 1
        area = dx * dy
        if area > largest_area:
            largest_area = area
            print(f"Rectangle formed by {p1} and {p2} has area: {area}")
        else:
            print(f".", end="")
        if i % 100 == 0:
            print(f"{i:3d}")
    return largest_area

def precompute_red_green_tiles(coords):
    """Precompute all red and green tiles"""
    red_green = set()
    n = len(coords)
    
    # Add red tiles
    red_green.update(coords)
    
    # Add green tiles (on the paths connecting red tiles)
    for i in range(n):
        curr = coords[i]
        next_tile = coords[(i + 1) % n]
        
        curr_x, curr_y = curr
        next_x, next_y = next_tile
        
        # Add all tiles on the line between curr and next_tile
        if curr_x == next_x:  # Vertical line
            start_y = min(curr_y, next_y)
            end_y = max(curr_y, next_y)
            for y in range(start_y, end_y + 1):
                red_green.add((curr_x, y))
        elif curr_y == next_y:  # Horizontal line
            start_x = min(curr_x, next_x)
            end_x = max(curr_x, next_x)
            for x in range(start_x, end_x + 1):
                red_green.add((x, curr_y))
    
    # Add tiles inside the polygon using ray casting algorithm
    min_x = min(c[0] for c in coords)
    max_x = max(c[0] for c in coords)
    min_y = min(c[1] for c in coords)
    max_y = max(c[1] for c in coords)
    
    for y in range(min_y, max_y + 1):
        # Find all x intersections with edges at this y
        intersections = []
        for i in range(n):
            p1 = coords[i]
            p2 = coords[(i + 1) % n]
            
            y1, y2 = p1[1], p2[1]
            x1, x2 = p1[0], p2[0]
            
            if y1 == y2:  # Horizontal edge, skip
                continue
            
            # Check if this edge intersects the horizontal line at y
            if min(y1, y2) < y <= max(y1, y2):
                # Calculate x coordinate of intersection
                if y2 != y1:
                    t = (y - y1) / (y2 - y1)
                    x_intersect = x1 + t * (x2 - x1)
                    intersections.append(x_intersect)
        
        # Sort and pair intersections
        intersections.sort()
        for j in range(0, len(intersections) - 1, 2):
            x_start = int(intersections[j])
            x_end = int(intersections[j + 1])
            for x in range(x_start, x_end + 1):
                red_green.add((x, y))
    
    return red_green

def get_largest_area_part2(coords):
    """Part 2: largest rectangle using only red and green tiles"""
    if not coords:
        return 0
    
    # Precompute red and green tiles
    red_green = precompute_red_green_tiles(coords)
    red_green_set = red_green
    
    largest_area = 0
    best_rect = None
    total = len(list(combinations(coords, 2)))
    
    for i, ps in enumerate(combinations(coords, 2)):
        p1, p2 = ps
        p1x, p1y = p1
        p2x, p2y = p2
        
        # Get the bounding box
        min_x = min(p1x, p2x)
        max_x = max(p1x, p2x)
        min_y = min(p1y, p2y)
        max_y = max(p1y, p2y)
        
        # Check if ALL tiles in the rectangle are red or green
        all_valid = True
        valid_count = 0
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if (x, y) in red_green_set:
                    valid_count += 1
                else:
                    all_valid = False
                    break
            if not all_valid:
                break
        
        # The rectangle is only valid if all tiles are red or green
        if all_valid:
            area = valid_count
            
            if area > largest_area:
                largest_area = area
                best_rect = (p1, p2)
                print(f"Rectangle from {p1} to {p2}: area = {area}")
        
        if (i + 1) % 100 == 0:
            print(f"{i+1}/{total}", end=" ", flush=True)
    
    print()
    return largest_area

def main():
    fnames = ['in.txt', 'ex.txt']
    
    # Part 2
    print("=== PART 2 ===")
    data = get_input(fnames[0])
    Amax2 = get_largest_area_part2(data)
    print(f"Largest area (Part 2): {Amax2}")

if __name__ == "__main__":
    main()