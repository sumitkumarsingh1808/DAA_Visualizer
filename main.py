import pygame
import sys
import time
from menu import show_main_menu

# -----------------------------------------------------
# 🧩 Initialize pygame
# -----------------------------------------------------
pygame.init()
pygame.mixer.init()

# Screen setup
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎮 DAA Visualizer")

# Fonts
TITLE_FONT = pygame.font.Font(None, 90)
SUB_FONT = pygame.font.Font(None, 40)

# Colors
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (25, 25, 25)
ACCENT_COLOR = (30, 150, 220)

# -----------------------------------------------------
# ✨ Splash / Intro Screen
# -----------------------------------------------------
def show_splash(screen):
    """Displays an elegant fade-in splash screen."""
    screen.fill(BG_COLOR)
    title = TITLE_FONT.render("DAA VISUALIZER", True, ACCENT_COLOR)
    sub = SUB_FONT.render("Designed & Developed by Sumit Maurya", True, TEXT_COLOR)

    for alpha in range(0, 255, 8):
        screen.fill(BG_COLOR)
        title_surf = title.copy()
        title_surf.set_alpha(alpha)
        sub_surf = sub.copy()
        sub_surf.set_alpha(alpha)
        screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
        screen.blit(sub_surf, sub_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))
        pygame.display.flip()
        pygame.time.delay(30)

    time.sleep(0.8)
    fade_out(screen)


# -----------------------------------------------------
# 🌫️ Smooth Fade-Out Transition
# -----------------------------------------------------
def fade_out(screen, color=(255, 255, 255)):
    """Fades the screen to a solid color."""
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill(color)
    for alpha in range(0, 255, 10):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(15)


# -----------------------------------------------------
# 💡 Loading Overlay (between modules)
# -----------------------------------------------------
def show_loading(screen, text="Loading..."):
    """Displays a quick loading transition."""
    overlay = pygame.Surface(screen.get_size())
    overlay.fill(BG_COLOR)
    loading_text = SUB_FONT.render(text, True, (70, 70, 70))
    dots = ["", ".", "..", "..."]
    for i in range(4):
        screen.blit(overlay, (0, 0))
        screen.blit(loading_text, loading_text.get_rect(center=(WIDTH // 2 - 20, HEIGHT // 2)))
        dots_text = SUB_FONT.render(dots[i], True, ACCENT_COLOR)
        screen.blit(dots_text, (WIDTH // 2 + 120, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(250)


# -----------------------------------------------------
# 🎮 Main Game Logic
# -----------------------------------------------------
def main():
    print("🎯 Launching DAA Visualizer...")
    running = True

    show_splash(screen)  # Intro

    while running:
        # Display main menu and get choice
        choice = show_main_menu(screen)
        print(f"✅ Selected: {choice}")

        try:
            if choice == "Sorting":
                show_loading(screen, "Loading Sorting Visualizer")
                import visuals.sorting as sorting
                sorting.run_sorting_visual(screen)

            elif choice == "Searching":
                show_loading(screen, "Loading Searching Visualizer")
                import algorithms.searching as searching
                searching.run_search_visual(screen)

            elif choice == "Graphs":
                show_loading(screen, "Loading Graph Algorithms")
                import visuals.graph_visual as graph
                graph.run_graph_visual(screen)

            elif choice == "DP":
                show_loading(screen, "Loading Dynamic Programming")
                import visuals.dp_visual as dp
                dp.run_dp_visual(screen)

            elif choice == "Backtracking":
                show_loading(screen, "Loading Backtracking Algorithms")
                import visuals.backtracking_visual as backtrack
                backtrack.run_backtracking_visual(screen)

            elif choice == "Exit":
                fade_out(screen)
                print("👋 Exiting the DAA Visualizer...")
                running = False

            else:
                print(f"⚠️ Unknown selection: {choice}")

        except ModuleNotFoundError as err:
            print(f"❌ Missing module: {err}")
            show_error(screen, f"Module Not Found: {err}")
        except Exception as e:
            print(f"💥 Unexpected Error: {e}")
            show_error(screen, f"Error: {e}")

    pygame.quit()
    sys.exit()


# -----------------------------------------------------
# 🚨 Error Display Overlay
# -----------------------------------------------------
def show_error(screen, message):
    """Displays an error popup overlay."""
    overlay = pygame.Surface(screen.get_size())
    overlay.fill((255, 230, 230))
    pygame.draw.rect(overlay, (255, 0, 0), (200, 230, 600, 150), border_radius=15)
    text = SUB_FONT.render("⚠️ ERROR", True, (255, 255, 255))
    msg = SUB_FONT.render(message, True, (255, 255, 255))
    screen.blit(overlay, (0, 0))
    screen.blit(text, (WIDTH // 2 - 50, 250))
    screen.blit(msg, (WIDTH // 2 - 250, 300))
    pygame.display.flip()
    pygame.time.delay(1800)


# -----------------------------------------------------
# 🚀 Entry Point
# -----------------------------------------------------
if __name__ == "__main__":
    main()
