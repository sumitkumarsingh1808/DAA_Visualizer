import pygame

# -------------------------------------------------
# 🧠 Visual Layout Manager (Scrolling + Theme)
# -------------------------------------------------
class VisualUI:
    def __init__(self, screen, title="Visualizer"):
        self.screen = screen
        self.title = title
        self.scroll_offset = 0
        self.scroll_speed = 30
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 60)
        self.bg_color = (255, 255, 255)
        self.text_color = (30, 30, 30)
        self.accent = (30, 150, 220)
        self.border = (200, 200, 200)
        self.max_y = 0  # max content height

    # Draws clean white background + title
    def draw_header(self):
        self.screen.fill(self.bg_color)
        title_text = self.big_font.render(self.title, True, self.accent)
        self.screen.blit(title_text, (50, 30))
        pygame.draw.line(self.screen, self.accent, (50, 85), (950, 85), 3)

    # Safe drawing area that auto scrolls if content too tall
    def draw_scrollable_area(self, draw_content_callback):
        """draw_content_callback(y_offset) must draw visuals using the given Y offset."""
        height = self.screen.get_height()
        surface = pygame.Surface((self.screen.get_width(), 2000))  # large virtual canvas
        surface.fill(self.bg_color)

        # Call visual drawing function
        draw_content_callback(surface)

        # Get total content height
        self.max_y = surface.get_height()

        # Scroll boundary checks
        if self.scroll_offset < 0:
            self.scroll_offset = 0
        elif self.scroll_offset > self.max_y - height + 100:
            self.scroll_offset = self.max_y - height + 100

        # Render only visible portion
        self.screen.blit(surface, (0, -self.scroll_offset))

    def handle_scroll(self, event):
        """Handles scroll up/down using mouse wheel or arrow keys."""
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset -= event.y * self.scroll_speed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.scroll_offset -= self.scroll_speed
            elif event.key == pygame.K_DOWN:
                self.scroll_offset += self.scroll_speed
