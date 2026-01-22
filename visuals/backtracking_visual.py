import pygame
import sys
import time
import random

pygame.font.init()
FONT = pygame.font.Font(None, 40)
BIG_FONT = pygame.font.Font(None, 60)
SMALL_FONT = pygame.font.Font(None, 28)

# -------------------------------------------------------------
# Global speed controller
# -------------------------------------------------------------
SPEEDS = {"Slow": 500, "Medium": 200, "Fast": 50}
current_speed = "Medium"
step_counter = 0


def get_delay():
    return SPEEDS[current_speed]


def increment_step():
    global step_counter
    step_counter += 1


# -------------------------------------------------------------
# 🧠 Complexity Info Panel
# -------------------------------------------------------------
def draw_info_panel(screen, algo_name):
    WIDTH, HEIGHT = screen.get_size()
    x, y, w, h = WIDTH - 340, 40, 300, 200
    pygame.draw.rect(screen, (240, 245, 255), (x, y, w, h), border_radius=12)
    pygame.draw.rect(screen, (50, 100, 200), (x, y, w, h), 2, border_radius=12)

    info_data = {
        "N-Queens": {"Time": "O(N!)", "Space": "O(N²)", "Concept": "Place N queens safely.", "Color": (0, 160, 255)},
        "Sudoku Solver": {"Time": "O(9ⁿ)", "Space": "O(81)", "Concept": "Solve Sudoku with constraint check.", "Color": (0, 180, 100)},
        "Rat in a Maze": {"Time": "O(2^(N²))", "Space": "O(N²)", "Concept": "Find path from start to destination.", "Color": (200, 80, 0)},
        "Subset Sum": {"Time": "O(2ⁿ)", "Space": "O(n)", "Concept": "Find subsets matching target sum.", "Color": (150, 50, 150)},
    }

    info = info_data.get(algo_name, {})
    color = info.get("Color", (0, 0, 0))
    title = BIG_FONT.render(algo_name, True, color)
    screen.blit(title, (x + 15, y + 10))
    screen.blit(FONT.render(f"⏱ {info.get('Time', '-')}", True, (0, 0, 0)), (x + 15, y + 60))
    screen.blit(FONT.render(f"💾 {info.get('Space', '-')}", True, (0, 0, 0)), (x + 15, y + 90))

    desc = SMALL_FONT.render(info.get("Concept", ""), True, (60, 60, 60))
    screen.blit(desc, (x + 15, y + 130))


# -------------------------------------------------------------
# 🧭 Global Top Bar (Speed + Steps)
# -------------------------------------------------------------
def draw_top_bar(screen):
    text = FONT.render(f"⚡ Speed: {current_speed}    🪜 Steps: {step_counter}", True, (0, 0, 0))
    screen.blit(text, (40, 20))


