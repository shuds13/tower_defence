import pygame
from tower import Tower, tower_types

pygame.mixer.init()
snd_sell = pygame.mixer.Sound('sell.wav')

cross_img = pygame.image.load('cross.png')  # Load your tower image
cross_img = pygame.transform.scale(cross_img, (50, 50))


def draw_button(surface, text, position, size, color=(0, 0, 255)):
    #font = pygame.font.SysFont(None, 36)
    font = pygame.font.SysFont(None, 30)
    button_rect = pygame.Rect(position, size)
    pygame.draw.rect(surface, color, button_rect)  # Blue button
    text_surf = font.render(text, True, (255, 255, 255))  # White text
    text_rect = text_surf.get_rect(center=button_rect.center)
    surface.blit(text_surf, text_rect)
    return button_rect


def is_click_inside_rect(click_pos, rect):
    clicked = rect.collidepoint(click_pos)
    return clicked


def play_button(window, window_size):
    x = window_size[0] - 190
    y = window_size[1] - 100
    width = 80
    height = 50
    draw_border(window, x, y, width, height, 3)
    replay_button = draw_button(window, "Replay", (x, y), (width, height))
    x += 100
    draw_border(window, x, y, width, height, 3)
    maps_button = draw_button(window, "Maps", (x, y), (width, height), (233, 116, 81))
    return replay_button, maps_button


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

    tower_rects = []
    for tower in tower_types:
        tower_rects.append(draw_tower_option(tower, y_offset))
        y_offset += 60

    rect = pygame.Rect(panel_rect.x + 10, panel_rect.y + y_offset, 180, 50)
    pygame.draw.rect(surface, (100, 100, 100), rect)  # Dark grey option box
    image_rect_1 = cross_img.get_rect(center=(rect.centerx - 40, rect.centery))
    surface.blit(cross_img, image_rect_1.topleft)
    tower_rects.append(rect)

    if current_tower_type is None:
        pygame.draw.rect(surface, (255, 255, 0), rect, 3)  # Yellow border

    return tower_rects


def draw_border(surface, x, y, width, height, border_width, color=(0,0,0)):
    pygame.draw.rect(surface, color, (x - border_width, y - border_width, width + 2 * border_width, height + 2 * border_width))


def draw_inset_window(surface, window_info, player_money):
    if not window_info['active']:
        return

    # Coordinates and dimensions for the window
    x, y, width, height = window_info['x'], window_info['y'], window_info['width'], window_info['height']
    tower = window_info['tower']

    # Draw the border
    draw_border(surface, x, y, width, height, 4, (255, 255, 255))

    # Draw the window background
    pygame.draw.rect(surface, (200, 200, 200), (x, y, width, height))

    font_title = pygame.font.SysFont('Arial', 16, bold=True)  # Choose a font and size
    font = pygame.font.SysFont(None, 24)

    # Tower name
    tower_name_text = font_title.render(tower.name.upper(), True, (0, 0, 0))  # Black text
    tower_name_rect = tower_name_text.get_rect(center=(x + width // 2, y + 20))
    surface.blit(tower_name_text, tower_name_rect.topleft)

    # Tower pops
    tower_pops_text = font.render(str(tower.total_score), True, (0, 0, 0))  # Black text
    tower_pops_rect = tower_pops_text.get_rect(center=(x + width // 2, y + 40))
    surface.blit(tower_pops_text, tower_pops_rect.topleft)

    # Draw the tower image
    image_y_pos = y + 105  # was 80
    tower_image = pygame.transform.scale(tower.image, (100, 100))
    image_rect = tower_image.get_rect(center=(x + width // 2, image_y_pos))
    surface.blit(tower_image, image_rect)

    # Draw buttons for upgrade and sell
    upgrade_y_pos = y + 175  # was 160
    upgrade_button = pygame.Rect(x + 40, upgrade_y_pos, 120, 40)
    draw_border(surface, x+40, upgrade_y_pos, 120, 40, 2)

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
        #TODO Instead of word "Upgrade" say name of upgrade tower.upgrade_name (will update with tower level)
        #burger upgrade - "extra spicy"?
        upgrade_text = font.render(f"Upgrade ${upgrade_cost}", True, (255, 255, 255))  # White text
    upgrade_text_rect = upgrade_text.get_rect(center=upgrade_button.center)
    surface.blit(upgrade_text, upgrade_text_rect)

    sell_y_pos = y + 240  # was 230

    sell_button = pygame.Rect(x + 40, sell_y_pos, 120, 40)
    draw_border(surface, x+40, sell_y_pos, 120, 40, 2)

    pygame.draw.rect(surface, (196, 30, 58), sell_button)  # Dark grey button
    # Render and draw "Sell" text and amount
    sell_text = font.render(f"Sell ${int(tower.cost * 0.8)}", True, (255, 255, 255))  # White text
    sell_text_rect = sell_text.get_rect(center=sell_button.center)
    surface.blit(sell_text, sell_text_rect)

    # Return button rects for further use (e.g., click detection)
    return upgrade_button, sell_button


def process_inset_window(mouse_pos, towers, inset_window, upgrade_button,
                         sell_button, player_money, alert_message, alert_timer, game_over):
    # Upgrade tower
    tower = inset_window['tower']
    if upgrade_button.collidepoint(mouse_pos) and not game_over:
        if tower.level < tower.__class__.max_level:
            upgrade_cost = tower.upgrade_costs[tower.level-1]
            if player_money >= upgrade_cost:
                tower.level_up()
                player_money -= upgrade_cost
    # Sell tower
    elif sell_button.collidepoint(mouse_pos) and not game_over:
        sell_val = int(tower.cost * 0.8)
        player_money += sell_val
        snd_sell.play()
        alert_message = f"Sold! (${sell_val})"
        alert_timer = 120  # Display message for 2 seconds (assuming 60 FPS)

        towers.remove(tower)
        inset_window['active'] = False
    else:
        # Close if click anywhere else
        inset_window['active'] = False

    return player_money, alert_message, alert_timer
