import pygame
from tower import Tower, tower_types


def draw_button(surface, text, position, size):
    font = pygame.font.SysFont(None, 36)
    button_rect = pygame.Rect(position, size)
    pygame.draw.rect(surface, (0, 0, 255), button_rect)  # Blue button
    text_surf = font.render(text, True, (255, 255, 255))  # White text
    text_rect = text_surf.get_rect(center=button_rect.center)
    surface.blit(text_surf, text_rect)
    return button_rect


def is_click_inside_rect(click_pos, rect):
    clicked = rect.collidepoint(click_pos)
    #print(f"{clicked=}")  #test
    return clicked


def play_button(window, window_size):
    return draw_button(window, "Play Again", (window_size[0] / 2 - 150, window_size[1] / 2 + 50), (200, 50))


def start_level_button(window, window_size):
    return draw_button(window, "Go", (window_size[0] - 125, window_size[1] - 100), (50, 50))


def draw_side_panel(surface, panel_rect, current_tower_type):
    # Draw the background of the side panel
    pygame.draw.rect(surface, (200, 200, 200), panel_rect)  # Light grey background
    font = pygame.font.SysFont(None, 24)
    y_offset = 10

    def draw_tower_option(tower_type, y_offset):
        # Draw tower selection options (simple rectangles or icons)
        rect = pygame.Rect(panel_rect.x + 10, panel_rect.y + y_offset, 180, 50)  # Example
        pygame.draw.rect(surface, (100, 100, 100), rect)  # Dark grey option box

        image_rect_1 = tower_type.image.get_rect(center=(rect.centerx - 40, rect.centery))
        surface.blit(tower_type.image, image_rect_1.topleft)
        price_text_1 = font.render(f"${tower_type.price}", True, (0, 0, 0))
        surface.blit(price_text_1, (image_rect_1.right + 5, rect.centery - 10))

        if current_tower_type is not None:
            if tower_type.name == current_tower_type.name:
                pygame.draw.rect(surface, (255, 255, 0), rect, 3)  # Yellow border

        return rect

    #TODO make image part of tower class and use tower_type.image
    tower_rects = []
    for tower in tower_types:  # keep this list in tower module
        tower_rects.append(draw_tower_option(tower, y_offset))
        y_offset += 60

    return tower_rects
