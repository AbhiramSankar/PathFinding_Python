import matplotlib.pyplot as plt
import matplotlib.animation as animation
from config import START, GOAL

def animate(grid, path):
    fig, ax = plt.subplots()
    # show heightmap
    hmap = [
        [grid.get_height(x, y) for x in range(grid.width)]
        for y in range(grid.height)
    ]
    cax = ax.imshow(hmap, cmap='terrain', origin='lower')
    fig.colorbar(cax, ax=ax)

    # overlay obstacles
    obs = [
        (n.x, n.y)
        for row in grid.nodes for n in row
        if n.is_obstacle
    ]
    if obs:
        xs, ys = zip(*obs)
        ax.scatter(xs, ys, marker='s', color='black', s=20)

    line, = ax.plot([], [], 'bo-')

    def init():
        line.set_data([], [])
        return line,

    def update(i):
        xs = [p[0] for p in path[:i+1]]
        ys = [p[1] for p in path[:i+1]]
        line.set_data(xs, ys)
        return line,

    ani = animation.FuncAnimation(
        fig, update, frames=len(path),
        init_func=init, interval=200, blit=True, repeat=False
    )

    plt.scatter(*START, c='green', s=100, marker='*')
    plt.scatter(*GOAL,  c='red',   s=100, marker='X')
    plt.title("Pathfinding Animation")
    plt.show()

def animate_multiple(grid, algo_paths):
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from config import START, GOAL

    fig, ax = plt.subplots()
    hmap = [
        [grid.get_height(x, y) for x in range(grid.width)]
        for y in range(grid.height)
    ]
    cax = ax.imshow(hmap, cmap='terrain', origin='lower')
    fig.colorbar(cax, ax=ax)

    COLORS = {
        "A*": "cyan",
        "AD*": "limegreen",
        "Dijkstra": "yellow",
        "GA": "magenta",
        "SA": "orange",
    }

    LINE_STYLES = {
        "A*": '-',
        "AD*": '-',
        "Dijkstra": '--',
        "GA": '-.',
        "SA": ':',
    }

    MARKERS = {
        "A*": 'o',
        "AD*": 'P',
        "Dijkstra": 's',
        "GA": '^',
        "SA": 'D',
    }

    plots = {}
    for i, name in enumerate(algo_paths):
        plots[name], = ax.plot([], [], 
                               label=name,
                               color=COLORS[name],
                               linestyle=LINE_STYLES[name],
                               marker=MARKERS[name],
                               linewidth=2.0,
                               markersize=6,
                               markeredgecolor='black',
                               markeredgewidth=0.8,
                               alpha=0.85)

    # Start & goal points
    ax.scatter(*START, color='green', s=100, marker='*', edgecolors='black')
    ax.scatter(*GOAL,  color='red',   s=100, marker='X', edgecolors='black')

    ax.set_title("Animated Path Comparison Across Algorithms")

    # Move legend to the left
    ax.legend(loc='upper left', bbox_to_anchor=(-0.05, 1.0), frameon=True)

    max_len = max(len(p) for p in algo_paths.values())

    def update(frame):
        for name, path in algo_paths.items():
            xs = [p[0] for p in path[:frame+1]]
            ys = [p[1] for p in path[:frame+1]]
            plots[name].set_data(xs, ys)
        return list(plots.values())

    ani = animation.FuncAnimation(
        fig, update, frames=max_len,
        interval=300, blit=True, repeat=False
    )

    plt.tight_layout()
    plt.show()
