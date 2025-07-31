import random
from config import START, GOAL

class MovingObstacles:
    def __init__(self, grid, count=4):
        self.grid = grid
        self.positions = set()
        while len(self.positions) < count:
            x, y = random.randint(0, grid.width - 1), random.randint(0, grid.height - 1)
            if (x, y) not in [START, GOAL]:
                node = self.grid.get_node(x, y)
                
                # If it's a static obstacle, disable its static status
                if node.is_obstacle:
                    if hasattr(node, 'is_static_obs') and node.is_static_obs:
                        node.is_static_obs = False  # Remove static marking
                self.positions.add((x, y))
        self.update_grid()

    def update_grid(self):
        # Reset ONLY dynamic obstacles, keep static ones as they are
        for row in self.grid.nodes:
            for node in row:
                if not getattr(node, 'is_static_obs', False):
                    node.is_obstacle = False

        # Mark positions as obstacles
        for x, y in self.positions:
            node = self.grid.get_node(x, y)
            node.is_obstacle = True

    def move(self):
        new_positions = set()
        for (x, y) in self.positions:
            dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            nx, ny = max(0, min(self.grid.width - 1, x + dx)), max(0, min(self.grid.height - 1, y + dy))
            
            if (nx, ny) not in [START, GOAL]:
                node = self.grid.get_node(nx, ny)

                # If target is a static obstacle, disable it
                if node.is_obstacle and getattr(node, 'is_static_obs', False):
                    node.is_static_obs = False
                
                new_positions.add((nx, ny))
            else:
                new_positions.add((x, y))

        self.positions = new_positions
        self.update_grid()
