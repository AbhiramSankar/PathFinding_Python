import pygame
import sys
from config import START, GOAL

CELL = 30
MARGIN = 2

COLORS = {
    "A*": (0, 255, 255),        # Cyan
    "Dijkstra": (255, 255, 0),  # Yellow
    "GA": (255, 0, 255),        # Magenta
    "SA": (255, 128, 0),        # Orange
    "AD*": (0, 255, 128)        # Light Green
}

BACKGROUND_COLOR = (240, 240, 240)  # Light gray background

class Button:
    def __init__(self, text, x, y, w, h, color, hover_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, screen, font):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        current_color = self.color
        if self.rect.collidepoint(mouse):
            current_color = self.hover_color
            if click[0] and self.action:
                self.action()
        pygame.draw.rect(screen, current_color, self.rect, border_radius=8)
        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

def display_multiple(grid, algo_paths):
    pygame.init()
    legend_width = 140
    w = grid.width * CELL + (grid.width + 1) * MARGIN
    h = grid.height * CELL + (grid.height + 1) * MARGIN + 100
    screen_width = w + legend_width
    screen = pygame.display.set_mode((screen_width, h))
    pygame.display.set_caption("Pathfinding Visualization with UI & Height Legend")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 24)
    font_small = pygame.font.SysFont(None, 18)

    # UI Buttons
    buttons = []
    current_algo = None
    step = 0
    paused = False
    trigger_matplotlib = False

    def trigger_algorithm(label):
        nonlocal current_algo, step, paused
        current_algo = label
        step = 0
        paused = False

    def show_matplotlib():
        nonlocal trigger_matplotlib, running
        trigger_matplotlib = True
        running = False  # Exit loop safely


    # Algorithm buttons
    x_start = 10
    for algo_name in algo_paths.keys():
        btn = Button(algo_name, x_start, h - 60, 120, 40,
                     (200, 200, 200), (170, 170, 170),
                     lambda a=algo_name: trigger_algorithm(a))
        buttons.append(btn)
        x_start += 130

    # Add "Show Matplotlib" button
    matplotlib_btn = Button("Show Matplotlib", screen_width - 200, h - 60, 180, 40,
                            (0, 200, 100), (0, 170, 80), show_matplotlib)
    buttons.append(matplotlib_btn)

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:  # Pause/Resume
                    paused = not paused
                elif e.key == pygame.K_r:  # Reset
                    current_algo = None
                    step = 0
                    paused = False

        screen.fill(BACKGROUND_COLOR)

        # Draw grid
        for y in range(grid.height):
            for x in range(grid.width):
                node = grid.get_node(x, y)
                rect = pygame.Rect(MARGIN + x * (CELL + MARGIN),
                                    MARGIN + y * (CELL + MARGIN),
                                    CELL, CELL)
                if node.is_obstacle:
                    pygame.draw.rect(screen, (50, 50, 50), rect)
                else:
                    shade = int(255 * (1 - node.height))
                    pygame.draw.rect(screen, (shade, shade, shade), rect)

        # Draw Start & Goal
        sx, sy = START
        gx, gy = GOAL
        s_rect = pygame.Rect(MARGIN + sx * (CELL + MARGIN), MARGIN + sy * (CELL + MARGIN), CELL, CELL)
        g_rect = pygame.Rect(MARGIN + gx * (CELL + MARGIN), MARGIN + gy * (CELL + MARGIN), CELL, CELL)
        pygame.draw.rect(screen, (0, 255, 0), s_rect)  # Green for Start
        pygame.draw.rect(screen, (255, 0, 0), g_rect)  # Red for Goal

        # Draw Buttons
        for btn in buttons:
            btn.draw(screen, font)

        # Animate selected algorithm path
        if current_algo:
            path = algo_paths[current_algo]
            color = COLORS.get(current_algo, (255, 255, 255))
            for i in range(min(step, len(path))):
                x, y = path[i]
                rect = pygame.Rect(MARGIN + x * (CELL + MARGIN),
                                    MARGIN + y * (CELL + MARGIN),
                                    CELL, CELL)
                pygame.draw.rect(screen, color, rect)

            if not paused and step < len(path):
                step += 1

            # Show status text
            status_text = f"Showing: {current_algo} | SPACE=Pause | R=Reset"
            txt_surface = font.render(status_text, True, (0, 0, 0))
            screen.blit(txt_surface, (10, 10))

        # Draw Height Legend
        legend_x = w + 20
        legend_y = 50
        legend_height = grid.height * CELL

        for i in range(legend_height):
            ratio = (i / legend_height)  # top=high, bottom=low
            color = (int(255 * ratio), int(255 * ratio), int(255 * ratio))
            pygame.draw.line(screen, color, (legend_x, legend_y + i), (legend_x + 20, legend_y + i))

        # Legend labels
        high_text = font_small.render("High", True, (0, 0, 0))
        low_text = font_small.render("Low", True, (0, 0, 0))
        screen.blit(high_text, (legend_x + 30, legend_y - 10))
        screen.blit(low_text, (legend_x + 30, legend_y + legend_height - 10))

        pygame.display.flip()
        clock.tick(10)  # Animation speed

    pygame.quit()
    if trigger_matplotlib:
        return "run_matplotlib"
    else:
        sys.exit()
