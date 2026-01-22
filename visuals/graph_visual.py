import pygame
import sys
import math
import random
from collections import deque
import heapq

pygame.font.init()
FONT = pygame.font.Font(None, 32)
BIG_FONT = pygame.font.Font(None, 48)

# ---------------------------------------------
# Node class and Graph drawing
# ---------------------------------------------
class Node:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.visited = False


def draw_graph(screen, nodes, edges, highlight_nodes=None, title="Graph Visualization"):
    if highlight_nodes is None:
        highlight_nodes = []

    screen.fill((255, 255, 255))

    # Draw edges
    for (a, b, w) in edges:
        color = (150, 150, 150)
        pygame.draw.line(screen, color, (nodes[a].x, nodes[a].y), (nodes[b].x, nodes[b].y), 2)
        mid_x = (nodes[a].x + nodes[b].x) // 2
        mid_y = (nodes[a].y + nodes[b].y) // 2
        weight_text = FONT.render(str(w), True, (0, 0, 0))
        screen.blit(weight_text, (mid_x, mid_y))

    # Draw nodes
    for i, node in enumerate(nodes):
        color = (0, 255, 0) if i in highlight_nodes else (0, 0, 255)
        pygame.draw.circle(screen, color, (node.x, node.y), 25)
        id_text = FONT.render(str(node.id), True, (255, 255, 255))
        screen.blit(id_text, (node.x - 8, node.y - 10))

    title_text = BIG_FONT.render(title, True, (0, 0, 0))
    screen.blit(title_text, (20, 20))
    pygame.display.flip()


def generate_random_graph(num_nodes=6):
    nodes = []
    edges = []

    # Random node positions
    for i in range(num_nodes):
        x = random.randint(100, 900)
        y = random.randint(120, 500)
        nodes.append(Node(x, y, i))

    # Random edges with weights
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < 0.4:  # 40% chance of edge
                w = random.randint(1, 9)
                edges.append((i, j, w))
                edges.append((j, i, w))

    return nodes, edges

# ---------------------------------------------
# BFS Visualization
# ---------------------------------------------
def bfs_visual(screen, nodes, edges, start=0):
    adj = {i: [] for i in range(len(nodes))}
    for (a, b, w) in edges:
        adj[a].append(b)

    visited = set()
    q = deque([start])
    visited.add(start)

    while q:
        current = q.popleft()
        draw_graph(screen, nodes, edges, highlight_nodes=visited, title=f"BFS: Visiting Node {current}")
        pygame.time.delay(500)
        for neighbor in adj[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
    pygame.time.delay(1000)

# ---------------------------------------------
# DFS Visualization
# ---------------------------------------------
def dfs_visual(screen, nodes, edges, start=0):
    adj = {i: [] for i in range(len(nodes))}
    for (a, b, w) in edges:
        adj[a].append(b)

    visited = set()

    def dfs(u):
        visited.add(u)
        draw_graph(screen, nodes, edges, highlight_nodes=visited, title=f"DFS: Visiting Node {u}")
        pygame.time.delay(500)
        for v in adj[u]:
            if v not in visited:
                dfs(v)

    dfs(start)
    pygame.time.delay(1000)

# ---------------------------------------------
# Dijkstra Visualization
# ---------------------------------------------
def dijkstra_visual(screen, nodes, edges, start=0):
    adj = {i: [] for i in range(len(nodes))}
    for (a, b, w) in edges:
        adj[a].append((b, w))

    dist = {i: math.inf for i in range(len(nodes))}
    dist[start] = 0
    pq = [(0, start)]
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)

        draw_graph(screen, nodes, edges, highlight_nodes=visited, title=f"Dijkstra: Node {u}, Dist={d}")
        pygame.time.delay(700)

        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))

    pygame.time.delay(1200)

# ---------------------------------------------
# Main Graph Visualization Menu
# ---------------------------------------------
def run_graph_visual(screen):
    nodes, edges = generate_random_graph()
    algos = ["BFS", "DFS", "Dijkstra", "Back"]
    selected = 0
    WIDTH, HEIGHT = screen.get_size()
    font = pygame.font.Font(None, 50)
    running = True

    while running:
        # Draw menu
        screen.fill((30, 30, 30))
        title = BIG_FONT.render("Graph Algorithm Visuals", True, (0, 255, 255))
        screen.blit(title, (WIDTH // 2 - 220, 100))

        for i, algo in enumerate(algos):
            color = (0, 255, 0) if i == selected else (255, 255, 255)
            label = font.render(algo, True, color)
            rect = label.get_rect(center=(WIDTH // 2, 250 + i * 80))
            screen.blit(label, rect)

        pygame.display.flip()

        # Handle inputs
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
                    if algos[selected] == "BFS":
                        bfs_visual(screen, nodes, edges)
                    elif algos[selected] == "DFS":
                        dfs_visual(screen, nodes, edges)
                    elif algos[selected] == "Dijkstra":
                        dijkstra_visual(screen, nodes, edges)
                    elif algos[selected] == "Back":
                        return
                    pygame.time.delay(600)
