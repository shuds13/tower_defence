import pygame
import levels
from assets import load_image, sys_font
import sounds
from tower import Tower, tower_types, burger5_img

cross_img = load_image('images/cross.png')
cross_img = pygame.transform.scale(cross_img, (50, 50))

cog_img = load_image('images/options.png')
cog_img = pygame.transform.scale(cog_img, (40, 40))

crown_img = load_image('images/crown.png')
crown_img = pygame.transform.scale(crown_img, (100, 100))
crownace_img = load_image('images/crown_ace.png')
crownace_img = pygame.transform.scale(crownace_img, (100, 100))
crown_extended_img = pygame.transform.scale(load_image('images/crown_extended.png'), (100, 100))  # placeholder art
troll_img = load_image('images/troll.png')
troll_img = pygame.transform.scale(troll_img, (100, 100))

frames_per_second = 60
# frames_per_second = 30 # testing

def is_hovered(rect):
    """True if the mouse is over this rect"""
    return rect is not None and rect.collidepoint(pygame.mouse.get_pos())


def hover_color(color, rect):
    """Slightly darker version of a button colour while the mouse is over it"""
    if not is_hovered(rect):
        return color
    return tuple(round(c * 0.82) for c in color[:3])


def draw_button(surface, text, pos, size, color=(0, 0, 255), fontsize=30):
    #font = sys_font(None, 36)
    draw_border(surface, pos[0], pos[1], size[0], size[1], 3)
    font = sys_font(None, fontsize)
    button_rect = pygame.Rect(pos, size)
    pygame.draw.rect(surface, hover_color(color, button_rect), button_rect)  # Blue button
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


def draw_surge_button(surface, burger, inset):
    """Burger King button, bottom left of the map (moved right if the tower box is open there).
    Shows ready, surging or cooling down."""
    x, y, size = 10, 540, 50
    if inset['active'] and inset['x'] == inset['xl']:
        x = inset['x'] + inset['width'] + 10
    rect = pygame.Rect(x, y, size, size)
    icon = pygame.transform.smoothscale(burger5_img, (size - 4, size - 4))
    if burger.surge_timer > 0:
        border, background = (255, 140, 0), (255, 200, 80)  # surging
    elif burger.surge_cooldown > 0:
        border, background = (60, 60, 60), (150, 150, 150)  # cooling down
        icon = pygame.transform.grayscale(icon)
    else:
        border, background = (255, 215, 0), hover_color((120, 20, 0), rect)  # ready
    draw_border(surface, x, y, size, size, 3, border)
    pygame.draw.rect(surface, background, rect)
    if burger.surge_cooldown > 0:
        # Fill rises as the cooldown runs down
        done = 1 - burger.surge_cooldown / burger.__class__.surge_cooldown_frames
        fill = int(size * done)
        pygame.draw.rect(surface, (200, 120, 60), (x, y + size - fill, size, fill))
    surface.blit(icon, icon.get_rect(center=rect.center))
    return rect


