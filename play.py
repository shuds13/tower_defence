#!/usr/bin/env python

# Author: Stephen Hudson

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import sys
from enemy import Enemy
from tower import Tower, tower_types, Totem, CannonBall
import placements as place
import navigation as nav
import levels as lev
from maps import map_window
import sounds
import hints
from accounts import Account, load_profile, load_most_recent_profile, save_profile
from game_metrics import Game

pygame.font.init()  # Initialize font module

# Current defaults: 30 / 150 / 1
initial_lives = 30
initial_money = 150
initial_level = 1
print_total_money = False
init_last_round_restarts = 5
restart_testing = False
print_pos = False

# Initialize Pygame
pygame.init()

pygame.display.set_caption("Tower Defense Game")
clock = pygame.time.Clock()

# Set up the display
window_size = (900, 600)
window = pygame.display.set_mode(window_size)
side_panel_width = 200
side_panel_height = window_size[1]  # same as the game window height
side_panel_rect = pygame.Rect(window_size[0] - side_panel_width, 0, side_panel_width, side_panel_height)

icon = pygame.image.load('images/icon.ico') #pygame.Surface()
pygame.display.set_icon(icon)

inset_window = {
    'active': False,
    'x': 4,  # X position of the window
    'xl': 4,
    'xr': window_size[0] - side_panel_width - 204,
    'y': window_size[1] - 304,  # Y position of the window
    'width': 200,
    'height': 300,
    'tower': None,
    'totem': None
}

projectiles = []

try:
    account = load_most_recent_profile()
except Exception:
    # create new default profile
    save_profile("default")
    account = load_profile("default.pkl")

test_setup = []  # Empty list means no setup.

# test_setup = [(1,(360,300),4), (3, (400,300), 1)]

game = Game(initial_money, initial_level, initial_lives, init_last_round_restarts,
            lev, print_total_money, inset_window, test_setup)

def reset_game(gmap=None):
    game = Game(initial_money, initial_level, initial_lives, init_last_round_restarts,
                lev, print_total_money, inset_window, test_setup)
    if gmap is not None:
        gmap = gmap.__class__()  # Reset map - only needed if removables.
        game.set_map(gmap)
        # in case starting at a different level
        gmap.map_update(initial_level) #, newstart=True)
    return game, gmap

def in_range(my_range, mouse_x, mouse_y, obj):
    distance = ((mouse_x - obj.position[0])**2 + (mouse_y - obj.position[1])**2)**0.5
    return distance <= my_range

def in_range2(my_range, mouse_x, mouse_y, obj):
    distance = ((obj.position[0] - mouse_x)**2 + (obj.position[1] - mouse_y)**2)**0.5
    return distance <= my_range

# Can use gmap attributes inline but for now
def set_map(gmap):
    global pygame, map_name, paths, background_color, path_thickness, path_color
    map_name = gmap.name
    paths = gmap.paths
    #background_color = gmap.background_color  # should use in place - esp if can change
    path_thickness = gmap.path_thickness
    path_color = gmap.path_color
    pygame.display.set_caption("Tower Defense Game" + f" ({gmap.name})")
    return gmap

def select_map():
    global pygame, window, window_size, game, account  # send to func
    gmap, account = map_window(pygame.display, window, window_size, account)
    if gmap is None:
        game.running = False
        return
    gmap = set_map(gmap)
    game.set_map(gmap)
    # TODO put this in account (profile) function.
    if gmap.name in account.maps_in_progress:
        game = account.maps_in_progress[gmap.name]
        game.restart_round(lev, gmap, decrement=False)  # TODO lev could just be imported in game_metrics
        game.reset_level(gmap, pygame.display, window)
    return gmap

play_again_button = None  # To store the button rectangle
start_level_button = None  # To store the button rectangle
restart_round_button = None
hint_button = None
close_game_over = None
maps_button = None

opts_play_again = False
opts_maps = False
opts_restart = False

alert_message = ""
alert_timer = 0
# restart_timer = 20000

