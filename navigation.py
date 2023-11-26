import pygame

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
