import pygame
import time
import os
import imageio
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from ui.buttons import Button
from ui.obstacles import MovingObstacles
from utils.path_utils import normalize_path
from utils.logger import log_results_csv, log_convergence_csv, log_computing_power
from utils.metrics import path_cost, path_length
from environment.grid import Grid
from config import START, GOAL, OBSTACLE_COUNT
from algorithms import astar, dijkstra, adstar, genetic, simulated_annealing, ssa

# ==== SETTINGS ====
CELL_SIZE = 20
MARGIN = 2
UPDATE_INTERVAL = 40
ANIMATION_DELAY = 20
BACKGROUND_COLOR = (245, 245, 245)
RESULTS_DIR = "results"
PANEL_WIDTH = 350
GRID_MARGIN = 20

COLORS = {
    "A*": (0, 200, 255),
    "Dijkstra": (255, 255, 0),
    "GA": (255, 0, 255),
    "SA": (255, 128, 0),
    "AD*": (0, 255, 128),
    "SSA": (128, 0, 255)
}

# Define colors as constants at the top of your file
COLOR_START = (34, 139, 34)
COLOR_GOAL = (227, 66, 52)
COLOR_STATIC_OBS = (63, 0, 255)
COLOR_MOVING_OBS = (255, 95, 21)

convergence_data = {"GA": [], "SA": [], "SSA": []}
performance_data = []

if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

