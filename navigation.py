import pygame
import sounds
from tower import Tower, tower_types

cross_img = pygame.image.load('images/cross.png')
cross_img = pygame.transform.scale(cross_img, (50, 50))

cog_img = pygame.image.load('images/options.png')
cog_img = pygame.transform.scale(cog_img, (40, 40))

crown_img = pygame.image.load('images/crown.png')
crown_img = pygame.transform.scale(crown_img, (100, 100))
crownace_img = pygame.image.load('images/crown_ace.png')
crownace_img = pygame.transform.scale(crownace_img, (100, 100))
troll_img = pygame.image.load('images/troll.png')
troll_img = pygame.transform.scale(troll_img, (100, 100))

frames_per_second = 60

def draw_button(surface, text, pos, size, color=(0, 0, 255), fontsize=30):
    #font = pygame.font.SysFont(None, 36)
    draw_border(surface, pos[0], pos[1], size[0], size[1], 3)
    font = pygame.font.SysFont(None, fontsize)
    button_rect = pygame.Rect(pos, size)
    pygame.draw.rect(surface, color, button_rect)  # Blue button
    text_surf = font.render(text, True, (255, 255, 255))  # White text
    text_rect = text_surf.get_rect(center=button_rect.center)
    surface.blit(text_surf, text_rect)
    return button_rect


def is_click_inside_rect(click_pos, rect):
    clicked = rect.collidepoint(click_pos)
    return clicked


def play_button(window, window_size, game):
    x = window_size[0] - 190
    #y = window_size[1] - 100
    y = window_size[1] - 160
    width = 80
    height = 50
    #draw_border(window, x, y, width, height, 3)
    if game.last_round_restarts > 0 and not game.map_complete:
        restart_text = "Restart round (" + str(game.last_round_restarts) + ")"
        restart_round = draw_button(window, restart_text, (x+15, y), (150, 40), (210, 125, 45), 25)
    else:
        restart_round = None
    y += 60
    replay_button = draw_button(window, "Replay", (x, y), (width, height))
    x += 100
    #draw_border(window, x, y, width, height, 3)
    maps_button = draw_button(window, "Maps", (x, y), (width, height), (233, 116, 81))
    return replay_button, maps_button, restart_round


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


def draw_options_cog(surface):
    # Draw the tower image
    pos = (650, 10)
    #cog_image = pygame.transform.scale(cog_image, (50, 50))
    image_rect = cog_img.get_rect(topleft=pos)
    surface.blit(cog_img, image_rect)
    return image_rect


