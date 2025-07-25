import math
import heapq
from algorithms.base import PathfindingAlgorithm

class AStar(PathfindingAlgorithm):
    def heuristic(self, node):
        gx, gy = self.goal
        dx = gx - node.x
        dy = gy - node.y
        dh = self.grid.get_height(gx, gy) - node.height
        return math.sqrt(dx*dx + dy*dy + dh*dh)

    def find_path(self):
        # Reset nodes
        for row in self.grid.nodes:
            for n in row:
                n.g = float('inf')
                n.h = 0.0
                n.f = float('inf')
                n.parent = None

        start_node = self.grid.get_node(*self.start)
        goal_node  = self.grid.get_node(*self.goal)

        start_node.g = 0.0
        start_node.h = self.heuristic(start_node)
        start_node.f = start_node.h

        open_set = [(start_node.f, start_node)]
        closed  = set()

        while open_set:
            _, current = heapq.heappop(open_set)
            if (current.x, current.y) == self.goal:
                path = []
                while current:
                    path.append((current.x, current.y))
                    current = current.parent
                return path[::-1]

            closed.add((current.x, current.y))

            for nbr in self.grid.neighbors(current):
                if (nbr.x, nbr.y) in closed:
                    continue
                dz = nbr.height - current.height
                dist = math.sqrt((nbr.x-current.x)**2 + (nbr.y-current.y)**2 + dz*dz)
                tentative_g = current.g + dist

                if tentative_g < nbr.g:
                    nbr.parent = current
                    nbr.g = tentative_g
                    nbr.h = self.heuristic(nbr)
                    nbr.f = nbr.g + nbr.h
                    heapq.heappush(open_set, (nbr.f, nbr))

        return []

def find_path(grid, start=None, goal=None):
    return AStar(grid, start, goal).find_path()
