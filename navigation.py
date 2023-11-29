import pygame
from tower import Tower, tower_types

cross_img = pygame.image.load('cross.png')  # Load your tower image
cross_img = pygame.transform.scale(cross_img, (50, 50))


def draw_button(surface, text, position, size, color=(0, 0, 255)):
    font = pygame.font.SysFont(None, 36)
    button_rect = pygame.Rect(position, size)
    pygame.draw.rect(surface, color, button_rect)  # Blue button
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
    border_color = (0, 0, 0)
    bw = 2  # Width of the border, change as needed
    pygame.draw.rect(window, border_color, (window_size[0] - 125 - bw,window_size[1] - 100 - bw, 50 + 2 * bw, 50 + 2 * bw))
    return draw_button(window, "Go", (window_size[0] - 125, window_size[1] - 100), (50, 50), (0,200,20))


def draw_side_panel(surface, panel_rect, current_tower_type):
    # Draw the background of the side panel
    pygame.draw.rect(surface, (200, 200, 200), panel_rect)  # Light grey background
    font = pygame.font.SysFont(None, 24)
    y_offset = 10

    def draw_tower_option(tower_type, y_offset):
        # Draw tower selection options (simple rectangles or icons)
        rect = pygame.Rect(panel_rect.x + 10, panel_rect.y + y_offset, 180, 50)
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

    #TODO incorporate with above
    rect = pygame.Rect(panel_rect.x + 10, panel_rect.y + y_offset, 180, 50)
    pygame.draw.rect(surface, (100, 100, 100), rect)  # Dark grey option box
    image_rect_1 = cross_img.get_rect(center=(rect.centerx - 40, rect.centery))
    surface.blit(cross_img, image_rect_1.topleft)
    tower_rects.append(rect)

    if current_tower_type is None:
        pygame.draw.rect(surface, (255, 255, 0), rect, 3)  # Yellow border

    return tower_rects


def draw_inset_window(surface, window_info, player_money):
    if not window_info['active']:
        return

    # Coordinates and dimensions for the window
    x, y, width, height = window_info['x'], window_info['y'], window_info['width'], window_info['height']

    # Draw the border
    border_color = (255, 255, 255)  # White border, change as needed
    border_width = 4  # Width of the border, change as needed
    pygame.draw.rect(surface, border_color, (x - border_width, y - border_width, width + 2 * border_width, height + 2 * border_width))

    # Draw the window background
    pygame.draw.rect(surface, (200, 200, 200), (x, y, width, height))


    # Draw the window background
    rect = (window_info['x'], window_info['y'], window_info['width'], window_info['height'])
    pygame.draw.rect(surface, (200, 200, 200), rect)  # Light grey background

    # Draw the tower image (replace with actual tower image)


    tower = window_info['tower']

    if tower:
        # Maybe best to use bigger versions of original image
        tower_image = pygame.transform.scale(tower.image, (100, 100))
        image_rect = tower_image.get_rect(center=(window_info['x'] + window_info['width'] // 2, window_info['y'] + 80))
        surface.blit(tower_image, image_rect)

    #font = pygame.font.SysFont('Arial', 16)  # Choose a font and size
    font = pygame.font.SysFont(None, 24)


    # Draw buttons for upgrade and sell (placeholder rectangles here)
    upgrade_button = pygame.Rect(window_info['x'] + 40, window_info['y'] + 160, 120, 40)

    border_color = (0, 0, 0)
    bw = 2  # Width of the border, change as needed
    pygame.draw.rect(surface, border_color, (window_info['x'] + 40  - bw, window_info['y'] + 160 - bw, 120 + 2 * bw, 40 + 2 * bw))


    # Render and draw "Upgrade" text and amount
    #upgrade_text = font.render(f"Upgrade ${int(tower.next_upgrade_cost())}", True, (255, 255, 255))  # White text

    #again could use  x=y=z
    #at_max_level = tower.level == tower.__class__.max_level
    if tower.level == tower.__class__.max_level:
        at_max_level = True
    else:
        at_max_level = False

    if at_max_level:
        upgrade_color = (0, 128, 128)
    else:
        upgrade_cost = tower.upgrade_costs[tower.level-1]
        if player_money < upgrade_cost:
            upgrade_color = (100, 100, 100)
        else:
            upgrade_color = (80, 200, 120)

    pygame.draw.rect(surface, upgrade_color, upgrade_button)  # Dark grey button

    if at_max_level:
        upgrade_text = font.render(f"Max Level", True, (255, 255, 255))  # White text
    else:
        #TODO what if dont have the money? Need diff color when available
        upgrade_text = font.render(f"Upgrade ${upgrade_cost}", True, (255, 255, 255))  # White text
    upgrade_text_rect = upgrade_text.get_rect(center=upgrade_button.center)
    surface.blit(upgrade_text, upgrade_text_rect)

    sell_button = pygame.Rect(window_info['x'] + 40, window_info['y'] + 230, 120, 40)
    pygame.draw.rect(surface, border_color, (window_info['x'] + 40  - bw, window_info['y'] + 230 - bw, 120 + 2 * bw, 40 + 2 * bw))


    pygame.draw.rect(surface, (196, 30, 58), sell_button)  # Dark grey button
    # Render and draw "Sell" text and amount
    sell_text = font.render(f"Sell ${int(tower.cost * 0.8)}", True, (255, 255, 255))  # White text
    sell_text_rect = sell_text.get_rect(center=sell_button.center)
    surface.blit(sell_text, sell_text_rect)

    # Return button rects for further use (e.g., click detection)
    return upgrade_button, sell_button


