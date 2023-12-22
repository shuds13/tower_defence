import os
import copy
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import sys
from enemy import Enemy
from tower import Tower, tower_types, Totem
import placements as place
import navigation as nav
import levels as lev
from maps import map_window
import sounds
import hints

#pygame.mixer.init()
pygame.font.init()  # Initialize font module

# Current defaults: 30 / 100 / 1


# IMPORTANT need to remember to update money_per_hit - < round 40 etc as it will affect difficulty of rounds which
# i'm trying to get right - i'll have to get it right all over again!
initial_lives = 30
initial_money = 150
initial_level = 1


init_last_round_restarts = 3
#init_last_round_restarts = 20

restart_testing = False


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

# navigation
inset_window = {
    'active': False,
    'x': 4,  # X position of the window
    'y': window_size[1] - 304,  # Y position of the window
    'width': 200,
    'height': 300,
    'tower': None,
    'totem': None
}

def reset_game():
    global player_money, level_num, level, towers, enemies, lives, money_per_hit
    global running, enemy_spawn_timer, game_over, active, current_tower_type, inset_window
    global start_round_money, start_round_lives, start_round_towers, last_round_restarts, path_id
    global total_hits, total_money, start_round_total_hits, start_round_total_money #, start_round_totems
    global lives_highlight, totems
    player_money = initial_money
    level_num = initial_level
    level = lev.levels[level_num]()
    towers = []
    enemies = []
    lives = initial_lives
    running = True
    enemy_spawn_timer = 0
    game_over = False
    active = False
    current_tower_type = None
    inset_window['active'] = False
    money_per_hit = 1.0
    # should be obj
    start_round_money = initial_money
    start_round_lives = initial_lives
    start_round_towers = []
    #start_round_totems = []
    last_round_restarts = init_last_round_restarts
    path_id = 0
    #more should be player obj attributes - for stats
    total_hits = 0
    total_money = 0
    start_round_total_hits = 0
    start_round_total_money = initial_money
    lives_highlight = 0
    totems = []

def reset_level():
    global enemies, running, spawned_enemies, enemy_spawn_timer, active, current_tower_type, path_id
    enemies = []
    running = True
    enemy_spawn_timer = 0
    active = False
    path_id = 0
    #current_tower_type = None
    #spawned_enemies = 0


def restart_round():
    global player_money, lives, towers, totems
    global start_round_money, start_round_lives, start_round_towers, last_round_restarts, game_over
    global level_num, level, lev
    global total_hits, total_money
    global lives_highlight
    #global start_round_totems

    player_money = start_round_money
    lives = start_round_lives

    # Will be in stats option in options window.
    #print(f"B4 Restart level: {total_hits=}")
    #print(f"B4 Restart level: {total_money=:.2f}")

    total_hits = start_round_total_hits
    total_money = start_round_total_money

    # Will be in stats option in options window.
    #print(f"Restart level: {total_hits=}")
    #print(f"Restart level: {total_money=:.2f}")

    # dont work - says TypeError: cannot pickle 'pygame.surface.Surface' object
    #towers = copy.deepcopy(start_round_towers)
    towers = []
    totems = []
    for tower in start_round_towers:
        ctower = copy.copy(tower)
        towers.append(ctower)
        if isinstance(ctower, Totem):
            totems.append(ctower)
    #for totem in start_round_totems:
        #totems.append(copy.copy(totem))
    #for tower in towers:
        #tower.get_start_hits()
    last_round_restarts -= 1
    game_over = False
    level = lev.levels[level_num]()  # reset this level (phase num / num_spawned)
    lives_highlight = 0


def in_range(my_range, mouse_x, mouse_y, obj):
    distance = ((mouse_x - obj.position[0])**2 + (mouse_y - obj.position[1])**2)**0.5
    return distance <= my_range

def in_range2(my_range, mouse_x, mouse_y, obj):
    distance = ((obj.position[0] - mouse_x)**2 + (obj.position[1] - mouse_y)**2)**0.5
    return distance <= my_range

