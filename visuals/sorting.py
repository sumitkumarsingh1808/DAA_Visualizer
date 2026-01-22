import pygame
import random
import sys
from visuals.ui_manager import VisualUI


pygame.font.init()
FONT = pygame.font.Font(None, 40)
BIG_FONT = pygame.font.Font(None, 60)

# ---------------------------------------------
# Utility: Draw Array
# ---------------------------------------------
def draw_array(screen, arr, highlight=[], title="Sorting Visualizer"):
    WIDTH, HEIGHT = screen.get_size()
    screen.fill((255, 255, 255))
    bar_width = WIDTH // len(arr)
    max_val = max(arr)

    for i, val in enumerate(arr):
        color = (0, 255, 0) if i in highlight else (0, 0, 255)
        bar_height = int((val / max_val) * (HEIGHT - 150))
        pygame.draw.rect(screen, color, (i * bar_width, HEIGHT - bar_height, bar_width - 2, bar_height))

    title_text = FONT.render(title, True, (0, 0, 0))
    screen.blit(title_text, (20, 20))
    pygame.display.flip()


# ---------------------------------------------
# Sorting Algorithms with Visualization
# ---------------------------------------------
def bubble_sort_visual(screen, arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            draw_array(screen, arr, [j, j + 1], "Bubble Sort")
            pygame.time.delay(15)
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    draw_array(screen, arr)
    pygame.time.delay(400)


def selection_sort_visual(screen, arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            draw_array(screen, arr, [min_idx, j], "Selection Sort")
            pygame.time.delay(15)
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    draw_array(screen, arr)
    pygame.time.delay(400)


def insertion_sort_visual(screen, arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            draw_array(screen, arr, [j, j + 1], "Insertion Sort")
            pygame.time.delay(15)
            j -= 1
        arr[j + 1] = key
    draw_array(screen, arr)
    pygame.time.delay(400)


def merge_sort_visual(screen, arr, l=0, r=None):
    if r is None:
        r = len(arr) - 1

    def merge(l, m, r):
        left = arr[l:m + 1]
        right = arr[m + 1:r + 1]
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            draw_array(screen, arr, [k], "Merge Sort")
            pygame.time.delay(20)
            k += 1
        while i < len(left):
            arr[k] = left[i]
            draw_array(screen, arr, [k], "Merge Sort")
            pygame.time.delay(20)
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            draw_array(screen, arr, [k], "Merge Sort")
            pygame.time.delay(20)
            j += 1
            k += 1

    if l < r:
        m = (l + r) // 2
        merge_sort_visual(screen, arr, l, m)
        merge_sort_visual(screen, arr, m + 1, r)
        merge(l, m, r)


def partition(arr, low, high, screen):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        draw_array(screen, arr, [j, high], "Quick Sort")
        pygame.time.delay(15)
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort_visual(screen, arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pi = partition(arr, low, high, screen)
        quick_sort_visual(screen, arr, low, pi - 1)
        quick_sort_visual(screen, arr, pi + 1, high)


def heapify(arr, n, i, screen):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        draw_array(screen, arr, [i, largest], "Heap Sort")
        pygame.time.delay(25)
        heapify(arr, n, largest, screen)


def heap_sort_visual(screen, arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, screen)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        draw_array(screen, arr, [i], "Heap Sort")
        pygame.time.delay(25)
        heapify(arr, i, 0, screen)


# ---------------------------------------------
# Menu to Choose Algorithm
# ---------------------------------------------
def run_sorting_visual(screen):
    arr = [random.randint(10, 400) for _ in range(80)]
    algorithms = [
        "Bubble Sort",
        "Selection Sort",
        "Insertion Sort",
        "Merge Sort",
        "Quick Sort",
        "Heap Sort",
        "Back"
    ]
    selected = 0
    WIDTH, HEIGHT = screen.get_size()
    font = pygame.font.Font(None, 50)
    running = True

    while running:
        # Draw menu
        screen.fill((30, 30, 30))
        title = BIG_FONT.render("Sorting Algorithms", True, (0, 255, 255))
        screen.blit(title, (WIDTH // 2 - 180, 100))

        for i, algo in enumerate(algorithms):
            color = (0, 255, 0) if i == selected else (255, 255, 255)
            label = font.render(algo, True, color)
            rect = label.get_rect(center=(WIDTH // 2, 250 + i * 70))
            screen.blit(label, rect)

        pygame.display.flip()

        # Handle inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(algorithms)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(algorithms)
                elif event.key == pygame.K_RETURN:
                    if algorithms[selected] == "Bubble Sort":
                        bubble_sort_visual(screen, arr.copy())
                    elif algorithms[selected] == "Selection Sort":
                        selection_sort_visual(screen, arr.copy())
                    elif algorithms[selected] == "Insertion Sort":
                        insertion_sort_visual(screen, arr.copy())
                    elif algorithms[selected] == "Merge Sort":
                        merge_sort_visual(screen, arr.copy())
                    elif algorithms[selected] == "Quick Sort":
                        quick_sort_visual(screen, arr.copy())
                        draw_array(screen, arr, title="Quick Sort")
                    elif algorithms[selected] == "Heap Sort":
                        heap_sort_visual(screen, arr.copy())
                    elif algorithms[selected] == "Back":
                        return
                    pygame.time.delay(500)
