import math
import heapq
from algorithms.base import PathfindingAlgorithm

class Dijkstra(PathfindingAlgorithm):
    def find_path(self):
        # Reset
        for row in self.grid.nodes:
            for n in row:
                n.g = float('inf')
                n.parent = None

        start_node = self.grid.get_node(*self.start)
        start_node.g = 0.0

        pq = [(0.0, start_node)]
        visited = set()

        while pq:
            cost, current = heapq.heappop(pq)
            if (current.x, current.y) == self.goal:
                path = []
                while current:
                    path.append((current.x, current.y))
                    current = current.parent
                return path[::-1]

            if (current.x, current.y) in visited:
                continue
            visited.add((current.x, current.y))

            for nbr in self.grid.neighbors(current):
                dz = nbr.height - current.height
                step = math.sqrt((nbr.x-current.x)**2 + (nbr.y-current.y)**2 + dz*dz)
                new_cost = current.g + step
                if new_cost < nbr.g:
                    nbr.g = new_cost
                    nbr.parent = current
                    heapq.heappush(pq, (nbr.g, nbr))

        return []

def find_path(grid, start=None, goal=None):
    return Dijkstra(grid, start, goal).find_path()
