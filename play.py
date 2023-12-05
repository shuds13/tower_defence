import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import sys
from enemy import Enemy
from tower import Tower, tower_types
import placements as place
import navigation as nav
import levels as lev
from maps import map_window
import sounds

#pygame.mixer.init()
pygame.font.init()  # Initialize font module

# Current defaults: 30 / 100 / 1

initial_lives = 30
initial_money = 100
initial_level = 1

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
    'tower': None  # The tower that is currently selected
}

def reset_game():
    global player_money, level_num, level, towers, enemies, lives, money_per_hit
    global running, enemy_spawn_timer, game_over, active, current_tower_type, inset_window
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


def reset_level():
    global enemies, running, spawned_enemies, enemy_spawn_timer, active, current_tower_type
    enemies = []
    running = True
    enemy_spawn_timer = 0
    active = False
    current_tower_type = None
    #spawned_enemies = 0

# Use gmap atributes inline but for now
def set_map(gmap):
    global pygame, map_name, path, background_color, path_thickness, path_color
    map_name = gmap.name
    path = gmap.path
    background_color = gmap.background_color
    path_thickness = gmap.path_thickness
    path_color = gmap.path_color
    pygame.display.set_caption("Tower Defense Game" + f" (Map {gmap.name})")


def select_map():
    global pygame, window, window_size, running
    gmap = map_window(pygame.display, window, window_size)
    if gmap is None:
        print('Exiting from map window')
        running = False
        return
    set_map(gmap)

play_again_button = None  # To store the button rectangle
start_level_button = None  # To store the button rectangle

alert_message = ""
alert_timer = 0
round_bonus = 20
#restart_timer = 20000

reset_game()
select_map()
options_button = nav.draw_options_cog(window)

def select_tower_type(tower_types):
    for i in range(len(tower_types)):
        if tower_option_rects[i].collidepoint(mouse_pos):
            return i
    return None

def sell_tower(mouse_pos):
    for tower in towers:
        if tower.is_clicked(mouse_pos):
            towers.remove(tower)
            return int(tower.cost * 0.8)
            break  # Exit the loop after selling one tower
    return 0

def show_tower_info(inset_window):
    for tower in towers:
        if tower.is_clicked(mouse_pos):
            inset_window['active'] = True
            inset_window['tower'] = tower
            return True
    return False

def get_money_per_hit(level_num):
    if level_num < 10:
        money_per_hit = 1.0
    elif level_num < 20:
        money_per_hit = 0.8
    elif level_num < 30:
        money_per_hit = 0.6
    else:
        money_per_hit = 0.4
    #print(f"{money_per_hit=}")
    return money_per_hit

money_per_hit = get_money_per_hit(level_num)


# Game loop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if options_button.collidepoint(mouse_pos):
                nav.draw_options_window(pygame.display, window, options_button)

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
                        mouse_pos, towers, inset_window, upgrade_button, sell_button, player_money,
                        alert_message, alert_timer, game_over
                    )

            # Place a tower
            else:
            #elif current_tower_type is not None:
                if place.is_valid_position(mouse_pos, path, towers):
                    if player_money >= current_tower_type.price:
                        towers.append(current_tower_type(position=mouse_pos))
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
        pygame.display.flip()  # Update the full display Surface to the screen
        #restart_timer -= 1
        #if restart_timer <=0:
            #running = False
        active = False
        #continue

    if active:
        # Spawn a new enemy at intervals if the max number has not been reached
        if not level.done():
            enemy_spawn_timer += 1
            if enemy_spawn_timer >= level.interval():
                #enemies.append(Enemy(path))  # Type will be determined also by level
                level.spawn_enemy(enemies, path)  # Type will be determined also by level
                enemy_spawn_timer = 0
                level.update()

        # Update positions of all enemies
        for enemy in enemies:
            enemy.move()

            # Check if the enemy has reached the end of the path
            if enemy.reached_end:
                lives -= enemy.value  # Decrease the lives

        # Check win condition
        if not enemies and lives > 0 and level.done():
            font = pygame.font.SysFont(None, 72)
            win_text = font.render("Win!", True, (0, 255, 0))  # Green color for the win text
            text_rect = win_text.get_rect(center=((window_size[0] - 100) / 2, window_size[1] / 2))
            window.blit(win_text, text_rect)
            pygame.display.flip()  # Update the full display Surface to the screen
            player_money += round_bonus

            # Pause for a few seconds to display the win message
            pygame.time.wait(2000)
            if level_num == lev.max_level:
                game_over = True
                current_tower_type = None
            else:
                level_num += 1
                money_per_hit = get_money_per_hit(level_num)
                level = lev.levels[level_num]()
                reset_level()
                continue

        if lives <= 0:
            game_over = True

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

    for tower in towers:
        tower.draw(window)
        if active:
            player_money += tower.update(enemies) * money_per_hit

    if active:
        for enemy in enemies:
            if enemy.health <= 0 and enemy.spawn_on_die:
                enemy.spawn_func(path, enemies)


        # Remove dead enemies - and reached_end check for enemies spawned - who moved in spawn_func
        enemies = [enemy for enemy in enemies if enemy.health > 0 and not enemy.reached_end]

    font = pygame.font.SysFont(None, 36)
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    window.blit(lives_text, (10, 10))

    # In your game loop, within the rendering section
    font = pygame.font.SysFont(None, 36)
    money_text = font.render(f"Money: ${int(player_money)}", True, (255, 255, 255))
    window.blit(money_text, (10, 50))  # Adjust position as needed

    font = pygame.font.SysFont(None, 36)
    lives_text = font.render(f"Level: {level_num}", True, (255, 255, 255))
    window.blit(lives_text, (200, 10))

    # Draw the path
    for i in range(len(path) - 1):
        pygame.draw.line(window, (path_color), path[i], path[i+1], path_thickness)

    # Draw enemies
    for enemy in enemies:
        enemy.draw(window)

    # Draw tower attacks
    # TODO remind me why this section is separate from above where finds target - though this is just animation
    # Though I dont notice it - I should prob update enemy list inside loop to prevent double(multiple) targeting
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
            current_tower_type_mod = current_tower_type.image.convert_alpha()
            ghost_tower_image = place.create_ghost_image(current_tower_type_mod, alpha=128)
        else:
            ghost_tower_image = current_tower_type.image

        # Show ghost image if not in side panel
        if mouse_x < 675:
            ghost_tower_rect = ghost_tower_image.get_rect(center=(mouse_x, mouse_y))
            window.blit(ghost_tower_image, ghost_tower_rect.topleft)
            pygame.draw.circle(window, (0, 255, 255), (mouse_x, mouse_y), current_tower_type.range, 1)  # Range

    nav.draw_inset_window(window, inset_window, player_money)

    if game_over:  # Game over condition
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=((window_size[0] - 100) / 2, window_size[1] / 2 - 50))
        window.blit(game_over_text, text_rect)

        # Draw the play again button
        play_again_button, maps_button = nav.play_button(window, window_size)
    else:
        if not active:
            start_level_button = nav.start_level_button(window, window_size)

    pygame.display.flip()  # Update the full display Surface to the screen
    clock.tick(60)  # Maintain 60 frames per second

#pygame.display.flip()  # Update the full display Surface to the screen

# Pause for a few seconds to display the game over message
#pygame.time.wait(200)

pygame.quit()
