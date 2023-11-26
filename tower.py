import math
import pygame

tower_image = pygame.image.load('tower1.png')  # Load your tower image
tower_image = pygame.transform.scale(tower_image, (50, 50))

tower_image2 = pygame.image.load('burger.png')  # Load your tower image
tower_image2 = pygame.transform.scale(tower_image2, (50, 50))


class Tower:

    price = 0
    name = 'Tower'

    def __init__(self, position):
        self.position = position
        self.range = 100
        self.attack_speed = 40
        self.attack_timer = 0
        self.target = None
        self.damage = 1
        self.is_attacking = False
        self.cost = Tower.price

    def find_target(self, enemies):
        for enemy in enemies:
            if self.in_range(enemy):
                self.target = enemy
                break
        else:
            self.target = None

    def in_range(self, enemy):
        distance = ((self.position[0] - enemy.position[0])**2 + (self.position[1] - enemy.position[1])**2)**0.5
        return distance <= self.range

    def attack(self):
        score = 0
        if self.target and self.attack_timer <= 0:
            score = self.target.take_damage(self.damage)
            self.attack_timer = self.attack_speed
            self.is_attacking = True  # Set to True when attacking
        else:
            self.is_attacking = False  # Set to False otherwise
        return score

    def update(self, enemies):
        self.attack_timer -= 1
        #if not self.target or not self.in_range(self.target):
            #self.find_target(enemies)
        self.find_target(enemies)
        score = self.attack()
        return score

    def get_target_angle(self):
        if not self.target:
            return 0
        dx = self.target.position[0] - self.position[0]
        dy = self.target.position[1] - self.position[1]
        return math.degrees(math.atan2(-dy, dx)) - 90  # Subtract 90 degrees if the image points up

    def rotate(self):
        """Rotate an image while keeping its center."""
        angle = self.get_target_angle()
        rotated_image = pygame.transform.rotate(tower_image, angle)
        new_rect = rotated_image.get_rect(center=tower_image.get_rect(center=self.position).center)
        return rotated_image, new_rect

class Fighter(Tower):

    price = 50
    name = 'Fighter'

    def __init__(self, position):
        super().__init__(position)
        self.range = 100
        self.attack_speed = 40
        self.damage = 1
        self.cost = Fighter.price

class Burger(Tower):

    price = 10
    name = 'Burger'

    def __init__(self, position):
        super().__init__(position)
        self.range = 75
        self.attack_speed = 100
        self.damage = 1
        self.cost = Burger.price

    def rotate(self):
        """Rotate an image while keeping its center."""
        angle = self.get_target_angle()
        rotated_image = pygame.transform.rotate(tower_image2, angle)
        new_rect = rotated_image.get_rect(center=tower_image2.get_rect(center=self.position).center)
        return rotated_image, new_rect
