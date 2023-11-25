import pygame
import sys
from enemy import Enemy
from tower import Tower


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


# Initialize Pygame
pygame.init()

lives = 10  # Initial lives

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

#standard
enemy_spawn_interval = 50  # Number of frames to wait before spawning a new enemy

#testing
#enemy_spawn_interval = 10  # Number of frames to wait before spawning a new enemy

enemies = []  # List to store enemies

# Create an enemy
#enemy = Enemy(path)

#pygame.draw.line(window, (0, 255, 0), path[i], path[i+1], 5)

# Define a tower
#tower = Tower(position=(400, 300), range=100, attack_speed=60)  # Example values
#tower = Tower(position=(360, 340), range=100, attack_speed=60)  # Example values
#tower = Tower(position=(360, 340), range=100, attack_speed=20)  # Example values

towers = []

max_enemies = 20
spawned_enemies = 0

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position and place a tower
            mouse_pos = pygame.mouse.get_pos()
            # Check if the position is valid for tower placement
            #if is_valid_position(mouse_pos):
                #towers.append(Tower(position=mouse_pos, range=100, attack_speed=40))
            towers.append(Tower(position=mouse_pos, range=100, attack_speed=40))

    # Spawn a new enemy at intervals if the max number has not been reached
    if spawned_enemies < max_enemies:
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_interval:
            enemies.append(Enemy(path))
            enemy_spawn_timer = 0
            spawned_enemies += 1  # Increment the counter

            if spawned_enemies >= 5:
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
        pygame.time.wait(3000)
        running = False

    if lives <= 0:
        running = False  # Stop the game if the lives is 0 or less

    # Remove enemies that have reached the end of the path
    enemies = [enemy for enemy in enemies if not enemy.reached_end]


    # Render game state
    window.fill((0, 0, 0))  # Clear screen

    for tower in towers:
        tower.update(enemies)
        # Draw the tower and its range
        pygame.draw.circle(window, (0, 0, 255), tower.position, 10)  # Tower
        pygame.draw.circle(window, (0, 255, 255), tower.position, tower.range, 1)  # Range

    enemies = [enemy for enemy in enemies if enemy.health > 0]  # Remove dead enemies


    ## Update and draw the tower
    #tower.update(enemies)
    #enemies = [enemy for enemy in enemies if enemy.health > 0]  # Remove dead enemies

    ## Draw the tower (as a simple circle for now)
    #pygame.draw.circle(window, (0, 0, 255), tower.position, 10)  # Blue color for the tower

    ## Optional: Draw the tower's range
    #pygame.draw.circle(window, (0, 255, 255), tower.position, tower.range, 1)  # Cyan color for the range



    # Draw the path
    for i in range(len(path) - 1):
        pygame.draw.line(window, (255, 255, 255), path[i], path[i+1], 2)

    #import pdb;pdb.set_trace()
    ## Draw the enemy if it hasn't reached the end
    #if not enemy.reached_end:
        #pygame.draw.circle(window, (255, 0, 0), (int(enemy.position[0]), int(enemy.position[1])), 10)

    # Draw enemies
    for enemy in enemies:
        pygame.draw.circle(window, (255, 0, 0), (int(enemy.position[0]), int(enemy.position[1])), 10)


    # Draw tower attacks
    for tower in towers:
        if tower.is_attacking and tower.target:
            pygame.draw.line(window, (255, 0, 0), tower.position, tower.target.position, 2)


    # Draw the lives
    font = pygame.font.SysFont(None, 36)
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    window.blit(lives_text, (10, 10))

    pygame.display.flip()  # Update the full display Surface to the screen
    clock.tick(60)  # Maintain 60 frames per second


# Game loop exits here if running is False
font = pygame.font.SysFont(None, 72)
game_over_text = font.render("Game Over", True, (255, 0, 0))
text_rect = game_over_text.get_rect(center=(window_size[0] / 2, window_size[1] / 2))
window.fill((0, 0, 0))  # Clear screen
window.blit(game_over_text, text_rect)
pygame.display.flip()  # Update the full display Surface to the screen

# Pause for a few seconds to display the game over message
pygame.time.wait(3000)

pygame.quit()


pygame.quit()