# -------------------------------------------------------------
# 🎯 N-Queens Visualization
# -------------------------------------------------------------
def draw_queens_board(screen, board, n, row=None, col=None, status=""):
    screen.fill((255, 255, 255))
    draw_top_bar(screen)
    cell_size = min(screen.get_width(), screen.get_height() - 100) // n
    offset_x = (screen.get_width() - n * cell_size) // 2
    offset_y = (screen.get_height() - n * cell_size) // 2 + 50

    for i in range(n):
        for j in range(n):
            rect = pygame.Rect(offset_x + j * cell_size, offset_y + i * cell_size, cell_size, cell_size)
            color = (240, 217, 181) if (i + j) % 2 == 0 else (181, 136, 99)
            if row == i and col == j:
                color = (255, 230, 120)
            pygame.draw.rect(screen, color, rect)
            if board[i][j] == 1:
                pygame.draw.circle(screen, (0, 150, 0), rect.center, cell_size // 3)

    msg = FONT.render(status, True, (0, 0, 0))
    screen.blit(msg, (offset_x, offset_y - 40))
    draw_info_panel(screen, "N-Queens")
    pygame.display.flip()


def is_safe_queen(board, row, col, n):
    for i in range(row):
        if board[i][col] == 1:
            return False
    for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
        if board[i][j] == 1:
            return False
    for i, j in zip(range(row - 1, -1, -1), range(col + 1, n)):
        if board[i][j] == 1:
            return False
    return True


def solve_nqueens(screen, board, row, n):
    if row == n:
        draw_queens_board(screen, board, n, status="✅ Solution Found!")
        time.sleep(1)
        return True
    for col in range(n):
        increment_step()
        draw_queens_board(screen, board, n, row, col, f"Trying row {row}, col {col}")
        pygame.time.delay(get_delay())
        if is_safe_queen(board, row, col, n):
            board[row][col] = 1
            draw_queens_board(screen, board, n, row, col, f"Placed Queen at ({row},{col}) ✅")
            pygame.time.delay(get_delay())
            if solve_nqueens(screen, board, row + 1, n):
                return True
            board[row][col] = 0
            draw_queens_board(screen, board, n, row, col, f"Backtracking from ({row},{col}) 🔄")
            pygame.time.delay(get_delay())
    return False


# -------------------------------------------------------------
# 🧩 Sudoku Visualization
# -------------------------------------------------------------
def draw_sudoku(screen, grid, r=None, c=None, msg=""):
    screen.fill((250, 250, 250))
    draw_top_bar(screen)
    size = 50
    offset_x, offset_y = 150, 80
    for i in range(9):
        for j in range(9):
            rect = pygame.Rect(offset_x + j * size, offset_y + i * size, size, size)
            color = (200, 255, 200) if (i, j) == (r, c) else (230, 230, 230)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
            if grid[i][j] != 0:
                val = FONT.render(str(grid[i][j]), True, (0, 0, 0))
                screen.blit(val, (offset_x + j * size + 15, offset_y + i * size + 8))
    draw_info_panel(screen, "Sudoku Solver")
    tip = FONT.render(msg, True, (0, 0, 0))
    screen.blit(tip, (offset_x, offset_y - 40))
    pygame.display.flip()


def is_valid_sudoku(grid, row, col, num):
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False
    return True


def solve_sudoku(screen, grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    increment_step()
                    draw_sudoku(screen, grid, row, col, f"Trying {num} at ({row},{col})")
                    pygame.time.delay(get_delay())
                    if is_valid_sudoku(grid, row, col, num):
                        grid[row][col] = num
                        if solve_sudoku(screen, grid):
                            return True
                        grid[row][col] = 0
                        draw_sudoku(screen, grid, row, col, f"Backtracking ({row},{col})")
                return False
    draw_sudoku(screen, grid, msg="✅ Sudoku Solved!")
    time.sleep(1)
    return True


# -------------------------------------------------------------
# 🧭 Rat in a Maze Visualization
# -------------------------------------------------------------
def draw_maze(screen, maze, path=None, pos=None):
    screen.fill((250, 250, 250))
    draw_top_bar(screen)
    n = len(maze)
    size = 60
    offset_x, offset_y = 200, 100
    for i in range(n):
        for j in range(n):
            rect = pygame.Rect(offset_x + j * size, offset_y + i * size, size, size)
            color = (255, 255, 255) if maze[i][j] == 1 else (50, 50, 50)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
    if path:
        for (i, j) in path:
            rect = pygame.Rect(offset_x + j * size, offset_y + i * size, size, size)
            pygame.draw.rect(screen, (0, 255, 0), rect)
    if pos:
        rect = pygame.Rect(offset_x + pos[1] * size, offset_y + pos[0] * size, size, size)
        pygame.draw.rect(screen, (255, 255, 0), rect)
    draw_info_panel(screen, "Rat in a Maze")
    pygame.display.flip()


def solve_maze(screen, maze, x, y, path):
    n = len(maze)
    if x == n - 1 and y == n - 1:
        path.append((x, y))
        draw_maze(screen, maze, path)
        time.sleep(1)
        return True
    if 0 <= x < n and 0 <= y < n and maze[x][y] == 1:
        increment_step()
        maze[x][y] = 0
        path.append((x, y))
        draw_maze(screen, maze, path, (x, y))
        pygame.time.delay(get_delay())
        if solve_maze(screen, maze, x + 1, y, path) or solve_maze(screen, maze, x, y + 1, path):
            return True
        path.pop()
        draw_maze(screen, maze, path, (x, y))
        pygame.time.delay(get_delay())
        maze[x][y] = 1
    return False


# -------------------------------------------------------------
# 🎯 Subset Sum Visualization
# -------------------------------------------------------------
def draw_subset(screen, arr, chosen, idx, target, msg=""):
    screen.fill((255, 255, 255))
    draw_top_bar(screen)
    draw_info_panel(screen, "Subset Sum")
    base_x, base_y = 150, 150
    for i, num in enumerate(arr):
        color = (0, 255, 0) if chosen[i] else (200, 200, 200)
        rect = pygame.Rect(base_x + i * 60, base_y, 50, 50)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        val = FONT.render(str(num), True, (0, 0, 0))
        screen.blit(val, (rect.x + 10, rect.y + 10))
    txt = FONT.render(msg, True, (0, 0, 0))
    screen.blit(txt, (150, 250))
    pygame.display.flip()


def subset_sum_visual(screen, arr, target, idx=0, current=None, chosen=None):
    if current is None:
        current = []
    if chosen is None:
        chosen = [False] * len(arr)
    increment_step()
    if sum(current) == target:
        draw_subset(screen, arr, chosen, idx, target, f"✅ Found Subset {current}")
        time.sleep(1)
        return True
    if idx >= len(arr) or sum(current) > target:
        return False
    chosen[idx] = True
    draw_subset(screen, arr, chosen, idx, target, f"Including {arr[idx]}")
    pygame.time.delay(get_delay())
    if subset_sum_visual(screen, arr, target, idx + 1, current + [arr[idx]], chosen):
        return True
    chosen[idx] = False
    draw_subset(screen, arr, chosen, idx, target, f"Excluding {arr[idx]}")
    pygame.time.delay(get_delay())
    return subset_sum_visual(screen, arr, target, idx + 1, current, chosen)


# -------------------------------------------------------------
# 🎮 Main Backtracking Menu
# -------------------------------------------------------------
def run_backtracking_visual(screen):
    global current_speed, step_counter
    algos = ["N-Queens", "Sudoku Solver", "Rat in a Maze", "Subset Sum", "Back"]
    selected = 0
    WIDTH, HEIGHT = screen.get_size()
    font = pygame.font.Font(None, 50)
    running = True

    while running:
        screen.fill((30, 30, 30))
        title = BIG_FONT.render("Backtracking Visuals", True, (0, 255, 255))
        screen.blit(title, (WIDTH // 2 - 200, 100))
        hint = SMALL_FONT.render("Press 1=Slow  2=Medium  3=Fast", True, (200, 200, 200))
        screen.blit(hint, (WIDTH // 2 - 160, 180))

        for i, algo in enumerate(algos):
            color = (0, 255, 0) if i == selected else (255, 255, 255)
            label = font.render(algo, True, color)
            rect = label.get_rect(center=(WIDTH // 2, 250 + i * 80))
            screen.blit(label, rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(algos)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(algos)
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    current_speed = {pygame.K_1: "Slow", pygame.K_2: "Medium", pygame.K_3: "Fast"}[event.key]
                elif event.key == pygame.K_RETURN:
                    step_counter = 0
                    if algos[selected] == "N-Queens":
                        n = 8
                        board = [[0 for _ in range(n)] for _ in range(n)]
                        solve_nqueens(screen, board, 0, n)
                    elif algos[selected] == "Sudoku Solver":
                        grid = [[0,0,0,2,6,0,7,0,1],
                                [6,8,0,0,7,0,0,9,0],
                                [1,9,0,0,0,4,5,0,0],
                                [8,2,0,1,0,0,0,4,0],
                                [0,0,4,6,0,2,9,0,0],
                                [0,5,0,0,0,3,0,2,8],
                                [0,0,9,3,0,0,0,7,4],
                                [0,4,0,0,5,0,0,3,6],
                                [7,0,3,0,1,8,0,0,0]]
                        solve_sudoku(screen, grid)
                    elif algos[selected] == "Rat in a Maze":
                        maze = [[1, 0, 0, 0],
                                [1, 1, 0, 1],
                                [0, 1, 0, 0],
                                [1, 1, 1, 1]]
                        path = []
                        solve_maze(screen, maze, 0, 0, path)
                    elif algos[selected] == "Subset Sum":
                        arr = [3, 34, 4, 12, 5, 2]
                        subset_sum_visual(screen, arr, target=9)
                    elif algos[selected] == "Back":
                        return
