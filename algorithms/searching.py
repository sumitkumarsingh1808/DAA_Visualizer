import pygame
import sys
import random
import os
import math

# ---------------------------
# Initialization
# ---------------------------
pygame.init()
pygame.font.init()

FONT = pygame.font.Font(None, 36)
BIG_FONT = pygame.font.Font(None, 60)
SMALL_FONT = pygame.font.Font(None, 28)

# ---------------------------
# Sound loading
# ---------------------------
sound_enabled = True
sound_path = os.path.join("assets", "sounds")

try:
    pygame.mixer.init()
except Exception:
    # mixer might fail on some systems; we'll handle gracefully
    pass

try:
    click_sound = pygame.mixer.Sound(os.path.join(sound_path, "click.wav"))
    success_sound = pygame.mixer.Sound(os.path.join(sound_path, "success.wav"))
    error_sound = pygame.mixer.Sound(os.path.join(sound_path, "error.wav"))
except Exception as e:
    # missing/invalid files -> disable sound
    # print for dev awareness but keep running
    print(f"⚠️ Sound files not found or failed to load: {e}")
    sound_enabled = False
    click_sound = success_sound = error_sound = None


def play_sound(effect, muted=False):
    """Play sound effect if available and not muted."""
    if muted or not sound_enabled:
        return
    try:
        if effect == "click" and click_sound:
            click_sound.play()
        elif effect == "success" and success_sound:
            success_sound.play()
        elif effect == "error" and error_sound:
            error_sound.play()
    except Exception:
        pass