# Use gmap atributes inline but for now
def set_map(gmap):
    global pygame, map_name, paths, background_color, path_thickness, path_color
    map_name = gmap.name
    paths = gmap.paths
    background_color = gmap.background_color
    path_thickness = gmap.path_thickness
    path_color = gmap.path_color
    pygame.display.set_caption("Tower Defense Game" + f" ({gmap.name})")


def select_map():
    global pygame, window, window_size, running
    gmap = map_window(pygame.display, window, window_size)
    if gmap is None:
        #print('Exiting from map window')
        running = False
        return
    set_map(gmap)

play_again_button = None  # To store the button rectangle
start_level_button = None  # To store the button rectangle
restart_round_button = None

alert_message = ""
alert_timer = 0
round_bonus = 20
highlight_time = 20
#restart_timer = 20000

reset_game()
select_map()
options_button = nav.draw_options_cog(window)

def select_tower_type(tower_types):
    for i in range(len(tower_types)):
        if tower_option_rects[i].collidepoint(mouse_pos):
            return i
    return None

#def sell_tower(mouse_pos):
    #for tower in towers:
        #if tower.is_clicked(mouse_pos):
            #cost = int(tower.cost * 0.8)
            #towers.remove(tower)
            ##del tower
            #return cost
            ##break  # Exit the loop after selling one tower
    #return 0

def update_inset_totems(inset_window):
    my_totem = None
    tower = inset_window['tower']
    inset_window['totem'] = None
    if tower.__class__.name != "Totem":
        for totem in totems:
            if totem.tower_in_range(tower):
                if my_totem is None or totem.level > my_totem.level:
                    my_totem = totem
        inset_window['totem'] = my_totem

def show_tower_info(inset_window):
    for tower in towers:
        if tower.is_clicked(mouse_pos):
            inset_window['active'] = True
            inset_window['tower'] = tower
            update_inset_totems(inset_window)
            return True
    return False

# If keep tower prices as is need to reduce more.
# proper version should increase tower price though
def get_money_per_hit(level_num):
    if level_num < 10:
        money_per_hit = 1.0
    elif level_num < 20:
        money_per_hit = 0.7 # 0.8
    elif level_num < 30:
        money_per_hit = 0.5 # 0.6
    elif level_num < 40:
        #money_per_hit = 0.3 # 0.6  #testing
        money_per_hit = 0.4 # 0.6
    elif level_num < 50:
        money_per_hit = 0.3 # 0.6
    else:
        money_per_hit = 0.2 # 0.4
    #print(f"{money_per_hit=}")
    return money_per_hit

money_per_hit = get_money_per_hit(level_num)

#hints.generate_hint(window, level_num)

