import math
import pygame
#pygame.init()
#screen = pygame.display.set_mode((800, 600))

fighter_img = pygame.image.load('tower1.png')
fighter_img = pygame.transform.scale(fighter_img, (50, 50))
fighter2_img = pygame.image.load('tower1_lev2.png')
fighter2_img = pygame.transform.scale(fighter2_img, (50, 50))
fighter3_img = pygame.image.load('tower1_lev3.png')
fighter3_img = pygame.transform.scale(fighter3_img, (55, 55))
fighter4_img = pygame.image.load('tower1_lev4.png')
fighter4_img = pygame.transform.scale(fighter4_img, (60, 60))

burger_img = pygame.image.load('burger.png')  # Load your tower image
burger_img = pygame.transform.scale(burger_img, (50, 50))
burger2_img = pygame.image.load('burger2.png')  # Load your tower image
burger2_img = pygame.transform.scale(burger2_img, (52, 52))
burger3_img = pygame.image.load('burger3.png')  # Load your tower image
burger3_img = pygame.transform.scale(burger3_img, (55, 55))
burger4_img = pygame.image.load('burger4.png')  # Load your tower image
burger4_img = pygame.transform.scale(burger4_img, (60, 60))

wizard_img = pygame.image.load('wizard.png')  # Load your tower image
wizard_img = pygame.transform.scale(wizard_img, (50, 50))
wizard2_img = pygame.image.load('wizard2.png')  # Load your tower image
wizard2_img = pygame.transform.scale(wizard2_img, (55, 55))
wizard3_img = pygame.image.load('wizard3.png')  # Load your tower image
wizard3_img = pygame.transform.scale(wizard3_img, (58, 58))

splat_img = pygame.image.load('splat.png')
#splat_img = pygame.transform.scale(splat_img, (120, 120))

class Tower:

    price = 0
    name = 'Tower'
    image = None
    range = 100
    max_level = 1

    def __init__(self, position):
        self.position = position
        self.range = Tower.range
        self.attack_speed = 40
        self.attack_timer = 0
        self.target = None
        self.damage = 1
        self.is_attacking = False
        self.cost = Tower.price
        self.angle = 0
        self.attack_count = 0
        self.viz_persist = 0
        self.level = 1
        self.total_score = 0
        self.see_ghosts = False
        self.beam_width = 5

    def level_up(self):
        pass

    def show_viz_persis(self, window):
        pass

    def is_visible(self, enemy):
        return not enemy.invis or self.see_ghosts

    # Goes through enemies - finds first (could find strongest etc...)
    def find_target(self, enemies):
        for enemy in enemies:
            if self.in_range(enemy) and self.is_visible(enemy):
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
            self.attack_count += 1
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
        self.total_score += score
        return score

    def get_target_angle(self):
        if not self.target:
            return 0
        dx = self.target.position[0] - self.position[0]
        dy = self.target.position[1] - self.position[1]
        return math.degrees(math.atan2(-dy, dx)) - 90  # Subtract 90 degrees if the image points up

    def draw(self, window):
        """Rotate an image while keeping its center."""
        angle = self.get_target_angle()

       # Keep from immediatly returning to upright.
        if angle == 0:
            angle = self.angle
        else:
            self.angle = angle

        rotated_image = pygame.transform.rotate(self.image, angle)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(center=self.position).center)

        window.blit(rotated_image, new_rect.topleft)
        #return rotated_image, new_rect

    def is_clicked(self, point):
        # Assuming the tower is drawn as a circle with a certain radius
        radius = 20  # or whatever your tower's radius is
        return (self.position[0] - point[0]) ** 2 + (self.position[1] - point[1]) ** 2 <= radius ** 2

    def attack_animate(self, window):
        pygame.draw.line(window, (255, 0, 0), self.position, self.target.position, self.beam_width)