# ---------------------------
# Drawing / UI
# ---------------------------
def draw_interface(screen, arr, highlight=None, title="Searching Visualizer",
                   message="", input_text="", comparisons=0, complexity="O(n)",
                   pointers=None, muted=False, glow_effect=None):
    """
    glow_effect: None or dict { "pos": (x,y), "rings": [(radius, alpha), ...] }
    pointers: dict like {"low": idx, "mid": idx, "high": idx} (indices may be floats for animation)
    """
    if highlight is None:
        highlight = []

    WIDTH, HEIGHT = screen.get_size()
    screen.fill((240, 248, 255))
    bar_count = len(arr)
    bar_width = max(1, WIDTH // bar_count)
    max_val = max(arr) if arr else 1

    # subtle vertical gradient
    for y in range(HEIGHT):
        shade = 230 + int(25 * (y / HEIGHT))
        pygame.draw.line(screen, (shade, shade, 255), (0, y), (WIDTH, y))

    # bars
    for i, val in enumerate(arr):
        is_high = i in highlight
        color = (0, 255, 128) if is_high else (0, 100, 255)
        bar_height = int((val / max_val) * (HEIGHT - 250))
        x = i * bar_width
        y = HEIGHT - bar_height - 50
        pygame.draw.rect(screen, color, (x, y, bar_width - 2, bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width - 2, bar_height), 1)
        # value label
        t = SMALL_FONT.render(str(val), True, (0, 0, 0))
        screen.blit(t, (x + max(2, bar_width // 4), y - 22))

    # glow rings (if any)
    if glow_effect is not None:
        # expect glow_effect = {"pos": (x, y), "rings":[(r,alpha), ...]}
        pos = glow_effect.get("pos")
        rings = glow_effect.get("rings", [])
        for radius, alpha in rings:
            if radius <= 0 or alpha <= 0:
                continue
            glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            glow_color = (255, 0, 0, int(alpha))
            pygame.draw.circle(glow_surface, glow_color, pos, int(radius))
            screen.blit(glow_surface, (0, 0))

    # title
    title_text = BIG_FONT.render(title, True, (0, 0, 80))
    screen.blit(title_text, (20, 20))

    # input area
    input_label = FONT.render("🔍 Enter number:", True, (0, 0, 0))
    screen.blit(input_label, (20, 90))
    pygame.draw.rect(screen, (255, 255, 255), (230, 90, 100, 40))
    pygame.draw.rect(screen, (0, 0, 0), (230, 90, 100, 40), 2)
    input_surface = FONT.render(input_text, True, (0, 0, 0))
    screen.blit(input_surface, (240, 95))

    # message
    msg_text = FONT.render(message, True, (200, 30, 30))
    screen.blit(msg_text, (20, 150))

    # complexity panel
    pygame.draw.rect(screen, (230, 230, 255), (WIDTH - 260, 30, 230, 130), border_radius=12)
    pygame.draw.rect(screen, (0, 0, 0), (WIDTH - 260, 30, 230, 130), 2, border_radius=12)
    screen.blit(FONT.render("📊 Complexity", True, (0, 0, 0)), (WIDTH - 245, 40))
    screen.blit(SMALL_FONT.render(f"Time: {complexity}", True, (0, 0, 0)), (WIDTH - 245, 80))
    screen.blit(SMALL_FONT.render("Space: O(1)", True, (0, 0, 0)), (WIDTH - 245, 105))

    # comparisons
    compare_text = FONT.render(f"🔁 Comparisons: {comparisons}", True, (0, 0, 0))
    screen.blit(compare_text, (WIDTH - 245, 155))

    # mute hint
    mute_text = SMALL_FONT.render(f"🔈 {'ON' if not muted else 'MUTED'} (Press M)", True, (0, 0, 0))
    screen.blit(mute_text, (20, HEIGHT - 40))

    # pointers (low/mid/high)
    # pointers (low/mid/high/i)
    if pointers:
        for key, index in pointers.items():
            if index is None:
                continue
            x = index * bar_width + bar_width // 2
            y = HEIGHT - 60

            color_map = {
                "low": (255, 165, 0),
                "mid": (255, 0, 0),
                "high": (0, 255, 255),
                "i": (255, 0, 0),  # 🔴 Red for Linear Search

            }
            color = color_map.get(key, (255, 255, 255))

            # draw pointer arrow
            pygame.draw.polygon(screen, color, [
                (x - 10, y + 10),
                (x + 10, y + 10),
                (x, y - 10)
            ])
            label = SMALL_FONT.render(key.upper(), True, color)
            screen.blit(label, (x - 10, y + 22))

            # triangle arrow
            pygame.draw.polygon(screen, color, [
                (x - 10, y + 10),
                (x + 10, y + 10),
                (x, y - 10)
            ])
            label = SMALL_FONT.render(key.upper(), True, color)
            screen.blit(label, (x - 20, y + 22))

    pygame.display.flip()


# ---------------------------
# Linear Search (with sound & glow)
# ---------------------------
def linear_search_visual(screen, arr, target, muted):
    comparisons = 0
    bar_width = max(1, screen.get_width() // len(arr))
    HEIGHT = screen.get_height()
    max_val = max(arr)

    for i in range(len(arr)):
        comparisons += 1
        pointers = {"i": i}

        # Regular checking frame
        draw_interface(screen, arr, highlight=[i], title="Linear Search",
                       message=f"Checking index {i}...", input_text=str(target),
                       comparisons=comparisons, complexity="O(n)",
                       pointers=pointers, muted=muted)
        play_sound("click", muted)
        pygame.time.delay(350)

        # Found condition
        if arr[i] == target:
            play_sound("success", muted)

            # 🎨 Pop animation (bar jumps up)
            for lift in range(0, 30, 3):
                screen.fill((240, 248, 255))
                popped_arr = arr.copy()
                # Draw bars, but make the found one higher and green
                for j, val in enumerate(popped_arr):
                    bar_height = int((val / max_val) * (HEIGHT - 250))
                    x = j * bar_width
                    y = HEIGHT - bar_height - 50

                    if j == i:
                        y -= lift  # lift upward
                        color = (0, 255, 0)  # bright green
                    else:
                        color = (0, 100, 255)

                    pygame.draw.rect(screen, color, (x, y, bar_width - 2, bar_height))
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width - 2, bar_height), 1)
                    val_text = SMALL_FONT.render(str(val), True, (0, 0, 0))
                    screen.blit(val_text, (x + bar_width // 4, y - 25))

                # Pointer above found bar
                x_pointer = i * bar_width + bar_width // 2
                pygame.draw.polygon(screen, (0, 255, 0), [
                    (x_pointer - 10, HEIGHT - 60),
                    (x_pointer + 10, HEIGHT - 60),
                    (x_pointer, HEIGHT - 80)
                ])
                label = SMALL_FONT.render("I", True, (0, 255, 0))
                screen.blit(label, (x_pointer - 10, HEIGHT - 100))

                msg_text = FONT.render(f"✅ Found {target} at index {i}", True, (0, 150, 0))
                screen.blit(msg_text, (20, 150))

                pygame.display.flip()
                pygame.time.delay(30)

            pygame.time.delay(800)
            return True, comparisons

    # ❌ Not found
    draw_interface(screen, arr, [], title="Linear Search",
                   message=f"❌ {target} not found", input_text=str(target),
                   comparisons=comparisons, complexity="O(n)", muted=muted)
    play_sound("error", muted)
    pygame.time.delay(1000)
    return False, comparisons



# ---------------------------
# Binary Search (with animated pointers, sound & glow)
# ---------------------------
def binary_search_visual(screen, arr, target, muted):
    arr.sort()
    low, high = 0, len(arr) - 1
    comparisons = 0
    WIDTH, HEIGHT = screen.get_size()
    bar_width = max(1, WIDTH // len(arr))
    max_val = max(arr)

    # previous pointers for smooth movement
    prev_ptrs = {"low": low, "mid": (low + high) // 2, "high": high}

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        pointers = {"low": low, "mid": mid, "high": high}

        draw_interface(screen, arr, highlight=[mid], title="Binary Search",
                       message=f"Checking mid index {mid}...", input_text=str(target),
                       comparisons=comparisons, complexity="O(log n)", pointers=pointers, muted=muted)
        play_sound("click", muted)
        pygame.time.delay(500)

        # ✅ FOUND VALUE
        if arr[mid] == target:
            play_sound("success", muted)

            # 🎨 Pop-up animation for found bar
            for lift in range(0, 30, 3):
                screen.fill((240, 248, 255))
                for i, val in enumerate(arr):
                    bar_height = int((val / max_val) * (HEIGHT - 250))
                    x = i * bar_width
                    y = HEIGHT - bar_height - 50

                    if i == mid:
                        y -= lift  # lift up
                        color = (0, 255, 0)  # bright green
                    else:
                        color = (0, 100, 255)

                    pygame.draw.rect(screen, color, (x, y, bar_width - 2, bar_height))
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width - 2, bar_height), 1)
                    val_text = SMALL_FONT.render(str(val), True, (0, 0, 0))
                    screen.blit(val_text, (x + bar_width // 4, y - 25))

                # Draw pointers (low, mid, high)
                for key, index in pointers.items():
                    if index is None:
                        continue
                    px = index * bar_width + bar_width // 2
                    py = HEIGHT - 60
                    color_map = {"low": (255, 165, 0), "mid": (0, 255, 0), "high": (0, 255, 255)}
                    pointer_color = color_map.get(key, (255, 255, 255))
                    pygame.draw.polygon(screen, pointer_color, [
                        (px - 10, py + 10),
                        (px + 10, py + 10),
                        (px, py - 10)
                    ])
                    label = SMALL_FONT.render(key.upper(), True, pointer_color)
                    screen.blit(label, (px - 10, py + 22))

                msg_text = FONT.render(f"✅ Found {target} at index {mid}", True, (0, 150, 0))
                screen.blit(msg_text, (20, 150))

                pygame.display.flip()
                pygame.time.delay(30)

            pygame.time.delay(800)
            return True, comparisons

        # 🔸 Move right
        elif arr[mid] < target:
            new_low = mid + 1
            for t in range(8):
                interp = {}
                for k in ("low", "mid", "high"):
                    start = prev_ptrs.get(k, 0)
                    end_val = {"low": new_low, "mid": mid, "high": high}.get(k, prev_ptrs.get(k))
                    interp[k] = start + (end_val - start) * (t / 8.0)
                draw_interface(screen, arr, highlight=list(range(prev_ptrs["low"], mid + 1)), title="Binary Search",
                               message=f"{arr[mid]} < {target}, moving right...", input_text=str(target),
                               comparisons=comparisons, complexity="O(log n)", pointers=interp, muted=muted)
                pygame.time.delay(30)
            low = new_low
            prev_ptrs = {"low": low, "mid": mid, "high": high}

        # 🔹 Move left
        else:
            new_high = mid - 1
            for t in range(8):
                interp = {}
                for k in ("low", "mid", "high"):
                    start = prev_ptrs.get(k, 0)
                    end_val = {"low": low, "mid": mid, "high": new_high}.get(k, prev_ptrs.get(k))
                    interp[k] = start + (end_val - start) * (t / 8.0)
                draw_interface(screen, arr, highlight=list(range(mid, prev_ptrs["high"] + 1)), title="Binary Search",
                               message=f"{arr[mid]} > {target}, moving left...", input_text=str(target),
                               comparisons=comparisons, complexity="O(log n)", pointers=interp, muted=muted)
                pygame.time.delay(30)
            high = new_high
            prev_ptrs = {"low": low, "mid": mid, "high": high}

    # ❌ NOT FOUND
    draw_interface(screen, arr, [], title="Binary Search",
                   message=f"❌ {target} not found", input_text=str(target),
                   comparisons=comparisons, complexity="O(log n)", muted=muted)
    play_sound("error", muted)
    pygame.time.delay(1000)
    return False, comparisons



# ---------------------------
# Retry overlay
# ---------------------------
def show_retry_overlay(screen, last_algo):
    WIDTH, HEIGHT = screen.get_size()
    font = pygame.font.Font(None, 50)
    options = ["🔁 Try Again", "⬅ Back"]
    selected = 0

    while True:
        # draw overlay background
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        title = BIG_FONT.render(f"{last_algo} Complete", True, (0, 255, 255))
        screen.blit(title, (WIDTH // 2 - 200, 140))

        for i, text in enumerate(options):
            color = (0, 255, 0) if i == selected else (255, 255, 255)
            label = font.render(text, True, color)
            rect = label.get_rect(center=(WIDTH // 2, 300 + i * 80))
            screen.blit(label, rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected]


# ---------------------------
# Main function to run searching UI
# ---------------------------
def run_search_visual(screen):
    arr = [random.randint(10, 99) for _ in range(20)]
    algorithms = ["Linear Search", "Binary Search", "Back"]
    selected_algo = 0
    WIDTH, HEIGHT = screen.get_size()
    font = pygame.font.Font(None, 50)
    muted = False

    while True:
        # algorithm selection menu
        screen.fill((30, 30, 30))
        title = BIG_FONT.render("Searching Algorithms", True, (0, 255, 255))
        screen.blit(title, (WIDTH // 2 - 200, 100))
        for i, algo in enumerate(algorithms):
            color = (0, 255, 0) if i == selected_algo else (255, 255, 255)
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
                    selected_algo = (selected_algo - 1) % len(algorithms)
                elif event.key == pygame.K_DOWN:
                    selected_algo = (selected_algo + 1) % len(algorithms)
                elif event.key == pygame.K_RETURN:
                    if algorithms[selected_algo] == "Back":
                        return

                    # interactive single-screen mode
                    arr_copy = arr.copy()
                    input_text = ""
                    searching = False
                    target = None

                    while True:
                        draw_interface(screen, arr_copy, [], algorithms[selected_algo],
                                       "Type number and press Enter to search",
                                       input_text, 0,
                                       "O(n)" if algorithms[selected_algo] == "Linear Search" else "O(log n)",
                                       muted=muted)

                        for e in pygame.event.get():
                            if e.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif e.type == pygame.KEYDOWN:
                                # mute toggle
                                if e.key == pygame.K_m:
                                    muted = not muted
                                if not searching:
                                    if e.key == pygame.K_RETURN and input_text.strip().isdigit():
                                        target = int(input_text)
                                        searching = True
                                        if algorithms[selected_algo] == "Linear Search":
                                            found, comps = linear_search_visual(screen, arr_copy, target, muted)
                                        else:
                                            found, comps = binary_search_visual(screen, arr_copy, target, muted)
                                        choice = show_retry_overlay(screen, algorithms[selected_algo])
                                        if choice == "⬅ Back":
                                            break  # return to algorithms menu
                                        elif choice == "🔁 Try Again":
                                            arr_copy = arr.copy()
                                            input_text = ""
                                            searching = False
                                            target = None
                                    elif e.key == pygame.K_BACKSPACE:
                                        input_text = input_text[:-1]
                                    elif e.unicode.isdigit():
                                        input_text += e.unicode
                        else:
                            # inner while continues
                            continue
                        # inner while broken by "Back"
                        break
