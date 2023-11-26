import math

class Tower:
    def __init__(self, position, range, attack_speed):
        self.position = position
        self.range = range
        self.attack_speed = attack_speed
        self.attack_timer = 0
        self.target = None
        self.damage = 1
        self.is_attacking = False

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
        if self.target and self.attack_timer <= 0:
            self.target.take_damage(self.damage)
            self.attack_timer = self.attack_speed
            self.is_attacking = True  # Set to True when attacking
        else:
            self.is_attacking = False  # Set to False otherwise

    def update(self, enemies):
        self.attack_timer -= 1
        #if not self.target or not self.in_range(self.target):
            #self.find_target(enemies)
        self.find_target(enemies)
        self.attack()

    def get_target_angle(self):
        if not self.target:
            return 0
        dx = self.target.position[0] - self.position[0]
        dy = self.target.position[1] - self.position[1]
        return math.degrees(math.atan2(-dy, dx)) - 90  # Subtract 90 degrees if the image points up


