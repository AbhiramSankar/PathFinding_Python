import math

def path_length(path, grid, alpha=2.0, power=2):
    """
    Path length with adaptive elevation penalty.
    alpha: penalty factor for slope
    power: exponent for slope steepness
    """
    if not path or len(path) < 2:
        return 0.0

    total_length = 0.0
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        node1 = grid.get_node(x1, y1)
        node2 = grid.get_node(x2, y2)

        dx, dy = x2 - x1, y2 - y1
        dz = abs(node2.height - node1.height)

        # Base horizontal distance
        base_dist = math.sqrt(dx**2 + dy**2)

        # Adaptive penalty
        penalty_factor = 1 + alpha * (dz ** power)
        segment_length = base_dist * penalty_factor

        total_length += segment_length

    return round(total_length, 4)


def path_cost(path, grid, alpha=2.0, beta=1.0, power=2):
    """
    Path cost with adaptive elevation penalty.
    alpha: penalty factor for slope applied to length
    beta: additional cost for elevation change
    power: exponent for slope steepness
    """
    if not path or len(path) < 2:
        return 0.0

    total_cost = 0.0
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        node1 = grid.get_node(x1, y1)
        node2 = grid.get_node(x2, y2)

        dx, dy = x2 - x1, y2 - y1
        dz = abs(node2.height - node1.height)

        # Base horizontal distance
        base_dist = math.sqrt(dx**2 + dy**2)

        # Adaptive penalties
        penalty_factor = 1 + alpha * (dz ** power)
        segment_cost = (base_dist * penalty_factor) + (beta * (dz ** power))

        total_cost += segment_cost

    return round(total_cost, 4)