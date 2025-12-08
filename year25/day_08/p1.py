
'''
Solution for Day 8: Connect junction boxes with light strings
Connect the 1000 closest pairs of junction boxes and find the
product of the sizes of the three largest resulting circuits.
'''
import math as m
from collections import defaultdict

class Box:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def distance(self, other):
        return m.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)
    
    def __repr__(self):
        return f"Box({self.x:3d}, {self.y:3d}, {self.z:3d})"
    
    def __str__(self) -> str:
        return f"({self.x:3d}, {self.y:3d}, {self.z:3d})"
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Box):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Box):
            return NotImplemented
        return (self.x, self.y, self.z) < (other.x, other.y, other.z)


class UnionFind:
    def __init__(self, items):
        self.parent = {item: item for item in items}
        self.rank = {item: 0 for item in items}
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return
        
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1


def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    boxes = []
    for line in lines:
        line = line.strip()
        if line:
            x, y, z = map(int, line.split(','))
            boxes.append(Box(x, y, z))
    return boxes


def get_all_pairs_with_distances(boxes):
    """Generate all unique pairs with their distances."""
    pairs = []
    n = len(boxes)
    for i in range(n):
        for j in range(i + 1, n):
            dist = boxes[i].distance(boxes[j])
            pairs.append((dist, boxes[i], boxes[j]))
    return pairs


def main():
    boxes = read_file("in.txt")
    print(f"Loaded {len(boxes)} boxes from in.txt")
    
    # Get all pairs sorted by distance
    all_pairs = get_all_pairs_with_distances(boxes)
    all_pairs.sort()  # Sort by distance
    print(f"Connecting {min(1000, len(all_pairs))} closest pairs...")
    
    # Connect the 1000 closest pairs using Union-Find
    uf = UnionFind(boxes)
    
    for i in range(min(1000, len(all_pairs))):
        dist, box1, box2 = all_pairs[i]
        uf.union(box1, box2)
    
    # Count circuit sizes
    circuit_sizes = defaultdict(int)
    for box in boxes:
        root = uf.find(box)
        circuit_sizes[root] += 1
    
    # Get the three largest circuits
    sizes = sorted(circuit_sizes.values(), reverse=True)
    
    print(f"Number of circuits: {len(sizes)}")
    print(f"Top 3 circuit sizes: {sizes[:3]}")
    
    if len(sizes) >= 3:
        result = sizes[0] * sizes[1] * sizes[2]
        print(f"Product of three largest circuits: {result}")
    else:
        print(f"Not enough circuits! Only {len(sizes)} circuits")
        if len(sizes) > 0:
            result = 1
            for size in sizes:
                result *= size
            print(f"Product of all circuits: {result}")


if __name__ == "__main__":
    main()