import pygame
import sys
import config
from config import START, GOAL

CELL = 30
MARGIN = 2

def display(grid, path):
    pygame.init()
    w = grid.width * CELL + (grid.width + 1) * MARGIN
    h = grid.height * CELL + (grid.height + 1) * MARGIN
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Pathfinding Visualization")
    clock = pygame.time.Clock()

    WHITE = (255,255,255)
    BLACK = (0,0,0)
    GREEN = (0,255,0)
    RED   = (255,0,0)

    font = pygame.font.SysFont(None, 12)

    step = 0
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        # Draw base grid
        for y in range(grid.height):
            for x in range(grid.width):
                node = grid.get_node(x, y)
                rect = pygame.Rect(
                    MARGIN + x * (CELL + MARGIN),
                    MARGIN + y * (CELL + MARGIN),
                    CELL, CELL
                )
                if node.is_obstacle:
                    color = BLACK
                else:
                    shade = int(255 * (1 - node.height))
                    color = (shade, shade, shade)
                pygame.draw.rect(screen, color, rect)

        # Animate the path gradually with elevation-based coloring
        for i in range(min(step, len(path))):
            x, y = path[i]
            node = grid.get_node(x, y)
            rect = pygame.Rect(
                MARGIN + x * (CELL + MARGIN),
                MARGIN + y * (CELL + MARGIN),
                CELL, CELL
            )
            # Color by height: low = blue, high = red
            elevation = node.height
            r = int(elevation * 255)
            b = int((1 - elevation) * 255)
            pygame.draw.rect(screen, (r, 0, b), rect)

            # Optional: show height value
            text = font.render(f"{elevation:.2f}", True, WHITE)
            screen.blit(text, (rect.x + 2, rect.y + 2))

        # start & goal
        sx, sy = config.START
        gx, gy = config.GOAL
        s_rect = pygame.Rect(MARGIN + sx * (CELL + MARGIN), MARGIN + sy * (CELL + MARGIN), CELL, CELL)
        g_rect = pygame.Rect(MARGIN + gx * (CELL + MARGIN), MARGIN + gy * (CELL + MARGIN), CELL, CELL)
        pygame.draw.rect(screen, GREEN, s_rect)
        pygame.draw.rect(screen, RED, g_rect)

        pygame.display.flip()
        clock.tick(10)
        if step < len(path):
            step += 1

    pygame.quit()
    sys.exit()
    
def display_multiple(grid, algo_paths):
    pygame.init()
    CELL = 30
    MARGIN = 2
    w = grid.width * CELL + (grid.width + 1) * MARGIN
    h = grid.height * CELL + (grid.height + 1) * MARGIN
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Animated Algorithm Paths with Elevation")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 18)

    COLORS = {
        "A*": (0, 255, 255),        # Cyan
        "AD*": (0, 255, 128),       # Light Green for AD*
        "Dijkstra": (255, 255, 0), # Yellow
        "GA": (255, 0, 255),       # Magenta
        "SA": (255, 128, 0)       # Orange
    }

    running = True
    paused = False
    trigger_matplotlib = False
    algo_keys = list(algo_paths.keys())
    algo_index = 0
    step = 0
    delay = 5  # slower animation (was 15)

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    paused = not paused
                elif e.key == pygame.K_r:
                    algo_index = 0
                    step = 0
                    paused = False
                elif e.key == pygame.K_m:
                    trigger_matplotlib = True
                    running = False

        screen.fill((0, 0, 0))

        # draw terrain grid with elevation
        for y in range(grid.height):
            for x in range(grid.width):
                node = grid.get_node(x, y)
                rect = pygame.Rect(
                    MARGIN + x * (CELL + MARGIN),
                    MARGIN + y * (CELL + MARGIN),
                    CELL, CELL
                )
                if node.is_obstacle:
                    pygame.draw.rect(screen, (0, 0, 0), rect)
                else:
                    shade = int(255 * (1 - node.height))
                    color = (shade, shade, shade)
                    pygame.draw.rect(screen, color, rect)

        # draw legend on right
        y_offset = 5
        legend_x = grid.width * (CELL + MARGIN) - 120
        for name, color in COLORS.items():
            txt = font.render(name, True, color)
            screen.blit(txt, (legend_x, y_offset))
            y_offset += 20

        # draw start & goal
        sx, sy = START
        gx, gy = GOAL
        s_rect = pygame.Rect(MARGIN + sx * (CELL + MARGIN), MARGIN + sy * (CELL + MARGIN), CELL, CELL)
        g_rect = pygame.Rect(MARGIN + gx * (CELL + MARGIN), MARGIN + gy * (CELL + MARGIN), CELL, CELL)
        pygame.draw.rect(screen, (0, 255, 0), s_rect)
        pygame.draw.rect(screen, (255, 0, 0), g_rect)

        # draw current algorithm path
        if algo_index < len(algo_keys):
            label = algo_keys[algo_index]
            path = algo_paths[label]
            color = COLORS[label]

            for i in range(min(step, len(path))):
                x, y = path[i]
                node = grid.get_node(x, y)
                rect = pygame.Rect(
                    MARGIN + x * (CELL + MARGIN),
                    MARGIN + y * (CELL + MARGIN),
                    CELL, CELL
                )
                elev = node.height
                r = int(elev * 255)
                b = int((1 - elev) * 255)
                pygame.draw.rect(screen, (r, 0, b), rect)

                text = font.render(f"{elev:.2f}", True, (255, 255, 255))
                screen.blit(text, (rect.x + 2, rect.y + 2))

            label_text = font.render(f"Now Showing: {label}", True, color)
            screen.blit(label_text, (grid.width * CELL // 2 - 50, 5))

            if not paused:
                if step < len(path):
                    step += 1
                else:
                    step = 0
                    algo_index += 1
                    pygame.time.delay(500)

        else:
            end_text = font.render("All Algorithms Done - Press R to Replay or Close to Exit", True, (255, 255, 255))
            screen.blit(end_text, (grid.width * CELL // 2 - 150, 5))

        # draw pause text
        if paused:
            pause_text = font.render("Paused - Press SPACE to Resume", True, (255, 255, 255))
            screen.blit(pause_text, (grid.width * CELL // 2 - 100, 30))

        pygame.display.flip()
        clock.tick(delay)

    pygame.quit()
    if trigger_matplotlib:
        return "run_matplotlib"
    else:
        sys.exit()