def draw_speed_buttons(surface, x, y, width, height):

    global frames_per_second

    #y_from_centre = -60
    #s1_pos = (x + width // 2 - 120, y+height/2 + y_from_centre)
    #s15_pos = (x + width // 2 - 40, y+height/2 + y_from_centre)
    #s2_pos = (x + width // 2 +40, y+height/2 + y_from_centre)

    y_pos = y+75
    s1_pos = (x + width // 2 - 120, y_pos)
    s15_pos = (x + width // 2 - 40, y_pos)
    s2_pos = (x + width // 2 +40, y_pos)


    col_off = (132, 136, 132)
    col_on = (0,200,0)

    s1_color = col_off
    s15_color = col_off
    s2_color = col_off

    if frames_per_second == 60:
        s1_color = col_on
    elif frames_per_second == 90:
        s15_color = col_on
    elif frames_per_second == 120:
        s2_color = col_on

    s1_button = draw_button(surface, "1x", s1_pos, (80, 40), color=s1_color)
    s15_button = draw_button(surface, "1.5x", s15_pos, (80, 40), color=s15_color)
    s2_button = draw_button(surface, "2x", s2_pos, (80, 40), color=s2_color)
    return s1_button, s15_button, s2_button


def draw_sound_buttons(surface, x, y, width, height):

    #y_from_centre = 40
    #mute_pos = (x + width // 2 - 120, y+height/2 + y_from_centre)
    #quiet_pos = (x + width // 2 - 40, y+height/2 + y_from_centre)
    #normal_pos = (x + width // 2 +40, y+height/2 + y_from_centre)

    y_pos = y + 175
    mute_pos = (x + width // 2 - 120, y_pos)
    quiet_pos = (x + width // 2 - 40, y_pos)
    normal_pos = (x + width // 2 +40, y_pos)

    col_off = (132, 136, 132)
    col_on = (0,200,0)

    mute_color = col_off
    quiet_color = col_off
    normal_color = col_off

    if sounds.get_volume() == 0:
        mute_color = col_on
    elif sounds.get_volume() == 1:
        normal_color = col_on
    else:
        quiet_color = col_on

    mute_button = draw_button(surface, "Mute", mute_pos, (80, 40), color=mute_color, fontsize=27)
    quiet_button = draw_button(surface, "Quiet", quiet_pos, (80, 40), color=quiet_color, fontsize=27)
    normal_button = draw_button(surface, "Normal", normal_pos, (80, 40), color=normal_color, fontsize=27)
    return mute_button, quiet_button, normal_button


def draw_game_options(display, surface, game, x, y, width, height):
    #x, y, width, height = 100, 100, 500, 400
    draw_border(surface, x, y, width, height, 4, (255, 255, 255))

    # Draw the window background
    pygame.draw.rect(surface, (245, 245, 220), (x, y, width, height))

    font_title = pygame.font.SysFont('Arial', 24, bold=True)  # Choose a font and size

    # Should this count during the round?
    if game.active and game.last_round_restarts > 0:
        restart_color = (210, 125, 45)
        can_restart = True
        restart_text = "Restart round (" + str(game.last_round_restarts) + ")"
    elif game.last_round_restarts <= 0:
        restart_color = (100, 100, 100)
        can_restart = False
        restart_text = "No more restarts"
    else:
        restart_color = (100, 100, 100)
        can_restart = False
        restart_text = "Restart round"

    # Want to restructure this window now added these - positioning does not look good.
    #replay_button = draw_button(surface, "Replay", (x + width // 2 - 180, y+30), (80, 40), (70, 130, 180), 25)
    #maps_button = draw_button(surface, "Maps", (x + width // 2 - 80, y+30), (80, 40), (233, 116, 81), 25)

    restart_y = y+height-150
    restart_round = draw_button(surface, restart_text, (x + width // 2 - 75, restart_y), (150, 40), restart_color, 25)

    speed_text = font_title.render("Speed", True, (0, 0, 0))  # Black text
    #speed_rect = speed_text.get_rect(topleft=(x + width // 2 - 40, y+height//2 - 100))
    speed_rect = speed_text.get_rect(topleft=(x + width // 2 - 40, y+35))
    surface.blit(speed_text, speed_rect.topleft)

    sound_text = font_title.render("Sound", True, (0, 0, 0))  # Black text
    #sound_rect = sound_text.get_rect(topleft=(x + width // 2 - 40, y+height//2))
    sound_rect = sound_text.get_rect(topleft=(x + width // 2 - 40, y+135))
    surface.blit(sound_text, sound_rect.topleft)

    buttons_size = (90, 40)
    buttons_y = y+height-80
    replay_pos = (x + width//4 - buttons_size[0]//2, buttons_y)
    replay_button = draw_button(surface, "Replay", replay_pos, buttons_size, (70, 130, 180), 27)
    maps_pos = (x + width//2 - buttons_size[0]//2, buttons_y)
    maps_button = draw_button(surface, "Maps", maps_pos, buttons_size, (233, 116, 81), 27)

    done_pos =  (x + 3*width//4 - buttons_size[0]//2, buttons_y)
    done_button = draw_button(surface, "Continue", done_pos, buttons_size, (0, 163, 108), 27)

    return can_restart, restart_round, replay_button, maps_button, done_button


def draw_options_window(display, surface, options_button, game):
    global frames_per_second
    x, y, width, height = 100, 100, 500, 400
    not_done = True
    while not_done:

        # Need functionalize this due to "Are you sure" box, maybe could do at start and then
        # only if "are_you_sure" and "False".
        can_restart, restart_round, replay_button, maps_button, done_button = draw_game_options(
            display, surface, game, x, y, width, height
        )
        s1_b, s15_b, s2_b = draw_speed_buttons(surface, x, y, width, height)
        mute_b, quiet_b, normal_b = draw_sound_buttons(surface, x, y, width, height)

        display.flip()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:   # what to do here
                not_done = False
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if done_button.collidepoint(mouse_pos) or options_button.collidepoint(mouse_pos):
                    not_done = False
                    break
                elif can_restart and restart_round.collidepoint(mouse_pos):
                    return False, False, True
                elif replay_button.collidepoint(mouse_pos):
                    if are_you_sure(display, surface, "This will end current game"):
                        return True, False, False
                elif maps_button.collidepoint(mouse_pos):
                    return False, True, False
                elif s1_b.collidepoint(mouse_pos):
                    frames_per_second = 60
                elif s15_b.collidepoint(mouse_pos):
                    frames_per_second = 90
                elif s2_b.collidepoint(mouse_pos):
                    frames_per_second = 120
                elif mute_b.collidepoint(mouse_pos):
                    sounds.set_volume(0)
                elif quiet_b.collidepoint(mouse_pos):
                    sounds.set_volume(0.3)
                elif normal_b.collidepoint(mouse_pos):
                    sounds.set_volume(1)
        display.flip()

    return False, False, False


def are_you_sure(display, surface, msg, enabled=True, prompt="Are you sure?", col=((0, 0, 0))):
    x, y, width, height = 200, 200, 300, 150

    # Just thinking, if I save game progress (should be easy given already do for restart round)
    # then this would not really be necessary.

    # turns out not just drawing a rectangle border - but filled in!!!
    draw_border(surface, x, y, width, height, 4, (255, 255, 255))
    #pygame.draw.rect(surface, (255, 127, 80), (x, y, width, height))
    pygame.draw.rect(surface, col, (x, y, width, height))

    font_title = pygame.font.SysFont('Arial', 20, bold=True)  # Choose a font and size
    sure_text1 = font_title.render(msg, True, (255, 255, 255))
    text_rect1 = sure_text1.get_rect(midtop=(x+width//2, y+10))
    surface.blit(sure_text1, text_rect1)
    if enabled:
        sure_text2 = font_title.render(prompt, True, (255, 255, 255))
        text_rect2 = sure_text2.get_rect(midtop=(x+width//2, y+30))
        surface.blit(sure_text2, text_rect2)
        pos = (x + width // 2 - 90, y + height//2)
        yes_button = draw_button(surface, "Yes", pos, (80, 40), color=(250, 95, 85))
        pos = (x + width // 2 +10, y + height//2)
        no_button = draw_button(surface, "No", pos, (80, 40), color=(250, 95, 85))
    else:
        no_button = cross_img.get_rect(center=(x+width//2, y+height - 60))
        surface.blit(cross_img, no_button.topleft)
        yes_button = None

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if yes_button and yes_button.collidepoint(mouse_pos):
                    return True
                elif no_button.collidepoint(mouse_pos):
                    return False
                #elif event.key == pygame.K_ESCAPE:
                    #return False
        display.flip()


# okay really need to collect stats / player data together for this
def draw_game_over_window(display, surface, map_complete, aced):
    #x, y, width, height = 100, 100, 500, 400
    x, y, width, height = 100, 200, 500, 300

    # turns out not just drawing a rectangle border - but filled in!!!
    draw_border(surface, x, y, width, height, 4, (255, 255, 255))
    #draw_border(surface, x, y, width, height, 4)  # black

    # Draw the window background
    #color = (245, 245, 220)  # cream
    #color = (0, 0, 0)  # black
    #color = (2, 48, 32)  # dark green
    #color = (25, 25, 112) # dark blue
    #color = (48, 25, 52)  # purple
    #pygame.draw.rect(surface, color, (x, y, width, height))

    # alt translucent surface - if want border - need to fix that to be just border
    #background = pygame.Surface((width,height), pygame.SRCALPHA)
    #background.fill((245, 245, 220, 128))
    #surface.blit(background, (x,y))

    # Compare
    font_title = pygame.font.SysFont('Arial', 42, bold=True)  # Choose a font and size
    #font_title = pygame.font.SysFont(None, 72)


    #tmp to test
    #map_complete = True
    #aced = True

    if map_complete:
        color = (25, 25, 112) # dark blue
        if aced:
            complete_text = "Map Complete (Aced)!"
            image = crownace_img
        else:
            complete_text = "Map Complete!"
            image = crown_img
        game_over_text = font_title.render(complete_text, True, (196, 180, 84))
    else:
        color = (48, 25, 52)  # purple
        image = troll_img
        game_over_text = font_title.render("Game Over", True, (255, 0, 0))

    pygame.draw.rect(surface, color, (x, y, width, height))

    text_rect = game_over_text.get_rect(midtop=(x+width//2, y+10))
    surface.blit(game_over_text, text_rect)

    image_rect = image.get_rect(center=(x+width//2, y+120))
    surface.blit(image, image_rect.topleft)

    close_game_over = cross_img.get_rect(center=(x+width//2, y+height - 60))
    surface.blit(cross_img, close_game_over.topleft)

    return close_game_over


def draw_border(surface, x, y, width, height, border_width, color=(0,0,0)):
    pygame.draw.rect(surface, color, (x - border_width, y - border_width, width + 2 * border_width, height + 2 * border_width))


def draw_inset_window(surface, window_info, player_money):
    if not window_info['active']:
        return

    # Coordinates and dimensions for the window
    x, y, width, height = window_info['x'], window_info['y'], window_info['width'], window_info['height']

    tower = window_info['tower']
    totem = window_info['totem']

    # Show radius of tower
    trange = tower.current_range()
    #print(tower.range, tower.current_range())
    pygame.draw.circle(surface, (0, 255, 255), tower.position, trange, 1)

    # Draw the border
    draw_border(surface, x, y, width, height, 4, (255, 255, 255))

    # Draw the window background
    pygame.draw.rect(surface, (200, 200, 200), (x, y, width, height))

    font_title = pygame.font.SysFont('Arial', 16, bold=True)  # Choose a font and size
    font = pygame.font.SysFont(None, 24)

    if totem is not None:
        #import pdb;pdb.set_trace()
        totem_image = pygame.transform.scale(totem.image, (50, 50))
        image_rect = totem_image.get_rect(topleft=(x+width-55, y+30))
        surface.blit(totem_image, image_rect)

    # Tower name
    tower_name_text = font_title.render(tower.name.upper(), True, (0, 0, 0))  # Black text
    tower_name_rect = tower_name_text.get_rect(center=(x + width // 2, y + 20))
    surface.blit(tower_name_text, tower_name_rect.topleft)

    # Tower pops
    if tower.attack_tower:
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
    upgrade_button = pygame.Rect(x + 30, upgrade_y_pos, 140, 40)
    draw_border(surface, x+30, upgrade_y_pos, 140, 40, 2)
    # DONT really like bigger button - looked better before - TODO might adjust size if needed

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
        upgrade_text = font.render(f"{tower.upgrade_name} ${upgrade_cost}", True, (255, 255, 255))  # White text
    upgrade_text_rect = upgrade_text.get_rect(center=upgrade_button.center)
    surface.blit(upgrade_text, upgrade_text_rect)

    sell_y_pos = y + 240  # was 230

    sell_button = pygame.Rect(x + 30, sell_y_pos, 140, 40)
    draw_border(surface, x+30, sell_y_pos, 140, 40, 2)

    pygame.draw.rect(surface, (196, 30, 58), sell_button)  # Dark grey button
    # Render and draw "Sell" text and amount
    sell_text = font.render(f"Sell ${int(tower.cost * 0.8)}", True, (255, 255, 255))  # White text
    sell_text_rect = sell_text.get_rect(center=sell_button.center)
    surface.blit(sell_text, sell_text_rect)

    # Return button rects for further use (e.g., click detection)
    return upgrade_button, sell_button


def process_inset_window(mouse_pos, towers, totems, inset_window, upgrade_button,
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
        sounds.play('sell')
        alert_message = f"Sold! (${sell_val})"
        alert_timer = 120  # Display message for 2 seconds (assuming 60 FPS)
        towers.remove(tower)
        if tower.__class__.name == "Totem":
            totems.remove(tower)
        inset_window['active'] = False
    else:
        # Close if click anywhere else
        inset_window['active'] = False

    return player_money, alert_message, alert_timer