def draw_side_panel(surface, panel_rect, current_tower_type):
    # Draw the background of the side panel
    pygame.draw.rect(surface, (200, 200, 200), panel_rect)  # Light grey background
    font = sys_font(None, 24)
    y_offset = 10

    def draw_tower_option(tower_type, y_offset):
        # Draw tower selection options (simple rectangles or icons)
        rect = pygame.Rect(panel_rect.x + 10, panel_rect.y + y_offset, 180, 50)
        pygame.draw.rect(surface, hover_color((100, 100, 100), rect), rect)  # Dark grey option box

        image_rect_1 = tower_type.image.get_rect(center=(rect.centerx - 40, rect.centery))
        surface.blit(tower_type.image, image_rect_1.topleft)
        price_text_1 = font.render(f"${tower_type.price}", True, (0, 0, 0))
        surface.blit(price_text_1, (image_rect_1.right + 5, rect.centery - 10))
        if tower_type.new_tower:
            price_width = price_text_1.get_width()
            new_text_1 = font.render("(New)", True, (0, 0, 0))
            surface.blit(new_text_1, (image_rect_1.right + price_width + 10, rect.centery - 10))

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

    font_title = sys_font('Arial', 24, bold=True)  # Choose a font and size

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

    font_title = sys_font('Arial', 20, bold=True)  # Choose a font and size
    sure_text1 = font_title.render(msg, True, (255, 255, 255))
    text_rect1 = sure_text1.get_rect(midtop=(x+width//2, y+10))
    surface.blit(sure_text1, text_rect1)
    if enabled:
        sure_text2 = font_title.render(prompt, True, (255, 255, 255))
        text_rect2 = sure_text2.get_rect(midtop=(x+width//2, y+30))
        surface.blit(sure_text2, text_rect2)
    else:
        no_button = cross_img.get_rect(center=(x+width//2, y+height - 60))
        surface.blit(cross_img, no_button.topleft)
        yes_button = None

    while True:
        if enabled:  # redrawn each time round so they light up under the mouse
            yes_button = draw_button(surface, "Yes", (x + width // 2 - 90, y + height//2), (80, 40), color=(250, 95, 85))
            no_button = draw_button(surface, "No", (x + width // 2 + 10, y + height//2), (80, 40), color=(250, 95, 85))
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


def remove_window(display, surface, name, image, price, money):
    """Ask whether to pay to clear an obstacle. Returns True if the player chose to remove it."""
    # Dim the game behind the window
    shade = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    shade.fill((0, 0, 0, 140))
    surface.blit(shade, (0, 0))

    x, y, width, height = 175, 150, 350, 290
    panel = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, (30, 28, 48), panel, border_radius=14)
    pygame.draw.rect(surface, (196, 180, 84), panel, 3, border_radius=14)

    affordable = money >= price
    title = sys_font('Arial', 24, bold=True).render(f"Clear the {name}?" if affordable else f"Can't clear the {name}", True, (255, 255, 255))
    surface.blit(title, title.get_rect(midtop=(panel.centerx, y + 14)))

    # Picture of the obstacle, fitted into a box keeping its shape
    iw, ih = image.get_size()
    fit = min(130 / iw, 100 / ih)
    picture = pygame.transform.smoothscale(image, (round(iw * fit), round(ih * fit)))
    surface.blit(picture, picture.get_rect(center=(panel.centerx, y + 110)))

    price_text = sys_font('Arial', 26, bold=True).render(f"${price}", True, (196, 180, 84))
    surface.blit(price_text, price_text.get_rect(center=(panel.centerx, y + 180)))
    if not affordable:
        short_text = sys_font(None, 22).render(f"You have ${int(money)}", True, (230, 120, 120))
        surface.blit(short_text, short_text.get_rect(center=(panel.centerx, y + 205)))

    def button(text, rect, color):
        pygame.draw.rect(surface, hover_color(color, rect), rect, border_radius=10)
        pygame.draw.rect(surface, (255, 255, 255), rect, 2, border_radius=10)
        label = sys_font(None, 30).render(text, True, (255, 255, 255))
        surface.blit(label, label.get_rect(center=rect.center))
        return rect

    def draw_buttons():
        if affordable:
            return (button("Remove", pygame.Rect(x + 45, y + 222, 120, 46), (0, 150, 60)),
                    button("Cancel", pygame.Rect(x + 185, y + 222, 120, 46), (90, 90, 110)))
        return None, button("OK", pygame.Rect(panel.centerx - 60, y + 228, 120, 46), (90, 90, 110))

    while True:
        yes_button, no_button = draw_buttons()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.post(event)  # let the main loop close the game
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if yes_button and yes_button.collidepoint(mouse_pos):
                    return True
                if no_button.collidepoint(mouse_pos) or not panel.collidepoint(mouse_pos):
                    return False
        display.flip()


# okay really need to collect stats / player data together for this
def draw_crown_window(surface, aced):
    """Box shown when the crown is first achieved mid-game. Returns the Continue and Maps buttons."""
    x, y, width, height = 100, 140, 500, 340
    draw_border(surface, x, y, width, height, 4, (255, 255, 255))
    pygame.draw.rect(surface, (25, 25, 112), (x, y, width, height))
    title = "Crown Achieved (Aced)!" if aced else "Crown Achieved!"
    title_text = sys_font('Arial', 38, bold=True).render(title, True, (196, 180, 84))
    surface.blit(title_text, title_text.get_rect(midtop=(x + width // 2, y + 12)))
    image = crownace_img if aced else crown_img
    surface.blit(image, image.get_rect(center=(x + width // 2, y + 115)))
    line = sys_font(None, 30).render("Tier 5 towers unlocked on this map", True, (255, 255, 255))
    surface.blit(line, line.get_rect(center=(x + width // 2, y + 190)))
    note = sys_font(None, 22).render("Advanced levels (Beta) - your progress is saved either way", True, (190, 190, 220))
    surface.blit(note, note.get_rect(center=(x + width // 2, y + 220)))
    continue_button = draw_button(surface, "Continue", (x + 90, y + 255), (140, 50), (0, 160, 40))
    maps_button = draw_button(surface, "Maps", (x + 270, y + 255), (140, 50), (0, 0, 200))
    return continue_button, maps_button


def draw_game_complete_window(surface, max_level):
    """Box shown when the last level is won: the platinum crown. Returns the close button."""
    x, y, width, height = 100, 120, 500, 380
    draw_border(surface, x, y, width, height, 4, (255, 255, 255))
    pygame.draw.rect(surface, (25, 25, 112), (x, y, width, height))
    title = sys_font('Arial', 42, bold=True).render("Platinum Crown!", True, (220, 225, 240))
    surface.blit(title, title.get_rect(midtop=(x + width // 2, y + 12)))
    image = pygame.transform.smoothscale(crown_extended_img, (140, 140))
    surface.blit(image, image.get_rect(center=(x + width // 2, y + 140)))
    line = sys_font(None, 32).render(f"All {max_level} levels complete on this map", True, (255, 255, 255))
    surface.blit(line, line.get_rect(center=(x + width // 2, y + 230)))
    note = sys_font(None, 28).render("You've beaten the game!", True, (196, 180, 84))
    surface.blit(note, note.get_rect(center=(x + width // 2, y + 262)))
    close_button = pygame.Rect(0, 0, 140, 46)
    close_button.center = (x + width // 2, y + height - 55)
    pygame.draw.rect(surface, hover_color((0, 150, 60), close_button), close_button, border_radius=10)
    pygame.draw.rect(surface, (255, 255, 255), close_button, 2, border_radius=10)
    label = sys_font(None, 30).render("Close", True, (255, 255, 255))
    surface.blit(label, label.get_rect(center=close_button.center))
    return close_button


def draw_game_over_window(display, surface, map_complete, aced, extended=False):
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
    font_title = sys_font('Arial', 42, bold=True)  # Choose a font and size
    #font_title = sys_font(None, 72)


    #tmp to test
    #map_complete = True
    #aced = True

    if map_complete and extended:
        return draw_game_complete_window(surface, levels.max_level)
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


def draw_inset_window(surface, window_info, player_money, game_level, map_crowned=False, towers=()):
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

    font_title = sys_font('Arial', 16, bold=True)  # Choose a font and size
    font = sys_font(None, 24)

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
    image_y_pos = y + 104  # was 80
    # Crop empty margins, then fit within 100 wide x 90 high keeping its shape, leaving a gap above the level line
    picture = tower.card_picture()
    visible = picture.subsurface(picture.get_bounding_rect(min_alpha=40))
    iw, ih = visible.get_size()
    fit = min(100 / iw, 90 / ih)
    resize = pygame.transform.smoothscale if fit < 1 else pygame.transform.scale  # smooth only when shrinking
    tower_image = resize(visible, (round(iw * fit), round(ih * fit)))
    image_rect = tower_image.get_rect(center=(x + width // 2, image_y_pos))
    surface.blit(tower_image, image_rect)

    # Level dots (filled up to the current level, gold for tier 5) followed by the level name
    max_level = tower.__class__.max_level
    dot_spacing = 11
    dots_width = max_level * dot_spacing
    level_name = tower.level_name()
    name_text = sys_font(None, 19).render(level_name, True, (60, 60, 60)) if level_name else None
    line_width = dots_width + (6 + name_text.get_width() if name_text else 0)
    line_x = x + width // 2 - line_width // 2
    line_y = y + 166
    reachable = tower.max_level_at(map_crowned)
    for i in range(max_level):
        centre = (line_x + i * dot_spacing + 4, line_y)
        if i < tower.level:
            pygame.draw.circle(surface, (255, 200, 0) if i == 4 else (60, 150, 60), centre, 4)
        elif i < reachable:
            pygame.draw.circle(surface, (150, 150, 150), centre, 4)
        else:
            pygame.draw.circle(surface, (120, 120, 120), centre, 4, 1)  # locked level: outline only
    if name_text:
        surface.blit(name_text, name_text.get_rect(midleft=(line_x + dots_width + 6, line_y)))

    # Tower option, e.g. targeting (cycles when clicked); click area is a little larger than the text
    target_button = None
    option_text = tower.option_text()
    if option_text is not None:
        font_small = sys_font(None, 20)
        target_rect = font_small.render(option_text, True, (50, 50, 90)).get_rect(center=(x + width // 2, y + 184))
        target_button = target_rect.inflate(10, 6)
        target_hover = is_hovered(target_button)
        target_text = font_small.render(option_text, True, (20, 20, 200) if target_hover else (50, 50, 90))
        surface.blit(target_text, target_rect)

    # Draw buttons for upgrade and sell
    upgrade_y_pos = y + 198  # was 160
    upgrade_button = pygame.Rect(x + 30, upgrade_y_pos, 140, 40)
    draw_border(surface, x+30, upgrade_y_pos, 140, 40, 2)
    # DONT really like bigger button - looked better before - TODO might adjust size if needed

    #at_max_level = tower.level == tower.__class__.max_level
    at_max_level = tower.level >= tower.__class__.max_level
    locked = not at_max_level and tower.level >= tower.max_level_at(map_crowned)
    only_one = not at_max_level and not locked and tower.next_level_taken(towers)

    if at_max_level:
        upgrade_color = (0, 128, 128)
    elif locked or only_one:
        upgrade_color = (100, 100, 100)
    else:
        upgrade_cost = tower.upgrade_costs[tower.level-1]
        if player_money < upgrade_cost:
            upgrade_color = (100, 100, 100)
        else:
            upgrade_color = hover_color((80, 200, 120), upgrade_button)  # only highlights when it can be bought

    pygame.draw.rect(surface, upgrade_color, upgrade_button)  # Dark grey button

    if at_max_level:
        upgrade_text = font.render(f"Max Level", True, (255, 255, 255))  # White text
        upgrade_text_rect = upgrade_text.get_rect(center=upgrade_button.center)
        surface.blit(upgrade_text, upgrade_text_rect)
    elif locked or only_one:
        # Tier 5: not unlocked yet on this map, or limited to one of each tower
        cx, cy = upgrade_button.center
        name_text = font.render(tower.upgrade_name, True, (255, 255, 255))
        surface.blit(name_text, name_text.get_rect(center=(cx, cy - 8)))
        note = "Locked" if locked else "Only one allowed"
        note_text = sys_font(None, 20).render(note, True, (255, 255, 255))
        surface.blit(note_text, note_text.get_rect(center=(cx, cy + 10)))
    else:
        # Upgrade name on the first line, price on the second
        cx, cy = upgrade_button.center
        name_text = font.render(tower.upgrade_name, True, (255, 255, 255))  # White text
        surface.blit(name_text, name_text.get_rect(center=(cx, cy - 8)))
        price_text = sys_font(None, 20).render(f"${upgrade_cost}", True, (255, 255, 255))
        surface.blit(price_text, price_text.get_rect(center=(cx, cy + 10)))

    sell_y_pos = y + 250  # was 230

    sell_button = pygame.Rect(x + 30, sell_y_pos, 140, 40)
    draw_border(surface, x+30, sell_y_pos, 140, 40, 2)

    pygame.draw.rect(surface, hover_color((196, 30, 58), sell_button), sell_button)
    # Render and draw "Sell" text and amount
    sell_text = font.render(f"Sell ${int(tower.cost * 0.8)}", True, (255, 255, 255))  # White text
    sell_text_rect = sell_text.get_rect(center=sell_button.center)
    surface.blit(sell_text, sell_text_rect)

    # Return button rects for further use (e.g., click detection)
    return upgrade_button, sell_button, target_button


def process_inset_window(mouse_pos, towers, totems, inset_window, upgrade_button,
                         sell_button, target_button, player_money, alert_message, alert_timer, game_over, game_level, map_crowned=False):
    on_window = False  # was click on window
    tower = inset_window['tower']
    # Change targeting
    if target_button is not None and target_button.collidepoint(mouse_pos):
        tower.next_option()
        on_window = True
    # Upgrade tower
    elif upgrade_button.collidepoint(mouse_pos) and not game_over:
        if tower.level < tower.max_level_at(map_crowned) and not tower.next_level_taken(towers):
            upgrade_cost = tower.upgrade_costs[tower.level-1]
            if player_money >= upgrade_cost:
                tower.level_up()
                player_money -= upgrade_cost
        elif tower.level < tower.__class__.max_level and tower.level >= tower.max_level_at(map_crowned):
            alert_message = "Needs this map's crown"
            alert_timer = 120
        on_window = True
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
        on_window = True
    else:
        # Close if click anywhere else
        inset_window['active'] = False

    return player_money, alert_message, alert_timer, on_window
