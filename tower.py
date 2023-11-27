import math
import pygame

fighter_img = pygame.image.load('tower1.png')  # Load your tower image
fighter_img = pygame.transform.scale(fighter_img, (50, 50))

burger_img = pygame.image.load('burger.png')  # Load your tower image
burger_img = pygame.transform.scale(burger_img, (50, 50))


class Tower:

    price = 0
    name = 'Tower'
    image = None
    range = 100

    def __init__(self, position):
        self.position = position
        self.range = Tower.range
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
        rotated_image = pygame.transform.rotate(self.image, angle)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(center=self.position).center)
        return rotated_image, new_rect

class Fighter(Tower):

    price = 50
    name = 'Fighter'
    image = fighter_img
    range = 100

    def __init__(self, position):
        super().__init__(position)
        self.range = Fighter.range
        self.attack_speed = 40
        self.damage = 1
        self.cost = Fighter.price
        self.image = Fighter.image

class Burger(Tower):

    price = 25
    name = 'Burger'
    image = burger_img
    range = 75

    def __init__(self, position):
        super().__init__(position)
        self.range = Burger.range
        self.attack_speed = 80
        self.damage = 1
        self.cost = Burger.price
        self.image = Burger.image

    #def rotate(self):
        #"""Rotate an image while keeping its center."""
        #angle = self.get_target_angle()
        #rotated_image = pygame.transform.rotate(burger_img, angle)
        #new_rect = rotated_image.get_rect(center=burger_img.get_rect(center=self.position).center)
        #return rotated_image, new_rect

tower_types = [Fighter, Burger]