def dynamic_visualization():
    pygame.init()
    pygame.font.init()

    grid = Grid()
    grid_area_width = grid.width * (CELL_SIZE + MARGIN)
    grid_area_height = grid.height * (CELL_SIZE + MARGIN)
    screen_width = grid_area_width + PANEL_WIDTH + GRID_MARGIN
    screen_height = grid_area_height + 250  # Adjust for extra buttons

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Dynamic Pathfinding")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 24)
    font_small = pygame.font.SysFont(None, 20)
    font_heading = pygame.font.SysFont(None, 28, bold=True)

    obstacles = MovingObstacles(grid, count=OBSTACLE_COUNT)
    algo_name = "AD*"
    algo_funcs = {
        "A*": astar.find_path,
        "Dijkstra": dijkstra.find_path,
        "AD*": adstar.find_path,
        "GA": genetic.find_path,
        "SA": simulated_annealing.find_path,
        "SSA": ssa.find_path
    }

    sidebar_x = grid_area_width + GRID_MARGIN
    button_width = 150
    button_height = 40
    button_spacing = 10

    trigger_matplotlib = False
    exit_simulation = False
    animate_path = []
    path_step = 0
    metrics = {"time": 0, "length": 0, "cost": 0, "ops": 0}

    buttons = []

    # GIF Settings
    frames = []
    gif_filename = f"results/simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.gif"
    gif_fps = 15
    frame_skip = 2
    recording = False  # Recording toggle state

    # --- Button Functions ---
    def set_algo(name):
        nonlocal algo_name, animate_path, metrics, path_step
        algo_name = name
        t0 = time.time()
        result = algo_funcs[name](grid)
        exec_time = round(time.time() - t0, 4)

        convergence = []
        work_units = 0

        if name in ["GA", "SA", "SSA"]:
            if isinstance(result, tuple) and len(result) >= 2:
                animate_path = normalize_path(result[0])
                convergence = result[1]
                work_units = result[2] if len(result) > 2 else 0
            else:
                animate_path = normalize_path(result)

            if convergence:
                convergence_data[name] = convergence
                log_convergence_csv(os.path.join(RESULTS_DIR, f"{name.lower()}_convergence.csv"),
                                     convergence, name)
        else:
            if isinstance(result, tuple) and len(result) == 2:
                animate_path = normalize_path(result[0])
                work_units = result[1]
            else:
                animate_path = normalize_path(result)

        OPS = work_units / exec_time if exec_time > 0 else 0
        length = path_length(animate_path, grid)
        cost = path_cost(animate_path, grid)
        metrics = {"time": exec_time, "length": length, "cost": cost, "ops": OPS}
        path_step = 0

        row = {
            "Algorithm": name,
            "Time (s)": exec_time,
            "Path Length (Adaptive 3D)": length,
            "Path Cost (Adaptive Elevation)": cost,
            "Computing Power (OPS)": OPS
        }
        performance_data.append(row)
        log_results_csv(os.path.join(RESULTS_DIR, "performance_metrics.csv"), [row])
        log_computing_power(os.path.join(RESULTS_DIR, "computing_power.csv"), name, exec_time, work_units)

    def reset_simulation():
        nonlocal grid, obstacles, animate_path, metrics, path_step
        grid = Grid()
        obstacles = MovingObstacles(grid, count=OBSTACLE_COUNT)
        animate_path = []
        path_step = 0
        metrics = {"time": 0, "length": 0, "cost": 0, "ops": 0}

    def toggle_recording():
        nonlocal recording, frames
        recording = not recording
        if not recording and frames:
            print(f"Saving GIF as {gif_filename} with {len(frames)} frames...")
            imageio.mimsave(gif_filename, frames, fps=gif_fps)
            frames = []
            print(f"GIF saved as {gif_filename}")

    def take_screenshot():
        filename = f"results/screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pygame.image.save(screen, filename)
        print(f"Screenshot saved as {filename}")

    def set_flag(flag):
        nonlocal trigger_matplotlib, exit_simulation, running
        if flag == "matplotlib":
            trigger_matplotlib = True
            running = False
        elif flag == "exit":
            exit_simulation = True
            running = False

    # Arrange Buttons
    def arrange_buttons():
        buttons.clear()
        x, y = 20, grid_area_height + 20

        # Row 1: Algorithms
        for algo in algo_funcs.keys():
            buttons.append(Button(algo, x, y, button_width, button_height, (200, 200, 200), (170, 170, 170),
                                  lambda a=algo: set_algo(a)))
            x += button_width + button_spacing

        # Row 2: Controls
        y += button_height + button_spacing
        x = 20
        for text, color, hover_color, func in [
            ("Reset Grid", (100, 149, 237), (65, 105, 225), reset_simulation),
            ("Show Matplotlib", (0, 200, 100), (0, 170, 80), lambda: set_flag("matplotlib")),
            ("Exit Simulation", (200, 80, 80), (170, 50, 50), lambda: set_flag("exit")),
            ("Start Recording", (255, 215, 0), (220, 180, 0), toggle_recording),
            ("Screenshot", (100, 200, 255), (80, 170, 230), take_screenshot)
        ]:
            buttons.append(Button(text, x, y, button_width, button_height, color, hover_color, func))
            x += button_width + button_spacing

        return y + button_height + 100

    screen_height = arrange_buttons()
    pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    # --- Main Loop ---
    frame_count = 0
    running = True
    
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit_simulation = True
                running = False

        frame_count += 1
        if frame_count % UPDATE_INTERVAL == 0:
            obstacles.move()
            if any(pos in obstacles.positions for pos in animate_path):
                set_algo(algo_name)

        screen.fill(BACKGROUND_COLOR)

        # Draw Grid
        for y in range(grid.height):
            for x in range(grid.width):
                node = grid.get_node(x, y)
                rect = pygame.Rect(MARGIN + x * (CELL_SIZE + MARGIN),
                                    MARGIN + y * (CELL_SIZE + MARGIN),
                                    CELL_SIZE, CELL_SIZE)

                # Drawing logic
                if (node.x, node.y) == START:
                    color = COLOR_START
                elif (node.x, node.y) == GOAL:
                    color = COLOR_GOAL
                elif node.is_obstacle:
                    color = COLOR_STATIC_OBS if node.is_static_obs else COLOR_MOVING_OBS
                else:
                    shade = int(255 * (1 - node.height))  # Scale height to grayscale
                    color = (shade, shade, shade)

                pygame.draw.rect(screen, color, rect)

        # Animate Path
        if animate_path:
            for i in range(min(path_step, len(animate_path))):
                px, py = animate_path[i]
                rect = pygame.Rect(MARGIN + px * (CELL_SIZE + MARGIN),
                                    MARGIN + py * (CELL_SIZE + MARGIN),
                                    CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, COLORS.get(algo_name, (0, 0, 255)), rect)
            if path_step < len(animate_path):
                path_step += 1
                pygame.time.delay(ANIMATION_DELAY)

        # Sidebar: Height Legend and Info
        pygame.draw.rect(screen, (230, 230, 230), (grid_area_width + GRID_MARGIN, 0, PANEL_WIDTH, grid_area_height))

        # Title
        legend_title = font_heading.render("Legend & Info", True, (0, 0, 0))
        screen.blit(legend_title, (sidebar_x, 30))

        # Height gradient
        legend_y = 80
        legend_height = 250
        for i in range(legend_height):
            ratio = i / legend_height
            color = (int(255 * ratio), int(255 * ratio), int(255 * ratio))
            pygame.draw.line(screen, color, (sidebar_x, legend_y + i), (sidebar_x + 30, legend_y + i))
        screen.blit(font_small.render("High", True, (0, 0, 0)), (sidebar_x + 40, legend_y))
        screen.blit(font_small.render("Low", True, (0, 0, 0)), (sidebar_x + 40, legend_y + legend_height - 15))

        # Start & Goal info
        info_y = legend_y + legend_height + 50
        pygame.draw.rect(screen, COLOR_START, (sidebar_x, info_y, 20, 20))
        screen.blit(font_small.render(f"Start: {START}", True, (0, 0, 0)), (sidebar_x + 30, info_y + 5))
        
        pygame.draw.rect(screen, COLOR_GOAL, (sidebar_x, info_y + 30, 20, 20))
        screen.blit(font_small.render(f"Goal: {GOAL}", True, (0, 0, 0)), (sidebar_x + 30, info_y + 35))

        # Obstacle Legend
        obs_y = info_y + 60
        pygame.draw.rect(screen, COLOR_STATIC_OBS, (sidebar_x, obs_y, 20, 20))
        screen.blit(font_small.render("Static Obstacle", True, (0, 0, 0)), (sidebar_x + 30, obs_y + 5))

        pygame.draw.rect(screen, COLOR_MOVING_OBS, (sidebar_x, obs_y + 30, 20, 20))
        screen.blit(font_small.render("Moving Obstacle", True, (0, 0, 0)), (sidebar_x + 30, obs_y + 35))


        # Draw Buttons
        for btn in buttons:
            if btn.text == algo_name:
                btn.base_color = (50, 205, 50)
            elif btn.text in algo_funcs:
                btn.base_color = (200, 200, 200)
            # Update Start/Stop Recording text
            if btn.text.startswith("Start Recording") or btn.text.startswith("Stop Recording"):
                btn.text = "Stop Recording" if recording else "Start Recording"
            btn.draw(screen, font)

        # Info Panel
        info_y = screen_height - 90
        info_text = [
            f"Algorithm: {algo_name}",
            f"Time: {metrics['time']} s",
            f"Length: {metrics['length']}",
            f"Cost: {metrics['cost']:.2f}",
            f"OPS: {metrics['ops']:.2f}",
            f"Recording: {'ON' if recording else 'OFF'}"
        ]
        for line in info_text:
            txt = font.render(line, True, (0, 0, 0))
            screen.blit(txt, (20, info_y))
            info_y += 25

        pygame.display.flip()

        # Capture frame for GIF only if recording
        if recording and frame_count % frame_skip == 0:
            frame = pygame.surfarray.array3d(screen)
            frames.append(frame.swapaxes(0, 1))

        clock.tick(30)

    pygame.quit()

    if trigger_matplotlib:
        plot_visualizations()