# Game loop
while running:

    #if restart_testing:
        #play_again_button, maps_button, restart_round_button = nav.play_button(
            #window, window_size, last_round_restarts
        #)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if options_button.collidepoint(mouse_pos):
                nav.draw_options_window(pygame.display, window, options_button)

            if game_over or restart_testing:

                #play_again_button, maps_button, restart_round_button = nav.play_button(
                    #window, window_size, last_round_restarts
                #)

                if restart_round_button and nav.is_click_inside_rect(mouse_pos, restart_round_button):
                    restart_round()
                    reset_level()

            if game_over:
                if play_again_button and nav.is_click_inside_rect(mouse_pos, play_again_button):
                    reset_game()
                if maps_button and nav.is_click_inside_rect(mouse_pos, maps_button):
                    reset_game()
                    select_map()
                    continue
            else:
                # If GO button is clicked then start level
                if not active and start_level_button:
                    if nav.is_click_inside_rect(mouse_pos, start_level_button):
                        active = True
                        start_level_button = None
                        continue

                # Is cross clicked to deselect a tower
                if tower_option_rects[-1].collidepoint(mouse_pos):
                    current_tower_type = None
                    continue

                # Select a tower
                new_type = select_tower_type(tower_types)
                if new_type is not None:
                    current_tower_type = tower_types[new_type]
                    continue

            if current_tower_type is None:

                # If user clicked on tower - open the info (inset) window
                if show_tower_info(inset_window):
                    upgrade_button, sell_button = nav.draw_inset_window(window, inset_window, player_money)

                # Process clicks in the info window
                elif inset_window['active']:
                    # should use object for inset window parameters
                    player_money, alert_message, alert_timer = nav.process_inset_window(
                        mouse_pos, towers, totems, inset_window, upgrade_button, sell_button, player_money,
                        alert_message, alert_timer, game_over
                    )

            # Place a tower
            else:
            #elif current_tower_type is not None:
                if place.is_valid_position(current_tower_type, mouse_pos, paths, towers):
                    if player_money >= current_tower_type.price:
                        newtower = current_tower_type(position=mouse_pos)
                        towers.append(newtower)
                        if isinstance(newtower, Totem):
                            totems.append(newtower)
                        #snd_place.play()
                        sounds.play('place')
                        player_money -= current_tower_type.price
                        # I did not used to do this - is it better
                        current_tower_type = None  # This deselects tower when put down
                    else:
                        alert_message = "Not enough money!"
                        alert_timer = 120  # Display message for 2 seconds (assuming 60 FPS)
                else:
                    alert_message = "Cant place here"
                    alert_timer = 120  # Display message for 2 seconds (assuming 60 FPS)

    #  prevent flash of level when close from map screen - is this okay here
    if not running:
        break

    if game_over:
        #if active:  # so shows once
            #print(f"{total_hits=}")  # testing - will put somewhere sensible - maybe in options.
        pygame.display.flip()  # Update the full display Surface to the screen
        #restart_timer -= 1
        #if restart_timer <=0:
            #running = False
        active = False
        #continue

    # If not too slow - work this out every time then okay with buying selling etc...
    for tower in towers:
        tower.speed_mod = 1
        tower.range_mod = 1
        tower.see_ghosts = tower.__class__.see_ghosts
        #print(f"Tower: {tower} {tower.__class__.see_ghosts} {tower.see_ghosts}")

    for totem in totems:
        for tower in towers:
            if totem.tower_in_range(tower):
                totem.boost(tower)

    if active:
        # Spawn a new enemy at intervals if the max number has not been reached
        if not level.done():
            enemy_spawn_timer += 1
            if enemy_spawn_timer >= level.interval():

                #path = paths[0]
                path = paths[path_id]
                #enemies.append(Enemy(path))  # Type will be determined also by level
                level.spawn_enemy(enemies, path)  # Type will be determined also by level
                enemy_spawn_timer = 0
                level.update()

                if len(paths) > 1:
                    if path_id == len(paths) - 1:
                        path_id = 0
                    else:
                        path_id += 1

        # Update positions of all enemies
        for enemy in enemies:
            enemy.move()

            # Check if the enemy has reached the end of the path
            if enemy.reached_end:
                lives -= enemy.value  # Decrease the lives
            elif enemy.toxic_glued:
                #print('hhhhhhhhhhhhhhhhhhere')
                hits = enemy.toxic_damage()
                total_hits += hits
                player_money += hits * money_per_hit
                total_money += hits * money_per_hit
                if enemy.health <= 0 and enemy.spawn_on_die:
                    #enemy.spawn_func(path, enemies)  # to do with multiple path -
                    enemy.spawn_func(enemies)  # to do with multiple path -

        enemies = [enemy for enemy in enemies if enemy.health > 0 and not enemy.reached_end]


        # Check win condition
        if not enemies and lives > 0 and level.done():
            font = pygame.font.SysFont(None, 72)
            win_text = font.render("Win!", True, (0, 255, 0))  # Green color for the win text
            text_rect = win_text.get_rect(center=((window_size[0] - 100) / 2, window_size[1] / 2))
            window.blit(win_text, text_rect)
            pygame.display.flip()  # Update the full display Surface to the screen
            player_money += round_bonus
            if level_num % 10 == 0:
                lives += 10
                lives_highlight = highlight_time

            # Pause for a few seconds to display the win message
            #print(f"{total_hits=}")  # testing - will put somewhere sensible - maybe in options.
            pygame.time.wait(1000)
            if level_num == lev.max_level:
                game_over = True
                current_tower_type = None
            else:
                start_round_money = player_money
                start_round_lives = lives
                start_round_total_hits = total_hits
                start_round_total_money = total_money
                #start_round_towers = towers
                #for tower in towers:
                    #tower.set_start_hits()  # not enough - reset all attributes of tower

                # dont work - says TypeError: cannot pickle 'pygame.surface.Surface' object
                # though surface appears in tower function - I dont see it stored in attribute
                #start_round_towers = copy.deepcopy(towers)
                start_round_towers = []
                for tower in towers:
                    start_round_towers.append(copy.copy(tower))
                #start_round_totems = []
                #for totem in totems:
                    #start_round_totems.append(copy.copy(totem))
                #print(f"{start_round_totems}")

                level_num += 1
                money_per_hit = get_money_per_hit(level_num)
                level = lev.levels[level_num]()
                reset_level()
                # Will be in stats option in options window.
                #print(f"{total_hits=}")
                print(f"Before level {level_num} {total_money=:.2f}")
                continue

        if lives <= 0:
            game_over = True

            # Will be in stats option in options window.
            #print(f"{total_hits=}")
            #print(f"{total_money=}")

        # Remove enemies that have reached the end of the path
        enemies = [enemy for enemy in enemies if not enemy.reached_end]


    # Render game state ------------------------------------------------------
    window.fill(background_color)  # Clear screen

    tower_option_rects = nav.draw_side_panel(window, side_panel_rect, current_tower_type)
    #tower_option_rects = draw_side_panel(window, side_panel_rect, tower_img_1)

    options_button = nav.draw_options_cog(window)

    if alert_timer > 0:
        alert_text = font.render(alert_message, True, (255, 0, 0))  # Red color
        window.blit(alert_text, (350, 10))
        alert_timer -= 1


    # Draw the paths - try drawing before towers how does it look
    for path in paths:
        for i in range(len(path) - 1):
            pygame.draw.line(window, (path_color), path[i], path[i+1], path_thickness)


    for tower in towers:
        tower.draw(window, enemies)  # test replacing this with commented lines (dedicated commit) - I think corrects funny angle - but does it 'wobble' more
        if active:
            hits = tower.update(enemies)
            #tower.draw(window, enemies)
            total_hits += hits
            #player_money += tower.update(enemies) * money_per_hit
            player_money += hits * money_per_hit
            total_money += hits * money_per_hit
        #else:
            #tower.draw(window, enemies)
        tower.highlight = False

    if active:
        for enemy in enemies:
            if enemy.health <= 0 and enemy.spawn_on_die:
                #enemy.spawn_func(path, enemies)  # to do with multiple path -
                enemy.spawn_func(enemies)  # to do with multiple path -

        # careful of thse between tower.update and animate - could be why sometimes dont see attach
        # SH TODO  bring attack and animate together.
        # Remove dead enemies - and reached_end check for enemies spawned - who moved in spawn_func

        ##testing
        #pr = False
        #for en in enemies:
            #if en.reached_end:
                #pr = True
                #break

        #if pr:
            #print(f"b4: {len(enemies)}  {enemies}", flush=True)

        enemies = [enemy for enemy in enemies if enemy.health > 0 and not enemy.reached_end]

        #if pr:
            #print(f"aft {len(enemies)} {enemies}", flush=True)

        #print(len(enemies))

    font = pygame.font.SysFont(None, 36)

    if lives_highlight > 0:
        lives_text = font.render(f"Lives: {lives}", True, (0, 255, 0))
        lives_highlight -= 1
    else:
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))

    window.blit(lives_text, (10, 10))

    # In your game loop, within the rendering section
    font = pygame.font.SysFont(None, 36)
    money_text = font.render(f"Money: ${int(player_money)}", True, (255, 255, 255))
    window.blit(money_text, (10, 50))  # Adjust position as needed

    font = pygame.font.SysFont(None, 36)
    lives_text = font.render(f"Level: {level_num}", True, (255, 255, 255))
    window.blit(lives_text, (200, 10))

    ## Draw the paths
    #for path in paths:
        #for i in range(len(path) - 1):
            #pygame.draw.line(window, (path_color), path[i], path[i+1], path_thickness)

    # Draw enemies
    for enemy in enemies:
        enemy.draw(window)

    # Draw tower attacks
    # TODO remind me why this section is separate from above where finds target - though this is just animation
    # Though I dont notice it - I should prob update enemy list inside loop to prevent double(multiple) targeting
    keep_animate = False
    if keep_animate or active:
        for tower in towers:
            if tower.viz_persist:
                tower.show_viz_persist(window)
            if tower.is_attacking and tower.target:
                tower.attack_animate(window)

    if current_tower_type is not None:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        use_ghost_image = True
        if use_ghost_image:
            # This line ensures image has alpha channel (some do, some dont)

            #try/except lazy way for now
            try:
                current_tower_type_mod = current_tower_type.in_game_image.convert_alpha()
            except AttributeError:
                current_tower_type_mod = current_tower_type.image.convert_alpha()
            ghost_tower_image = place.create_ghost_image(current_tower_type_mod, alpha=128)
        else:
            ghost_tower_image = current_tower_type.image

        # Show ghost image if not in side panel

        if mouse_x < 675:
            ghost_tower_rect = ghost_tower_image.get_rect(center=(mouse_x, mouse_y))
            window.blit(ghost_tower_image, ghost_tower_rect.topleft)

            range_color = (255,0,0)
            if place.is_valid_position(current_tower_type, (mouse_x, mouse_y), paths, towers):
                if player_money >= current_tower_type.price:
                    range_color = (0,255,0)
                else:
                    range_color = (255, 165, 0)  # orange

            #pygame.draw.circle(window, range_color, (mouse_x, mouse_y), current_tower_type.range, 1)  # Range

            show_range = current_tower_type.range
            if current_tower_type.name == "Totem":
                for tower in towers:
                    if in_range(current_tower_type.range, mouse_x, mouse_y, tower):
                        if tower.__class__.name != "Totem":  # dont highlight totem here
                            tower.highlight = True
            else:
                # Make totems glow gives more info - but little pic might be nice!
                # also if adjust range need most powerful totem
                my_totem = None
                # if totem adjusts tower ranges - need to show here - maybe draw range line
                # down here rather than above
                for totem in totems:
                    totem.highlight = False
                    if in_range2(totem.range, mouse_x, mouse_y, totem):
                        totem.highlight = True
                        if my_totem is None or totem.level > my_totem.level:
                            #print('in range')
                            my_totem = totem
                            show_range = (current_tower_type.range * totem.range_boost)

            pygame.draw.circle(window, range_color, (mouse_x, mouse_y), show_range, 1)


    if not active:
        hints.generate_hint(window, level_num)

    if inset_window['active']:
        update_inset_totems(inset_window)
    nav.draw_inset_window(window, inset_window, player_money)

    if game_over:  # Game over condition
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=((window_size[0] - 100) / 2, window_size[1] / 2 - 50))
        window.blit(game_over_text, text_rect)


        # TODO thinking about this right now - buttons are not none after start - even if not drawn - can you click!!!!
        # oh but click only looked for if game_over!!!!! - you could reset button to None at that point!!!
        # Draw the play again button
        play_again_button, maps_button, restart_round_button = nav.play_button(
            window, window_size, last_round_restarts
        )
    else:
        if not active:
            start_level_button = nav.start_level_button(window, window_size)

    pygame.display.flip()  # Update the full display Surface to the screen
    clock.tick(nav.frames_per_second)  # Maintain 60 frames per second

#pygame.display.flip()  # Update the full display Surface to the screen

# Pause for a few seconds to display the game over message
#pygame.time.wait(200)

pygame.quit()
