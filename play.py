import pygame
import sys
from enemy import Enemy
from tower import Tower


initial_lives = 10
initial_money = 100


def is_valid_position(pos):
    # Check if the position is not on the path and not too close to other towers
    # This is a simple example; you'll need to replace it with your game's logic
    for point in path:
        if (pos[0] - point[0])**2 + (pos[1] - point[1])**2 < some_minimum_distance**2:
            return False
    for tower in towers:
        if (pos[0] - tower.position[0])**2 + (pos[1] - tower.position[1])**2 < some_minimum_distance_between_towers**2:
            return False
    return True

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

def reset_game():
    global player_money, towers, enemies, lives, running, spawned_enemies
    player_money = initial_money
    towers = []
    enemies = []
    lives = initial_lives
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

max_enemies = 20
spawned_enemies = 0
tower_cost = 50

alert_message = ""
alert_timer = 0
restart_timer = 12000

game_over = False  # Add a flag to indicate game over state
play_again_button = None  # To store the button rectangle

lives = initial_lives
player_money = initial_money


# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if play_again_button and is_click_inside_rect(pygame.mouse.get_pos(), play_again_button):
                reset_game()
                game_over = False
            else:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position and place a tower
            mouse_pos = pygame.mouse.get_pos()
            # Check if the position is valid for tower placement

            #TODO need to work out valid position.
            #if is_valid_position(mouse_pos) and player_money >= tower_cost:
            if player_money >= tower_cost:
                towers.append(Tower(position=mouse_pos, range=100, attack_speed=40))
                player_money -= tower_cost
            else:
                alert_message = "Not enough money!"
                alert_timer = 120  # Display message for 2 seconds (assuming 60 FPS)

    if game_over:
        pygame.display.flip()  # Update the full display Surface to the screen
        restart_timer -= 1
        if restart_timer <=0:
            running = False
        continue

    # Spawn a new enemy at intervals if the max number has not been reached
    if spawned_enemies < max_enemies:
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_interval:
            enemies.append(Enemy(path))
            enemy_spawn_timer = 0
            spawned_enemies += 1  # Increment the counter

            if spawned_enemies >= 10:
                enemy_spawn_interval = 15

    # Update positions of all enemies
    for enemy in enemies:
        enemy.move()

        # Check if the enemy has reached the end of the path
        if enemy.reached_end:
            lives -= 1  # Decrease the lives
            #enemy = Enemy(path)  # Reset the enemy

    # Check win condition
    if not enemies and lives > 0 and spawned_enemies >= max_enemies:
        font = pygame.font.SysFont(None, 72)
        win_text = font.render("Win!", True, (0, 255, 0))  # Green color for the win text
        text_rect = win_text.get_rect(center=(window_size[0] / 2, window_size[1] / 2))
        window.blit(win_text, text_rect)
        pygame.display.flip()  # Update the full display Surface to the screen

        # Pause for a few seconds to display the win message
        pygame.time.wait(2000)
        #running = False
        game_over = True

    if lives <= 0:
        #running = False  # Stop the game if the lives is 0 or less
        game_over = True

    # Remove enemies that have reached the end of the path
    enemies = [enemy for enemy in enemies if not enemy.reached_end]


    # Render game state ------------------------------------------------------
    window.fill((0, 0, 0))  # Clear screen

    # Draw the lives
    font = pygame.font.SysFont(None, 36)
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    window.blit(lives_text, (10, 10))

    # In your game loop, within the rendering section
    font = pygame.font.SysFont(None, 36)
    money_text = font.render(f"Money: ${player_money}", True, (255, 255, 255))
    window.blit(money_text, (10, 50))  # Adjust position as needed

    if alert_timer > 0:
        alert_text = font.render(alert_message, True, (255, 0, 0))  # Red color
        window.blit(alert_text, (200, 10))
        alert_timer -= 1


    for tower in towers:
        tower.update(enemies)
        # Draw the tower and its range
        pygame.draw.circle(window, (0, 0, 255), tower.position, 10)  # Tower
        pygame.draw.circle(window, (0, 255, 255), tower.position, tower.range, 1)  # Range

    enemies = [enemy for enemy in enemies if enemy.health > 0]  # Remove dead enemies

    # Draw the path
    for i in range(len(path) - 1):
        pygame.draw.line(window, (255, 255, 255), path[i], path[i+1], 2)

    # Draw enemies
    for enemy in enemies:
        pygame.draw.circle(window, (255, 0, 0), (int(enemy.position[0]), int(enemy.position[1])), 10)

    # Draw tower attacks
    for tower in towers:
        if tower.is_attacking and tower.target:
            pygame.draw.line(window, (255, 0, 0), tower.position, tower.target.position, 2)

    if game_over:  # Game over condition
        #game_over = True
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(window_size[0] / 2, window_size[1] / 2 - 50))
        window.blit(game_over_text, text_rect)

        # Draw the play again button
        play_again_button = draw_button(window, "Play Again", (window_size[0] / 2 - 100, window_size[1] / 2 + 50), (200, 50))

    pygame.display.flip()  # Update the full display Surface to the screen
    clock.tick(60)  # Maintain 60 frames per second

pygame.display.flip()  # Update the full display Surface to the screen

# Pause for a few seconds to display the game over message
#pygame.time.wait(200)

pygame.quit()
