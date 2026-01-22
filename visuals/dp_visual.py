import pygame
import sys
import math
import random

pygame.font.init()
FONT = pygame.font.Font(None, 32)
BIG_FONT = pygame.font.Font(None, 48)
SMALL_FONT = pygame.font.Font(None, 24)

# -------------------------------------------------------------
# 🧠 Complexity Info Panel
# -------------------------------------------------------------
def draw_info_panel(screen, algo_name):
    """Draws algorithm-specific complexity and info box."""
    WIDTH, HEIGHT = screen.get_size()
    x, y, w, h = WIDTH - 340, 40, 300, 180

    # Draw box background
    pygame.draw.rect(screen, (240, 245, 255), (x, y, w, h), border_radius=12)
    pygame.draw.rect(screen, (0, 80, 180), (x, y, w, h), 2, border_radius=12)

    info_data = {
        "Floyd–Warshall": {
            "Time": "O(V³)",
            "Space": "O(V²)",
            "Concept": "Finds shortest path between all pairs using DP.",
            "Color": (0, 100, 255),
        },
        "0/1 Knapsack": {
            "Time": "O(N·W)",
            "Space": "O(N·W)",
            "Concept": "Maximizes total value under capacity constraints.",
            "Color": (0, 160, 0),
        },
        "LCS": {
            "Time": "O(M·N)",
            "Space": "O(M·N)",
            "Concept": "Finds longest subsequence common to two strings.",
            "Color": (180, 60, 60),
        },
        "Matrix Chain": {
            "Time": "O(N³)",
            "Space": "O(N²)",
            "Concept": "Optimizes matrix multiplication order.",
            "Color": (120, 0, 150),
        }
    }

    info = info_data.get(algo_name, {})
    title_color = info.get("Color", (0, 0, 0))

    # Title
    title = BIG_FONT.render(algo_name, True, title_color)
    screen.blit(title, (x + 15, y + 10))

    # Time & Space
    time_text = FONT.render(f"⏱ Time: {info.get('Time', '-')}", True, (0, 0, 0))
    space_text = FONT.render(f"💾 Space: {info.get('Space', '-')}", True, (0, 0, 0))
    screen.blit(time_text, (x + 15, y + 60))
    screen.blit(space_text, (x + 15, y + 90))

    # Concept (wrapped)
    words = info.get("Concept", "").split(" ")
    line, lines = "", []
    for w_ in words:
        if len(line + w_) < 30:
            line += w_ + " "
        else:
            lines.append(line.strip())
            line = w_ + " "
    lines.append(line.strip())

    for i, line in enumerate(lines[:3]):
        desc = SMALL_FONT.render(line, True, (40, 40, 40))
        screen.blit(desc, (x + 15, y + 120 + i * 20))


