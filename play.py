import pygame
import sys
from enemy import Enemy
from tower import Tower, Fighter
from placements import is_valid_position
import navigation as nav

initial_lives = 10
initial_money = 100
initial_level = 1
max_level = 2

def reset_game():
    global player_money, towers, enemies, lives, running, spawned_enemies, level
    player_money = initial_money
    level = initial_level
    towers = []
    enemies = []
    lives = initial_lives
    running = True
    spawned_enemies = 0

def reset_level():
    global enemies, running, spawned_enemies
    enemies = []
    running = True
    spawned_enemies = 0

# Initialize Pygame
pygame.init()

# Set up the display
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Tower Defense Game")

# Game variables
running = True
clock = pygame.time.Clock()

# Define a simple path as a list of (x, y) tuples
path = [(50, 100), (200, 100), (200, 300), (400, 300), (400, 500), (650, 500)]

# Enemy spawning variables
enemy_spawn_timer = 0
enemy_spawn_interval = 40  # Number of frames to wait before spawning a new enemy
enemies = []  # List to store enemies
towers = []

path_thickness = 15
max_enemies = [20, 30]


spawned_enemies = 0
tower_cost = 50

alert_message = ""
alert_timer = 0
restart_timer = 12000

game_over = False  # Add a flag to indicate game over state
play_again_button = None  # To store the button rectangle

lives = initial_lives
player_money = initial_money
level = initial_level
money_per_kill = 1
round_bonus = 20

# Game loop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if play_again_button and nav.is_click_inside_rect(pygame.mouse.get_pos(), play_again_button):
                reset_game()
                game_over = False
            else:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position and place a tower
            mouse_pos = pygame.mouse.get_pos()
            # Check if the position is valid for tower placement

            #TODO need to work out valid position.
            if is_valid_position(mouse_pos, path, towers):
                if player_money >= tower_cost:
                    #towers.append(Tower(position=mouse_pos))
                    towers.append(Fighter(position=mouse_pos))
                    player_money -= tower_cost
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
    if spawned_enemies < max_enemies[level-1]:
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_interval:
            enemies.append(Enemy(path))
            enemy_spawn_timer = 0
            spawned_enemies += 1  # Increment the counter

            if level == 1:
                if spawned_enemies >= 10:
                    enemy_spawn_interval = 15
            elif level == 2:
                if spawned_enemies >= 20:
                    enemy_spawn_interval = 8

    # Update positions of all enemies
    #print(f"{enemies=}")
    for enemy in enemies:
        enemy.move()

        ## Check if the enemy is dead (health <= 0) and reward the player
        #if enemy.health <= 0:
            #player_money += money_per_kill

        # Check if the enemy has reached the end of the path
        if enemy.reached_end:
            lives -= 1  # Decrease the lives
            #enemy = Enemy(path)  # Reset the enemy

    # Check win condition
    if not enemies and lives > 0 and spawned_enemies >= max_enemies[level-1]:
        font = pygame.font.SysFont(None, 72)
        win_text = font.render("Win!", True, (0, 255, 0))  # Green color for the win text
        text_rect = win_text.get_rect(center=(window_size[0] / 2, window_size[1] / 2))
        window.blit(win_text, text_rect)
        pygame.display.flip()  # Update the full display Surface to the screen
        player_money += round_bonus

        # Pause for a few seconds to display the win message
        pygame.time.wait(2000)
        #running = False
        if level == max_level:
            game_over = True
        else:
            level += 1
            reset_level()
            #TODO generalise this
            if level == 2:
                enemy_spawn_interval = 30
            continue

    if lives <= 0:
        #running = False  # Stop the game if the lives is 0 or less
        game_over = True

    # Remove enemies that have reached the end of the path
    enemies = [enemy for enemy in enemies if not enemy.reached_end]


    # Render game state ------------------------------------------------------
    window.fill((0, 0, 0))  # Clear screen

    font = pygame.font.SysFont(None, 36)
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    window.blit(lives_text, (10, 10))

    # In your game loop, within the rendering section
    font = pygame.font.SysFont(None, 36)
    money_text = font.render(f"Money: ${player_money}", True, (255, 255, 255))
    window.blit(money_text, (10, 50))  # Adjust position as needed

    font = pygame.font.SysFont(None, 36)
    lives_text = font.render(f"Level: {level}", True, (255, 255, 255))
    window.blit(lives_text, (200, 10))


    if alert_timer > 0:
        alert_text = font.render(alert_message, True, (255, 0, 0))  # Red color
        window.blit(alert_text, (500, 10))
        alert_timer -= 1

    for tower in towers:
        tower.update(enemies)
        rotated_image, new_rect = tower.rotate()
        window.blit(rotated_image, new_rect.topleft)

        pygame.draw.circle(window, (0, 0, 255), tower.position, 10)  # Tower
        pygame.draw.circle(window, (0, 255, 255), tower.position, tower.range, 1)  # Range

        ## Check if the enemy is dead (health <= 0) and reward the player
        for enemy in enemies:
            if enemy.health <= 0:
                player_money += money_per_kill

    enemies = [enemy for enemy in enemies if enemy.health > 0]  # Remove dead enemies

    # Draw the path
    for i in range(len(path) - 1):
        pygame.draw.line(window, (255, 255, 255), path[i], path[i+1], path_thickness)

    # Draw enemies
    for enemy in enemies:
        pygame.draw.circle(window, (255, 0, 0), (int(enemy.position[0]), int(enemy.position[1])), 10)

    # Draw tower attacks
    for tower in towers:
        if tower.is_attacking and tower.target:
            pygame.draw.line(window, (255, 0, 0), tower.position, tower.target.position, 5)

    if game_over:  # Game over condition
        #game_over = True
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(window_size[0] / 2, window_size[1] / 2 - 50))
        window.blit(game_over_text, text_rect)

        # Draw the play again button
        play_again_button = nav.play_button(window, window_size)

    pygame.display.flip()  # Update the full display Surface to the screen
    clock.tick(60)  # Maintain 60 frames per second

pygame.display.flip()  # Update the full display Surface to the screen

# Pause for a few seconds to display the game over message
#pygame.time.wait(200)

pygame.quit()
