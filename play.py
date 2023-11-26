import pygame
import sys
from enemy import Enemy
from tower import Tower, Fighter, Burger
from placements import is_valid_position
import navigation as nav
import levels as lev

initial_lives = 10
initial_money = 100
initial_level = 1

def reset_game():
    global player_money, level_num, level, towers, enemies, lives, running, enemy_spawn_timer, game_over
    player_money = initial_money
    level_num = initial_level
    level = lev.levels[level_num]()
    towers = []
    enemies = []
    lives = initial_lives
    running = True
    enemy_spawn_timer = 0
    game_over = False
    #spawned_enemies = 0
    #enemy_spawn_interval = 40

def reset_level():
    global enemies, running, spawned_enemies, enemy_spawn_timer
    enemies = []
    running = True
    enemy_spawn_timer = 0
    #spawned_enemies = 0

# Initialize Pygame
pygame.init()

# Set up the display
window_size = (900, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Tower Defense Game")
clock = pygame.time.Clock()

# Define a simple path as a list of (x, y) tuples - will be under map.py
path = [(50, 100), (200, 100), (200, 300), (400, 300), (400, 500), (650, 500)]
path_thickness = 15

current_tower_type = Fighter  # Will be selected
alert_message = ""
alert_timer = 0
restart_timer = 12000
play_again_button = None  # To store the button rectangle
#money_per_kill = 1
round_bonus = 20

reset_game()

side_panel_width = 200
side_panel_height = window_size[1]  # same as the game window height
side_panel_rect = pygame.Rect(window_size[0] - side_panel_width, 0, side_panel_width, side_panel_height)


# tmp here - in tower
tower_image = pygame.image.load('tower1.png')  # Load your tower image
tower_image = pygame.transform.scale(tower_image, (50, 50))
tower_image2 = pygame.image.load('burger.png')  # Load your tower image
tower_image2 = pygame.transform.scale(tower_image2, (50, 50))


# tmp here - put in placements or navigation
def draw_side_panel(surface, panel_rect):
    # Draw the background of the side panel
    pygame.draw.rect(surface, (200, 200, 200), panel_rect)  # Light grey background
    font = pygame.font.SysFont(None, 24)

    # Draw tower selection options (simple rectangles or icons)
    tower_option_rect_1 = pygame.Rect(panel_rect.x + 10, panel_rect.y + 10, 180, 50)  # Example
    pygame.draw.rect(surface, (100, 100, 100), tower_option_rect_1)  # Dark grey option box

    image_rect_1 = tower_image.get_rect(center=(tower_option_rect_1.centerx - 40, tower_option_rect_1.centery))
    surface.blit(tower_image, image_rect_1.topleft)
    #price_text_1 = font.render(f"${tower_type_prices['Type1']}", True, (0, 0, 0))
    price_text_1 = font.render(f"${Fighter.price}", True, (0, 0, 0))
    surface.blit(price_text_1, (image_rect_1.right + 5, tower_option_rect_1.centery - 10))

    if current_tower_type.name == "Fighter":
        pygame.draw.rect(surface, (255, 255, 0), tower_option_rect_1, 3)  # Yellow border


    # Add more tower options as needed...
    # Draw the tower image on this rectangle
    #image_rect = tower_image.get_rect(center=tower_option_rect_1.center)
    #surface.blit(tower_image, image_rect.topleft)

    tower_option_rect_2 = pygame.Rect(panel_rect.x +10, panel_rect.y + 70, 180, 50)  # Adjust position
    pygame.draw.rect(surface, (100, 100, 100), tower_option_rect_2)

    #image_rect_2 = tower_image2.get_rect(center=tower_option_rect_2.center)
    #surface.blit(tower_image2, image_rect_2.topleft)


    image_rect_2 = tower_image2.get_rect(center=(tower_option_rect_2.centerx - 40, tower_option_rect_2.centery))
    surface.blit(tower_image2, image_rect_2.topleft)
    price_text_2 = font.render(f"${Burger.price}", True, (0, 0, 0))
    surface.blit(price_text_2, (image_rect_2.right + 5, tower_option_rect_2.centery - 10))
    if current_tower_type.name == "Burger":
        pygame.draw.rect(surface, (255, 255, 0), tower_option_rect_2, 3)  # Yellow border


    return [tower_option_rect_1, tower_option_rect_2] # Return a list of rects representing tower options


# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if play_again_button and nav.is_click_inside_rect(pygame.mouse.get_pos(), play_again_button):
                reset_game()
                #game_over = False
            else:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position and place a tower
            mouse_pos = pygame.mouse.get_pos()
            if tower_option_rects[0].collidepoint(mouse_pos):
                current_tower_type = Fighter
            elif tower_option_rects[1].collidepoint(mouse_pos):
                current_tower_type = Burger            #for rect in tower_option_rects:
                #if rect.collidepoint(mouse_pos):
                    #print(f"{rect=} {type(rect)=}")
                    #current_tower_type = 'tower_type_here'  # Assign the selected tower type
                    #break
            # Check if the position is valid for tower placement
            elif is_valid_position(mouse_pos, path, towers):
                if player_money >= current_tower_type.price:
                    #towers.append(Tower(position=mouse_pos))
                    towers.append(current_tower_type(position=mouse_pos))
                    player_money -= current_tower_type.price
                else:
                    alert_message = "Not enough money!"
                    alert_timer = 120  # Display message for 2 seconds (assuming 60 FPS)
            else:
                alert_message = "Cant place here"
                alert_timer = 120  # Display message for 2 seconds (assuming 60 FPS)


    if game_over:
        pygame.display.flip()  # Update the full display Surface to the screen
        restart_timer -= 1
        if restart_timer <=0:
            running = False
        continue

    # Spawn a new enemy at intervals if the max number has not been reached
    if not level.done():
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= level.interval():
            enemies.append(Enemy(path))  # Type will be determined also by level
            enemy_spawn_timer = 0
            level.update()

    # Update positions of all enemies
    for enemy in enemies:
        enemy.move()

        # Check if the enemy has reached the end of the path
        if enemy.reached_end:
            lives -= 1  # Decrease the lives

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
            print(f"{lev.max_level=} {level_num=}")
            game_over = True
        else:
            level_num += 1
            level = lev.levels[level_num]()
            print(f"{level.level_id=}")
            reset_level()
            continue

    if lives <= 0:
        #running = False  # Stop the game if the lives is 0 or less
        game_over = True

    # Remove enemies that have reached the end of the path
    enemies = [enemy for enemy in enemies if not enemy.reached_end]


    # Render game state ------------------------------------------------------
    #window.fill((0, 0, 0))  # Clear screen
    window.fill((50, 25, 0))  # Clear screen

    tower_option_rects = draw_side_panel(window, side_panel_rect)
    #tower_option_rects = draw_side_panel(window, side_panel_rect, tower_image)

    if alert_timer > 0:
        alert_text = font.render(alert_message, True, (255, 0, 0))  # Red color
        window.blit(alert_text, (500, 10))
        alert_timer -= 1

    for tower in towers:
        rotated_image, new_rect = tower.rotate()
        window.blit(rotated_image, new_rect.topleft)
        player_money += tower.update(enemies)

        pygame.draw.circle(window, (0, 0, 255), tower.position, 10)  # Tower
        pygame.draw.circle(window, (0, 255, 255), tower.position, tower.range, 1)  # Range

    enemies = [enemy for enemy in enemies if enemy.health > 0]  # Remove dead enemies

    font = pygame.font.SysFont(None, 36)
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    window.blit(lives_text, (10, 10))

    # In your game loop, within the rendering section
    font = pygame.font.SysFont(None, 36)
    money_text = font.render(f"Money: ${player_money}", True, (255, 255, 255))
    window.blit(money_text, (10, 50))  # Adjust position as needed

    font = pygame.font.SysFont(None, 36)
    lives_text = font.render(f"Level: {level_num}", True, (255, 255, 255))
    window.blit(lives_text, (200, 10))

    # Draw the path
    for i in range(len(path) - 1):
        pygame.draw.line(window, (255, 255, 255), path[i], path[i+1], path_thickness)

    # Draw enemies
    for enemy in enemies:
        pygame.draw.circle(window, (255, 0, 0), (int(enemy.position[0]), int(enemy.position[1])), 10)

    # Draw tower attacks
    for tower in towers:
        if tower.is_attacking and tower.target:
            pygame.draw.line(window, (255, 0, 0), tower.position, tower.target.position, 5)  # should be in tower

    if game_over:  # Game over condition
        #game_over = True
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=((window_size[0] - 100) / 2, window_size[1] / 2 - 50))
        window.blit(game_over_text, text_rect)

        # Draw the play again button
        play_again_button = nav.play_button(window, window_size)

    pygame.display.flip()  # Update the full display Surface to the screen
    clock.tick(60)  # Maintain 60 frames per second

pygame.display.flip()  # Update the full display Surface to the screen

# Pause for a few seconds to display the game over message
#pygame.time.wait(200)

pygame.quit()
