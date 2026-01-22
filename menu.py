import pygame
import sys

# ----------------------------------------
# Menu Options
# ----------------------------------------
BUTTONS = ["Sorting", "Searching", "Graphs", "DP", "Backtracking", "Exit"]

# ----------------------------------------
# Draw Rounded Background & Title
# ----------------------------------------
def draw_background(screen):
    """Draws a soft white background with slight gradient."""
    width, height = screen.get_size()
    for y in range(height):
        ratio = y / height
        shade = int(255 - 10 * ratio)
        pygame.draw.line(screen, (shade, shade, shade), (0, y), (width, y))

# ----------------------------------------
# Draw Animated Menu
# ----------------------------------------
def draw_menu(screen, selected_index, font, fade, pulse):
    """Draws the elegant white theme main menu."""
    draw_background(screen)
    width, height = screen.get_size()

    # --- Title ---
    title_font = pygame.font.Font(None, 90)
    title_surface = title_font.render("DAA VISUALIZER", True, (20, 90, 160))
    title_surface.set_alpha(fade)
    title_rect = title_surface.get_rect(center=(width // 2, 100))
    screen.blit(title_surface, title_rect)

    # Underline accent
    if fade > 80:
        pygame.draw.line(screen, (30, 130, 210),
                         (width // 2 - 200, 140),
                         (width // 2 + 200, 140), 4)

    # --- Menu Buttons ---
    for i, text in enumerate(BUTTONS):
        y_pos = height // 3 + i * 75

        if i == selected_index:
            color = (255, 255, 255)
            accent_color = (30, 150, 220)
            bar_width = 400 + int(pulse * 12)
            bar_height = 60 + int(pulse * 6)
            glow_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (accent_color[0], accent_color[1], accent_color[2], 120),
                             glow_surface.get_rect(), border_radius=30)
            glow_rect = glow_surface.get_rect(center=(width // 2, y_pos))
            screen.blit(glow_surface, glow_rect)

            # Outer subtle border
            pygame.draw.rect(screen, accent_color, glow_rect, 3, border_radius=30)
        else:
            color = (60, 60, 60)

        label = font.render(text, True, color)
        rect = label.get_rect(center=(width // 2, y_pos))
        screen.blit(label, rect)

    pygame.display.flip()

# ----------------------------------------
# Main Menu Logic
# ----------------------------------------
def show_main_menu(screen):
    """Displays the minimal white-theme main menu."""
    pygame.font.init()
    font = pygame.font.Font(None, 60)
    selected = 0
    fade = 0
    fade_in = True
    pulse = 0
    pulse_direction = 1

    clock = pygame.time.Clock()
    running = True

    while running:
        # Fade-in animation
        if fade_in:
            fade = min(fade + 10, 255)
            if fade == 255:
                fade_in = False

        # Pulse for glowing bar
        pulse += 0.05 * pulse_direction
        if pulse >= 1 or pulse <= 0:
            pulse_direction *= -1

        draw_menu(screen, selected, font, fade, pulse)

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(BUTTONS)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(BUTTONS)
                elif event.key == pygame.K_RETURN:
                    return BUTTONS[selected]

        clock.tick(60)