def plot_visualizations():
    if performance_data:
        df = pd.DataFrame(performance_data)

        # Time
        plt.figure(figsize=(8, 6))
        plt.bar(df["Algorithm"], df["Time (s)"], color="skyblue")
        plt.title("Execution Time per Algorithm")
        plt.ylabel("Time (s)")
        plt.show()

        # Path Length
        plt.figure(figsize=(8, 6))
        plt.bar(df["Algorithm"], df["Path Length (Adaptive 3D)"], color="lightgreen")
        plt.title("Path Length per Algorithm")
        plt.ylabel("Length")
        plt.show()

        # Path Cost
        plt.figure(figsize=(8, 6))
        plt.bar(df["Algorithm"], df["Path Cost (Adaptive Elevation)"], color="salmon")
        plt.title("Path Cost per Algorithm")
        plt.ylabel("Cost")
        plt.show()

        # OPS
        plt.figure(figsize=(8, 6))
        plt.bar(df["Algorithm"], df["Computing Power (OPS)"], color="violet")
        plt.title("Computing Power (OPS)")
        plt.ylabel("OPS")
        plt.show()
        
        for algo, convergence in convergence_data.items():
            if convergence:  # Only plot if there is data
                plt.figure(figsize=(8, 6))
                plt.plot(range(1, len(convergence) + 1), convergence, linewidth=2)
                plt.title(f"{algo} Convergence Curve")
                plt.xlabel("Iterations")
                plt.ylabel("Cost / Fitness")
                plt.grid(alpha=0.3)
                plt.show()