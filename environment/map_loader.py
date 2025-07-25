import random
import config

def load_heightmap():
    """Generate a random heightmap of size GRID_WIDTH x GRID_HEIGHT."""
    return [
        [random.random() for _ in range(config.GRID_WIDTH)]
        for _ in range(config.GRID_HEIGHT)
    ]
