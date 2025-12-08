
'''
Solution for Day 8 Part 2: Connect all junction boxes into one circuit
Find the last connection that merges all circuits and multiply X coordinates.
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
        self.num_components = len(items)
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in same component
        
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        self.num_components -= 1
        return True


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
    print(f"Total pairs to consider: {len(all_pairs)}")
    
    # Connect pairs using Union-Find until all are in one component
    uf = UnionFind(boxes)
    last_box1, last_box2 = None, None
    connections_made = 0
    
    for dist, box1, box2 in all_pairs:
        if uf.union(box1, box2):
            connections_made += 1
            last_box1, last_box2 = box1, box2
            
            if uf.num_components == 1:
                print(f"All boxes connected into one circuit after {connections_made} connections")
                print(f"Last connection: {box1} to {box2}")
                print(f"Distance: {dist:.2f}")
                result = box1.x * box2.x
                print(f"Product of X coordinates: {box1.x} × {box2.x} = {result}")
                break


if __name__ == "__main__":
    main()