class Fighter(Tower):

    price = 50
    name = 'Fighter'
    image = fighter_img
    range = 100
    max_level = 4

    def __init__(self, position):
        super().__init__(position)
        self.range = Fighter.range
        self.attack_speed = 40
        self.damage = 1
        self.cost = Fighter.price
        self.image = Fighter.image
        self.level = 1
        self.upgrade_costs = [40, 150, 400]
        self.beam_width = 5
        #self.max_level = Fighter.max_level  # try using __class__ and if works do same for other attributes

    def level_up(self):
        #should never happen - if have this condition - then return money to remove from player
        #if self.level == self.__class__.max_level:
            #return
            #print('here3a')

        self.level +=1
        if self.level == 2:
            self.attack_speed = 25  # lower is better currently
            self.range = 110
            self.image = fighter2_img
            self.cost += self.upgrade_costs[0]  # used in sell price calc - sell price should prob be returned from this obj
        if self.level == 3:
            self.attack_speed = 10  # lower is better currently
            self.range = 120
            self.image = fighter3_img
            self.cost += self.upgrade_costs[1]
        if self.level == 4:
            self.attack_speed = 6  # lower is better currently - if dam 1 make faster
            self.range = 140
            self.image = fighter4_img
            self.cost += self.upgrade_costs[2]
            self.damage = 2  # compare
            self.beam_width = 7

class Burger(Tower):

    price = 65
    name = 'Burger'
    image = burger_img
    range = 60
    max_level = 4

    def __init__(self, position):
        super().__init__(position)
        self.range = Burger.range
        self.attack_speed = 75
        self.damage = 1
        self.cost = Burger.price
        self.image = Burger.image
        self.level = 1
        self.max_attacks = 4
        self.upgrade_costs = [95, 220, 680]
        self.splat_img = pygame.transform.scale(splat_img, (self.range+60, self.range+60))

    def level_up(self):
        self.level +=1
        if self.level == 2:
            self.attack_speed = 55  # lower is better currently
            self.range = 70
            self.image = burger2_img
            #self.image = pygame.transform.scale(burger_img, (55, 55))
            self.max_attacks = 6
            self.cost += self.upgrade_costs[0]
            self.splat_img = pygame.transform.scale(splat_img, (self.range+60, self.range+60))
        if self.level == 3:
            self.attack_speed = 26  # lower is better currently
            self.range = 75
            self.image = burger3_img
            #self.image = pygame.transform.scale(burger_img, (55, 55))
            self.max_attacks = 8
            self.cost += self.upgrade_costs[1]
            self.splat_img = pygame.transform.scale(splat_img, (self.range+60, self.range+60))
        if self.level == 4:
            self.attack_speed = 16  # lower is better currently
            self.range = 80
            self.image = burger4_img
            self.max_attacks = 12
            self.cost += self.upgrade_costs[2]
            self.splat_img = pygame.transform.scale(splat_img, (self.range+60, self.range+60))
            #either slower attack_speed (~20) and damage 2 or faster <15 and damage 1
            self.damage = 2 # not sure - with damage 2 and other stats nothing got past

    # Splat attack!
    def attack(self):
        score = 0
        if self.target and self.attack_timer <= 0:
            # If using IF this could be in generic one
            self.attack_count += 1
            if type(self.target) is list:
                for target in self.target:
                    # Do more damage to big enemies to simulate multiple projectiles hitting
                    #multiplier = target.size  # maybe too strong?
                    if target.size >=3:
                        multiplier = 2
                    else:
                        multiplier = 1
                    #print(multiplier)
                    score += target.take_damage(self.damage * multiplier)
            else:
                # is burger ever here? Nope
                multiplier = self.target.size  # Do more damage to big enemies to simulate multiple projectiles hitting
                #print('single', multiplier)
                score = self.target.take_damage(self.damage * multiplier)
            #print(f"{score=}")
            self.attack_timer = self.attack_speed
            self.is_attacking = True  # Set to True when attacking
        else:
            self.is_attacking = False  # Set to False otherwise
        return score

    def create_sublist(self,input_list, N):
        """
        Create a sublist of N equally spaced elements from the input list.
        If the input list has N or fewer elements, the sublist is a copy of the input list.
        """
        if len(input_list) <= N:
            # If the input list is smaller than or equal to N, return a copy of the input list
            return input_list.copy()
        else:
            # Calculate the step size for equally spaced elements
            step = len(input_list) / N
            # Create the sublist using list comprehension
            return [input_list[int(i * step)] for i in range(N)]

    def draw(self, window):
        """Dont rotate burger"""
        #rotated_image = self.image  # pygame.transform.rotate(self.image, angle)
        new_rect = self.image.get_rect(center=self.image.get_rect(center=self.position).center)
        window.blit(self.image, new_rect.topleft)
        #return rotated_image, new_rect

    def find_target(self, enemies):
        # Only place to call function - after just check self.cloud_attack
        tmp_target = []
        self.target = []
        for enemy in enemies:
            if self.in_range(enemy) and self.is_visible(enemy):
                tmp_target.append(enemy)
        if tmp_target:
            self.target = self.create_sublist(tmp_target, self.max_attacks)


    # Could do retention of image like wizard cloud but its actually ok
    def attack_animate(self, window):
        #for target in self.target:
            #pygame.draw.line(window, (255,0,0), self.position, target.position, self.beam_width)
            #image_rect = self.splat_img.get_rect(center=(x + width // 2, image_y_pos))
        image_rect = self.splat_img.get_rect(center=self.position)
        window.blit(self.splat_img, image_rect)
        # draw burger back on top - normally dont notice but for end of levels etc.
        self.draw(window)


        #pygame.display.flip()
        #import time
        #time.sleep(2)