gmap = select_map()
options_button = nav.draw_options_cog(window)

def select_tower_type(tower_types):
    for i in range(len(tower_types)):
        if tower_option_rects[i].collidepoint(mouse_pos):
            return i
    return None

def update_inset_totems(inset_window):
    my_totem = None
    tower = inset_window['tower']
    inset_window['totem'] = None
    if tower.__class__.name != "Totem":
        for totem in game.totems:
            if totem.tower_in_range(tower):
                if my_totem is None or totem.level > my_totem.level:
                    my_totem = totem
        inset_window['totem'] = my_totem

def show_tower_info(inset_window):
    for tower in game.towers:
        if tower.is_clicked(mouse_pos):
            inset_window['active'] = True
            inset_window['tower'] = tower
            update_inset_totems(inset_window)
            return True
    return False

game.set_money_per_hit()

# Game loop
while game.running:

    #for now
    paths = gmap.paths

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # For helping make maps - comment out when done
            if print_pos:
                print(mouse_pos)

            if options_button.collidepoint(mouse_pos):
                #nav.draw_options_window(pygame.display, window, options_button)
                opts_play_again, opts_maps, opts_restart = nav.draw_options_window(pygame.display, window, options_button, game)
                # prevents restart round from working
                #continue  # stops you accidently placing tower on cog and dont need to send it to is_valid_position

            gmap.background_mod(mouse_pos, window)

            #if game.game_over or restart_testing:
            if opts_restart or restart_round_button and nav.is_click_inside_rect(mouse_pos, restart_round_button):
                game.restart_round(lev, gmap)
                game.reset_level(gmap, pygame.display, window)
                opts_restart = False

            #if game.game_over:
            if close_game_over and  nav.is_click_inside_rect(mouse_pos, close_game_over):
                close_game_over = None
                game.displayed_game_over = True
            if opts_play_again or play_again_button and nav.is_click_inside_rect(mouse_pos, play_again_button):
                game, gmap = reset_game(gmap=gmap)
                opts_play_again = False
            if opts_maps or maps_button and nav.is_click_inside_rect(mouse_pos, maps_button):
                game, _ = reset_game()
                gmap = select_map()
                opts_maps = False
                continue
            else:
                # If GO button is clicked then start level
                if not game.active and start_level_button:
                    if nav.is_click_inside_rect(mouse_pos, start_level_button):
                        game.active = True
                        start_level_button = None
                        continue
                    if hint_button and nav.is_click_inside_rect(mouse_pos, hint_button):
                        hint_button = None
                        game.shown_hint = True
                        continue
                # Is cross clicked to deselect a tower
                if tower_option_rects[-1].collidepoint(mouse_pos):
                    game.current_tower_type = None
                    continue

                # Select a tower
                new_type = select_tower_type(tower_types)
                if new_type is not None:
                    game.current_tower_type = tower_types[new_type]
                    continue

            if game.current_tower_type is None:

                # Process clicks in the info window
                if game.inset_window['active']:
                    # should use object for inset window parameters
                    game.player_money, alert_message, alert_timer = nav.process_inset_window(
                        mouse_pos, game.towers, game.totems, game.inset_window, upgrade_button, sell_button, game.player_money,
                        alert_message, alert_timer, game.game_over
                    )
                else:
                    removables = gmap.get_removables()
                    if removables:  #unnecessary
                        for rem in removables:
                            if rem.rect.collidepoint(mouse_pos):
                                #todo replace with window - and ok button
                                #print(f"Remove {rem.price}")
                                msg = f"Remove for {rem.price}"
                                if game.player_money >= rem.price:
                                    #window_was = pygame.Surface(window_size)
                                    #window_was.blit( window, ( 0, 0 ), ( 0, 0, window_size[0], window_size[1] ) )
                                    #window_was = window.copy()
                                    if nav.are_you_sure(pygame.display, window, msg, True, "", (0, 0, 128)):
                                        #pygame.display.flip()
                                        game.player_money -= rem.price
                                        #gmap.remove(rem, pygame.display, window_was)
                                        gmap.remove(rem, pygame.display, window)
                                else:
                                    nav.are_you_sure(pygame.display, window, msg, False, "", (128,128,128))

                # If user clicked on tower - open the info (inset) window
                if show_tower_info(game.inset_window):
                    #if mouse_pos[0] < (window_size[0] - side_panel_width) // 2:  # left side of window
                    # only if over inset
                    if mouse_pos[0] < game.inset_window['width'] + 50 and mouse_pos[1] > game.inset_window['y'] - 50:
                        game.inset_window['x'] = game.inset_window['xr']
                    else:
                        game.inset_window['x'] = game.inset_window['xl']
                    upgrade_button, sell_button = nav.draw_inset_window(window, game.inset_window, game.player_money)

            # Place a tower
            else:
            #elif game.current_tower_type is not None:
                if place.is_valid_position(game.current_tower_type, mouse_pos, paths, game.towers, options_button, gmap):
                    if game.player_money >= game.current_tower_type.price:
                        newtower = game.current_tower_type(position=mouse_pos)
                        game.towers.append(newtower)
                        if isinstance(newtower, Totem):
                            game.totems.append(newtower)
                        sounds.play('place')
                        game.player_money -= game.current_tower_type.price
                        game.current_tower_type = None  # This deselects tower when put down (could be option)
                    else:
                        alert_message = "Not enough money!"
                        alert_timer = 120  # Display message for 2 seconds (assuming 60 FPS)
                else:
                    alert_message = "Cant place here"
                    alert_timer = 120  # Display message for 2 seconds (assuming 60 FPS)

    # prevent flash of level when close from map screen
    if not game.running:
        break

    if game.game_over:
        pygame.display.flip()  # Update the full display Surface to the screen
        # restart_timer -= 1
        # if restart_timer <=0:
            # game.running = False
        game.active = False

    # Work this out every time then okay with buying selling etc...
    for tower in game.towers:
        tower.speed_mod = 1
        tower.range_mod = 1
        tower.see_ghosts = tower.__class__.see_ghosts

    for totem in game.totems:
        for tower in game.towers:
            if totem.tower_in_range(tower):
                totem.boost(tower)

    if game.active:
        # Spawn a new enemy at intervals if the max number has not been reached
        if not game.level.done():
            game.enemy_spawn_timer += 1
            if game.enemy_spawn_timer >= game.level.interval():

                #path = paths[0]
                path = paths[game.path_id]
                game.level.spawn_enemy(game.enemies, path)  # Type will be determined also by level
                game.enemy_spawn_timer = 0
                game.level.update()

                # Distribute enemies evenly over paths

                if len(paths) > 1 and not gmap.alternate_paths:
                    if game.path_id == len(paths) - 1:
                        game.path_id = 0
                    else:
                        game.path_id += 1

        # Update positions of all enemies
        for enemy in game.enemies:
            enemy.move()

            # Check if the enemy has reached the end of the path (should stop the double use of reached_end !)
            if enemy.reached_end:
                game.lives -= enemy.value  # Decrease the lives
            elif enemy.toxic_glued:
                hits = enemy.toxic_damage()
                game.process_hits(hits)
                if enemy.health <= 0 and enemy.spawn_on_die:
                    enemy.spawn_func(game.enemies)

        # May not need both conditions as reached_end is set to True when killed
        game.enemies = [enemy for enemy in game.enemies if enemy.health > 0 and not enemy.reached_end]

        # Single reorder to keep targeting first
        game.enemies.sort(key=lambda x: x.distance, reverse=True)

        # Check win condition
        if not game.enemies and game.lives > 0 and game.level.done():
            game.level_complete(pygame.display, window, window_size, lev, gmap, init_last_round_restarts, account)
            #testing remove continue - is it needed? Might finish levels clean - inc. toxic
            #toxic still dont dusappear till after the WIN has finished.
            #continue # this was in if not at max level - does it matter being done either way

        if game.lives <= 0:
            game.game_over = True
            game.current_tower_type = None
            game.failed_map(gmap, account)

        # Remove enemies that have reached the end of the path
        game.enemies = [enemy for enemy in game.enemies if not enemy.reached_end]


    # Render game state ------------------------------------------------------
    window.fill(gmap.background_color)  # Clear screen
    gmap.paint_features(window)

    tower_option_rects = nav.draw_side_panel(window, side_panel_rect, game.current_tower_type)
    options_button = nav.draw_options_cog(window)

    if alert_timer > 0:
        alert_text = font.render(alert_message, True, (255, 0, 0))  # Red color
        window.blit(alert_text, (350, 10))
        alert_timer -= 1

    # Draw the paths - try drawing before towers how does it look
    for path in paths:
        for i in range(len(path) - 1):
            pygame.draw.line(window, (path_color), path[i], path[i+1], path_thickness)

    for tower in game.towers:
        if game.active:
            hits = tower.update(game.enemies, gmap)
            if hits == -1:
                # try making the projectile a tower - but should prob be its own class.
                projectile = tower.get_projectile()
                #projectile = CannonBall(tower)
                projectiles.append(projectile)
                projectile.draw(window) # testing
                #game.towers.append(projectile)
            tower.draw(window, game.enemies)
            if hits > -1:
                game.process_hits(hits)

            #have to remove enmies etc..

            ##can do enemy here
            #if enemy.health <= 0 and enemy.spawn_on_die:
                    #enemy.spawn_func(game.enemies)

            ## May not need both conditions as reached_end is set to True when killed
            #game.enemies = [enemy for enemy in game.enemies if enemy.health > 0 and not enemy.reached_end]

        else:
            tower.draw(window, game.enemies)
        tower.highlight = False


    if game.active:
        # projecitles will be game.projecitles of course
        for projectile in projectiles:
            hits = projectile.update(game.enemies, gmap)
            game.process_hits(hits)
            #print(f"Here {projectile}")
            projectile.draw(window)

    #projectiles = [p for p in projectiles if p.active]


    if game.active:
        for enemy in game.enemies:
            if enemy.health <= 0 and enemy.spawn_on_die:
                #enemy.spawn_func(path, game.enemies)  # to do with multiple path -
                enemy.spawn_func(game.enemies)  # to do with multiple path -

        # careful of thse between tower.update and animate - could be why sometimes dont see attach
        # SH TODO  bring attack and animate together.
        # Remove dead enemies - and reached_end check for enemies spawned - who moved in spawn_func

        game.enemies = [enemy for enemy in game.enemies if enemy.health > 0 and not enemy.reached_end]

    font = pygame.font.SysFont(None, 36)

    if game.lives_highlight > 0:
        lives_text = font.render(f"Lives: {game.lives}", True, (0, 255, 0))
        game.lives_highlight -= 1
    else:
        lives_text = font.render(f"Lives: {game.lives}", True, gmap.font_color)

    window.blit(lives_text, (10, 10))

    # In your game loop, within the rendering section
    font = pygame.font.SysFont(None, 36)
    money_text = font.render(f"Money: ${int(game.player_money)}", True, gmap.font_color)
    window.blit(money_text, (10, 50))  # Adjust position as needed

    font = pygame.font.SysFont(None, 36)
    lives_text = font.render(f"Level: {game.level_num}", True, gmap.font_color)
    window.blit(lives_text, (200, 10))

    # Draw enemies
    for enemy in game.enemies:
        enemy.draw(window)

    # Draw tower attacks
    # TODO remind me why this section is separate from above where finds target - though this is just animation
    # Though I dont notice it - I should prob update enemy list inside loop to prevent double(multiple) targeting
    # Instead I check enemy is not reached_end inside for each tower targetting.
    # one thing is - drawing after enemies - so goes on top
    keep_animate = False
    if keep_animate or game.active:
        for tower in game.towers:
            if tower.viz_persist:
                tower.show_viz_persist(window)
            if tower.is_attacking and tower.target:
                tower.attack_animate(window)
        for projectile in projectiles:
            projectile.attack_animate(window)

    projectiles = [p for p in projectiles if p.active]


    if game.current_tower_type is not None:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        use_ghost_image = True
        if use_ghost_image:
            # This line ensures image has alpha channel (some do, some dont)

            #try/except lazy way for now
            try:
                current_tower_type_mod = game.current_tower_type.in_game_image.convert_alpha()
            except AttributeError:
                current_tower_type_mod = game.current_tower_type.image.convert_alpha()
            ghost_tower_image = place.create_ghost_image(current_tower_type_mod, alpha=128)
        else:
            ghost_tower_image = game.current_tower_type.image

        # Show ghost image if not in side panel (-10 just for aesthetic reasons)
        if mouse_x < (window_size[0] - side_panel_width - 10):
            ghost_tower_rect = ghost_tower_image.get_rect(center=(mouse_x, mouse_y))
            window.blit(ghost_tower_image, ghost_tower_rect.topleft)

            range_color = (255,0,0)
            if place.is_valid_position(game.current_tower_type, (mouse_x, mouse_y), paths, game.towers, options_button, gmap):
                if game.player_money >= game.current_tower_type.price:
                    range_color = (0,255,0)
                else:
                    range_color = (255, 165, 0)  # orange

            #pygame.draw.circle(window, range_color, (mouse_x, mouse_y), game.current_tower_type.range, 1)  # Range

            show_range = game.current_tower_type.range
            if game.current_tower_type.name == "Totem":
                for tower in game.towers:
                    if in_range(game.current_tower_type.range, mouse_x, mouse_y, tower):
                        if tower.__class__.name != "Totem":  # dont highlight totem here
                            tower.highlight = True
            else:
                # Make totems glow gives more info - but little pic might be nice!
                # also if adjust range need most powerful totem
                my_totem = None
                # if totem adjusts tower ranges - need to show here - maybe draw range line
                # down here rather than above
                for totem in game.totems:
                    totem.highlight = False
                    if in_range2(totem.range, mouse_x, mouse_y, totem):
                        totem.highlight = True
                        if my_totem is None or totem.level > my_totem.level:
                            #print('in range')
                            my_totem = totem
                            show_range = (game.current_tower_type.range * totem.range_boost)

            pygame.draw.circle(window, range_color, (mouse_x, mouse_y), show_range, 1)


    if not game.active and not game.shown_hint:
        hint_button = hints.generate_hint(window, game.level_num, game.inset_window)

    if game.inset_window['active']:
        update_inset_totems(game.inset_window)
    nav.draw_inset_window(window, game.inset_window, game.player_money)

    if game.game_over:  # Game over condition
        font = pygame.font.SysFont(None, 72)

        # Do we want to always bring up window - not if have last round restarts for now
        if not game.displayed_game_over and (game.map_complete or game.last_round_restarts <= 0):
            close_game_over = nav.draw_game_over_window(pygame.display, window, game.map_complete, game.aced)
        elif not game.map_complete:
            game_over_text = font.render("Game Over", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=((window_size[0] - 100) / 2, window_size[1] / 2 - 50))
            window.blit(game_over_text, text_rect)

        # TODO Buttons are not none after start - even if not drawn
        # click only looked for if game_over - you could reset button to None at that point!
        # Draw the play again button
        play_again_button, maps_button, restart_round_button = nav.play_button(
            window, window_size, game
        )
    else:
        play_again_button = None
        maps_button = None
        restart_round_button = None
        if not game.active:
            start_level_button = nav.start_level_button(window, window_size)

    pygame.display.flip()  # Update the full display Surface to the screen
    clock.tick(nav.frames_per_second)  # Maintain 60 frames per second

# Pause for a few seconds to display the game over message
#pygame.time.wait(200)

pygame.quit()
