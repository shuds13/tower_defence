import pygame
pygame.mixer.init()

snd_blop = pygame.mixer.Sound('blop.wav')

class Enemy:
    def __init__(self, path):
        self.path = path
        self.path_index = 0
        self.position = self.path[0]
        self.speed = 2
        self.reached_end = False  # Indicates if the enemy has reached the end of the path
        self.health = 1
        self.value = 1
        self.color = (255, 0, 0)

    def move(self):
        # Move towards the next point in the path
        if self.path_index < len(self.path) - 1:
            target_pos = self.path[self.path_index + 1]
            dx, dy = target_pos[0] - self.position[0], target_pos[1] - self.position[1]
            distance = (dx**2 + dy**2)**0.5
            if distance > self.speed:
                dx, dy = dx / distance * self.speed, dy / distance * self.speed
            self.position = (self.position[0] + dx, self.position[1] + dy)

            # Check if the enemy has reached the target position
            if abs(self.position[0] - target_pos[0]) < self.speed and abs(self.position[1] - target_pos[1]) < self.speed:
                self.path_index += 1

        # Check if the enemy has reached the end of the path
        if self.path_index >= len(self.path) - 1:
            self.reached_end = True

    def take_damage(self, damage):
        self.health -= damage
        snd_blop.play()
        if self.health <= 0:
            self.reached_end = True  # Treat the enemy as "dead" or "reached the end"
        if self.reached_end:
            return self.value
        return 0

class Enemy2(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.health = 2
        self.value = 2
        self.speed = 3
        self.color = (0, 0, 255)  # todo maybe turn red after one damage

    def take_damage(self, damage):
        self.health -= damage
        snd_blop.play()
        if self.health <= 0:
            self.reached_end = True  # Treat the enemy as "dead" or "reached the end"
        elif self.health == 1:  # same other than these 2 lines - maybe can combine with super.
            self.color = (255, 0, 0)
            self.speed = 2
        if self.reached_end:
            return self.value
        return 0

enemy_types = {1: Enemy, 2: Enemy2}
