from dataclasses import dataclass, field

@dataclass
class Node:
    x: int
    y: int
    height: float = 0.0
    is_obstacle: bool = False
    g: float = field(default=float('inf'), init=False)
    h: float = field(default=0.0, init=False)
    f: float = field(default=float('inf'), init=False)
    parent: 'Node' = field(default=None, init=False)