class Wizard(Tower):

    price = 125
    name = 'Wizard'
    image = wizard_img
    range = 120
    max_level = 3

    def __init__(self, position):
        super().__init__(position)
        self.range = Wizard.range
        self.attack_speed = 60
        self.damage = 2
        self.cost = Wizard.price
        self.image = Wizard.image
        self.level = 1
        self.cloud_freq = 4
        self.attack_count = 0
        self.cloud_attack = False
        self.upgrade_costs = [200, 600]  # [200]
        self.beam_width = 8
        self.see_ghosts = True


    def draw(self, window):
        """Dont rotate burger"""
        #rotated_image = self.image  # pygame.transform.rotate(self.image, angle)
        new_rect = self.image.get_rect(center=self.image.get_rect(center=self.position).center)
        window.blit(self.image, new_rect.topleft)

    #def rotate(self):
        #"""Dont rotate wizard"""
        #rotated_image = self.image  # pygame.transform.rotate(self.image, angle)
        #new_rect = rotated_image.get_rect(center=self.image.get_rect(center=self.position).center)
        #return rotated_image, new_rect

    def level_up(self):
        self.level +=1
        if self.level == 2:
            self.attack_speed = 30  # lower is better currently
            self.range = 130
            self.image = wizard2_img
            self.cloud_freq = 5  # ironially i think this needs to be less as attack speed is faster
            self.cost += self.upgrade_costs[0]
            self.beam_width = 10
        if self.level == 3:
            # I really want to introduce a new spell - maybe blow enemies back or something else.
            self.attack_speed = 15  # lower is better currently
            self.range = 150
            self.image = wizard3_img
            self.cloud_freq = 6  # less freq
            self.cost += self.upgrade_costs[1]
            self.beam_width = 12

    def _is_cloud_attack(self):
        # The slow but elegant way - can do one line also x=y=z
        if self.attack_count % self.cloud_freq == 0:
            self.cloud_attack = True
        else:
            self.cloud_attack = False
        return self.cloud_attack

    def _is_multi_attack(self):
        # The slow but elegant way - can do one line also x=y=z
        if self.attack_count % self.cloud_freq == 2:
            self.multi_attack = True
        else:
            self.multi_attack = False
        return self.multi_attack


    def create_cloud(self, radius):
        cloud = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(cloud, (128, 0, 128, 128), (radius, radius), radius)
        return cloud

    def show_viz_persist(self, window):
        # Currently only cloud persists - could also change in size/color etc
        # TODO avoid duplication

        #cloud = self.create_cloud(self.range)
        # try changing somwhow
        radius = max(0, self.range - 100//self.viz_persist)
        #color = 128
        color = max(128 - 5*self.viz_persist, 0)
        cloud = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(cloud, (color, 0, color, color), (radius, radius), radius)

        cloud_rect = cloud.get_rect(center=self.position)
        window.blit(cloud, cloud_rect)
        if self.viz_persist > 0:
            self.viz_persist -= 1


    def get_staff_pos(self):
        if self.level == 1:
            return (self.position[0]+20, self.position[1]-10)
        elif self.level == 2:
            return (self.position[0]-17, self.position[1]-15)
        elif self.level == 3:
            return (self.position[0]+15, self.position[1]-16)

    # To be every so many attacks but for now replace
    def attack_animate(self, window):
        staff_position = self.get_staff_pos()
        if self.cloud_attack:
            #cloud = pygame.transform.scale(cloud_image, (tower.attack_radius*2, tower.attack_radius*2))
            cloud = self.create_cloud(self.range)
            cloud_rect = cloud.get_rect(center=self.position)
            window.blit(cloud, cloud_rect)
            pygame.draw.circle(window, (255, 0, 0), staff_position, 15)  # Tower
            self.viz_persist = 5
        else:
            #pygame.draw.line(window, (255,0,255), self.position, self.target.position, self.beam_width)
            if type(self.target) is list:
                for target in self.target:
                    pygame.draw.line(window, (255,0,255), staff_position, target.position, self.beam_width)
            else:
                pygame.draw.line(window, (255,0,255), staff_position, self.target.position, self.beam_width)

    def find_target(self, enemies):
        # Only place to call function - after just check self.cloud_attack
        if self._is_cloud_attack():
            self.target = []
            for enemy in enemies:
                if self.in_range(enemy):
                    self.target.append(enemy)
            if not self.target:
                self.target = None
        elif self._is_multi_attack():
            tmp_target = []
            self.target = []
            for enemy in enemies:
                if self.in_range(enemy):
                    tmp_target.append(enemy)
            if tmp_target:
                self.target.append(tmp_target[0])
                if len(tmp_target) > 1:
                    #could be strongest (if not same as first) - but try last
                    self.target.append(tmp_target[-1])
        else:
            super().find_target(enemies)

    # Could be generic to deal with lists
    def attack(self):
        score = 0
        if self.target and self.attack_timer <= 0:
            # If using IF this could be in generic one
            self.attack_count += 1
            if type(self.target) is list:
                for target in self.target:
                    if target.size >=3:
                        multiplier = 2
                    else:
                        multiplier = 1
                    score += target.take_damage(self.damage * multiplier)
            else:
                score = self.target.take_damage(self.damage)
            self.attack_timer = self.attack_speed
            self.is_attacking = True  # Set to True when attacking
        else:
            self.is_attacking = False  # Set to False otherwise
        return score

    # TODO can now use burger algorithm to attach >2 - act is this fumc diff from attack
    # maybe can remove this - its find_target that has code for targeting multiple
    def multi_attack(self):
        score = 0
        if self.target and self.attack_timer <= 0:
            # If using IF this could be in generic one
            self.attack_count += 1
            if type(self.target) is list:
                for target in self.target:
                    score += target.take_damage(self.damage)
            else:
                score = self.target.take_damage(self.damage)
            self.attack_timer = self.attack_speed
            self.is_attacking = True  # Set to True when attacking
        else:
            self.is_attacking = False  # Set to False otherwise
        return score

    # Also could be generic to deal with lists - or he does not rotate when uses cloud attack
    def get_target_angle(self):
        if not self.target:
            return 0
        if type(self.target) is list:
            target = self.target[0]
        else:
            target = self.target
        dx = target.position[0] - self.position[0]
        dy = target.position[1] - self.position[1]
        return math.degrees(math.atan2(-dy, dx)) - 90  # Subtract 90 degrees if the image points up


tower_types = [Fighter, Burger, Wizard]