# -------------------------------------------------------------
# 🎨 Utility: Matrix Drawing
# -------------------------------------------------------------
def draw_matrix(screen, matrix, title, highlights=None, arrow=None,
                cell_size=70, start_x=150, start_y=100):
    """Draws a matrix with optional highlighted cells and arrows."""
    screen.fill((245, 250, 255))
    n, m = len(matrix), len(matrix[0])
    highlights = highlights or []

    title_surface = BIG_FONT.render(title, True, (0, 0, 0))
    screen.blit(title_surface, (100, 30))

    for i in range(n):
        for j in range(m):
            x = start_x + j * cell_size
            y = start_y + i * cell_size
            color = (255, 255, 120) if (i, j) in highlights else (220, 230, 240)

            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, cell_size, cell_size), 1)

            val = matrix[i][j]
            val_text = "∞" if val == math.inf else str(val)
            text_surface = FONT.render(val_text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
            screen.blit(text_surface, text_rect)

    # Draw arrow pointer (optional)
    if arrow:
        i, j = arrow
        ax = start_x + j * cell_size + cell_size // 2
        ay = start_y + i * cell_size - 10
        pygame.draw.polygon(screen, (255, 0, 0),
                            [(ax - 6, ay - 10), (ax + 6, ay - 10), (ax, ay + 5)])
        pygame.draw.line(screen, (255, 0, 0), (ax, ay - 15), (ax, ay + 5), 2)

    pygame.display.flip()


# -------------------------------------------------------------
# 1️⃣ Floyd–Warshall Visualization
# -------------------------------------------------------------
def floyd_warshall_visual(screen):
    n = 5
    dist = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
        for j in range(n):
            if i != j and random.random() < 0.5:
                dist[i][j] = random.randint(1, 9)

    draw_matrix(screen, dist, "Floyd–Warshall (Initial)")
    draw_info_panel(screen, "Floyd–Warshall")
    pygame.display.flip()
    pygame.time.delay(1000)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                draw_matrix(screen, dist, f"Step k={k+1}, i={i}, j={j}",
                            highlights=[(i, j)], arrow=(i, j))
                draw_info_panel(screen, "Floyd–Warshall")
                pygame.display.flip()
                pygame.time.delay(300)

                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    draw_matrix(screen, dist, "Floyd–Warshall (Final)")
    draw_info_panel(screen, "Floyd–Warshall")
    pygame.display.flip()
    pygame.time.delay(2000)


# -------------------------------------------------------------
# 2️⃣ 0/1 Knapsack Visualization
# -------------------------------------------------------------
def knapsack_visual(screen):
    n, W = 5, 10
    weights = [2, 3, 4, 5, 9]
    values = [3, 4, 5, 8, 10]
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(W + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w],
                               values[i - 1] + dp[i - 1][w - weights[i - 1]])
            else:
                dp[i][w] = dp[i - 1][w]

            draw_matrix(screen, dp, f"Knapsack (i={i}, w={w})",
                        highlights=[(i, w)], arrow=(i, w), cell_size=50, start_x=100, start_y=120)
            draw_info_panel(screen, "0/1 Knapsack")
            pygame.display.flip()
            pygame.time.delay(200)

    draw_matrix(screen, dp, "Knapsack Complete", cell_size=50, start_x=100, start_y=120)
    draw_info_panel(screen, "0/1 Knapsack")
    pygame.display.flip()
    pygame.time.delay(2000)


# -------------------------------------------------------------
# 3️⃣ Longest Common Subsequence Visualization
# -------------------------------------------------------------
def lcs_visual(screen):
    X = "ACDB"
    Y = "ACB"
    m, n = len(X), len(Y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

            draw_matrix(screen, dp, f"LCS '{X}' & '{Y}' (i={i}, j={j})",
                        highlights=[(i, j)], arrow=(i, j), cell_size=60)
            draw_info_panel(screen, "LCS")
            pygame.display.flip()
            pygame.time.delay(300)

    draw_matrix(screen, dp, "LCS Complete", cell_size=60)
    draw_info_panel(screen, "LCS")
    pygame.display.flip()
    pygame.time.delay(2000)


# -------------------------------------------------------------
# 4️⃣ Matrix Chain Multiplication Visualization
# -------------------------------------------------------------
def matrix_chain_visual(screen):
    dims = [5, 10, 3, 12, 5, 50, 6]
    n = len(dims) - 1
    m = [[0 if i == j else math.inf for j in range(n)] for i in range(n)]

    for L in range(2, n + 1):
        for i in range(n - L + 1):
            j = i + L - 1
            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if q < m[i][j]:
                    m[i][j] = q

                draw_matrix(screen, m, f"Matrix Chain (i={i}, j={j}, k={k})",
                            highlights=[(i, j)], arrow=(i, j), cell_size=60)
                draw_info_panel(screen, "Matrix Chain")
                pygame.display.flip()
                pygame.time.delay(250)

    draw_matrix(screen, m, "Matrix Chain Complete", cell_size=60)
    draw_info_panel(screen, "Matrix Chain")
    pygame.display.flip()
    pygame.time.delay(2000)


# -------------------------------------------------------------
# 🧩 DP Visual Menu
# -------------------------------------------------------------
def run_dp_visual(screen):
    algos = ["Floyd–Warshall", "0/1 Knapsack", "LCS", "Matrix Chain", "Back"]
    selected = 0
    WIDTH, HEIGHT = screen.get_size()
    font = pygame.font.Font(None, 50)
    running = True

    while running:
        screen.fill((30, 30, 30))
        title = BIG_FONT.render("Dynamic Programming Visuals", True, (0, 255, 255))
        screen.blit(title, (250, 100))

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
                elif event.key == pygame.K_RETURN:
                    if algos[selected] == "Floyd–Warshall":
                        floyd_warshall_visual(screen)
                    elif algos[selected] == "0/1 Knapsack":
                        knapsack_visual(screen)
                    elif algos[selected] == "LCS":
                        lcs_visual(screen)
                    elif algos[selected] == "Matrix Chain":
                        matrix_chain_visual(screen)
                    elif algos[selected] == "Back":
                        return
