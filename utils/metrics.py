import math

def path_cost(path, grid):
    """Sum of 3D Euclidean distances between consecutive nodes."""
    total = 0.0
    for (x1,y1), (x2,y2) in zip(path, path[1:]):
        h1 = grid.get_height(x1, y1)
        h2 = grid.get_height(x2, y2)
        total += math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (h2 - h1)**2)
    return total
