import math
import heapq
from algorithms.base import PathfindingAlgorithm

class Dijkstra(PathfindingAlgorithm):
    def find_path(self):
        # Reset nodes
        for row in self.grid.nodes:
            for n in row:
                n.g = float('inf')
                n.parent = None

        start_node = self.grid.get_node(*self.start)
        start_node.g = 0.0

        pq = [(0.0, start_node)]
        visited = set()
        expanded_nodes = 0  # Track work units

        while pq:
            cost, current = heapq.heappop(pq)
            expanded_nodes += 1  # Count node expansions

            if (current.x, current.y) == self.goal:
                path = []
                while current:
                    path.append((current.x, current.y))
                    current = current.parent
                return path[::-1], expanded_nodes  # Return path + work units

            if (current.x, current.y) in visited:
                continue
            visited.add((current.x, current.y))

            for nbr in self.grid.neighbors(current):
                dz = abs(nbr.height - current.height)
                dx = nbr.x - current.x
                dy = nbr.y - current.y

                base_dist = math.sqrt(dx ** 2 + dy ** 2)
                penalty_factor = 1 + 2.0 * (dz ** 2)  # alpha = 2.0, power = 2
                segment_cost = (base_dist * penalty_factor) + (1.0 * (dz ** 2))  # beta = 1.0

                new_cost = current.g + segment_cost
                if new_cost < nbr.g:
                    nbr.g = new_cost
                    nbr.parent = current
                    heapq.heappush(pq, (nbr.g, nbr))

        return [], expanded_nodes

# Wrapper
def find_path(grid, start=None, goal=None):
    return Dijkstra(grid, start, goal).find_path()
