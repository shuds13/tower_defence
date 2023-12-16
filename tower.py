import math
import pygame
import random
import sounds
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

#burger5_img = pygame.image.load('burger5.png')  # Load your tower image
#burger5_img = pygame.transform.scale(burger5_img, (60, 60))

wizard_img = pygame.image.load('wizard.png')  # Load your tower image
wizard_img = pygame.transform.scale(wizard_img, (50, 50))
wizard2_img = pygame.image.load('wizard2.png')  # Load your tower image
wizard2_img = pygame.transform.scale(wizard2_img, (55, 55))
wizard3_img = pygame.image.load('wizard3.png')  # Load your tower image
wizard3_img = pygame.transform.scale(wizard3_img, (58, 58))
wizard4_img = pygame.image.load('wizard4.png')  # Load your tower image
wizard4_img = pygame.transform.scale(wizard4_img, (58, 60))

splat_img = pygame.image.load('splat.png')
#splat_img = pygame.transform.scale(splat_img, (120, 120))

# I would rather use original oriented images and rotate when put down - without rotatig rectangle.
# For now use pre-rotated images.
gluegun_img = pygame.image.load('glue_gun.png')
gluegun_img = pygame.transform.scale(gluegun_img, (50, 50))
gluegun2_img = pygame.image.load('glue_gun2.png')
gluegun2_img = pygame.transform.scale(gluegun2_img, (50, 50))
gluegun3_img = pygame.image.load('glue_gun3.png')
gluegun3_img = pygame.transform.scale(gluegun3_img, (50, 50))
gluegun4_img = pygame.image.load('glue_gun4.png')
gluegun4_img = pygame.transform.scale(gluegun4_img, (55, 55))

totem_img = pygame.image.load('totem.png')
totem_img = pygame.transform.scale(totem_img, (50, 50))
totem_img_ingame = pygame.transform.scale(totem_img, (70, 70))

totem2_img = pygame.image.load('totem2.png')
totem2_img = pygame.transform.scale(totem2_img, (73, 73))
#totem2_img_ingame = pygame.transform.scale(totem2_img, (70, 70))

totem3_img = pygame.image.load('totem3.png')
totem3_img = pygame.transform.scale(totem3_img, (80, 80))
totem4_img = pygame.image.load('totem4.png')
totem4_img = pygame.transform.scale(totem4_img, (90, 90))


class Tower:

    price = 0
    name = 'Tower'
    image = None
    range = 100
    see_ghosts = False
    max_level = 1
    footprint = (50,50)  # for distance to place towers - this should not change for a tower (image size may)

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
        #self.start_round_score = 0
        self.see_ghosts = False
        self.beam_width = 5
        self.image_angle_offset = 0
        self.upgrade_name = "Upgrade"
        self.speed_mod = 1
        self.highlight = False
        self.attack_tower = True

    def level_up(self):
        pass

    def show_viz_persis(self, window):
        pass

    def reset_attack_timer(self):
        self.attack_timer = max(int(self.attack_speed * self.speed_mod), 1)
        #print(f"{self.attack_timer=}")

    #def set_start_hits(self):
        #self.start_round_score = self.total_score

    #def reset_tower(self):
        #self.total_score = self.start_round_score
        #self.viz_persist = 0
        ##reset level

    #def get_start_hits(self):
        #return self.start_round_score

    def is_visible(self, enemy):
        return not enemy.invis or self.see_ghosts

    # Goes through enemies - finds first (could find strongest etc...)
    # Note that enemy order if order came on to screen but may not be at the front at any point in time!
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
            self.reset_attack_timer()
            self.is_attacking = True  # Set to True when attacking
        else:
            self.is_attacking = False  # Set to False otherwise
        return score

    def update(self, enemies):
        score = 0
        self.attack_timer -= 1
        #if not self.target or not self.in_range(self.target):
            #self.find_target(enemies)
        if self.attack_timer <= 0:  # not havingt this is why multi-toxic glue agaist big enenmy is not working
            self.find_target(enemies)
            score = self.attack()
            self.total_score += score
        else:
            self.is_attacking = False
        return score

    def get_target_angle(self):
        if not self.target:
            return 0
        if type(self.target) is list:
            #for now point at first target
            target = self.target[0]
        else:
            target = self.target
        dx = target.position[0] - self.position[0]
        dy = target.position[1] - self.position[1]
        return math.degrees(math.atan2(-dy, dx)) - 90  # Subtract 90 degrees if the image points up

    def general_draw(self, window, image, rect):
        if self.highlight:
            pygame.draw.rect(window, (0,160,0), rect, 3)
        window.blit(image, rect.topleft)

    def draw(self, window, enemies=None):
        """Rotate an image while keeping its center."""
        angle = self.get_target_angle()

       # Keep from immediatly returning to upright.
        if angle == 0:
            angle = self.angle
        else:
            self.angle = angle

        rotated_image = pygame.transform.rotate(self.image, angle)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(center=self.position).center)
        self.general_draw(window, rotated_image, new_rect)

    def is_clicked(self, point):
        # Assuming the tower is drawn as a circle with a certain radius
        #radius = 20  # or whatever your tower's radius is
        #return (self.position[0] - point[0]) ** 2 + (self.position[1] - point[1]) ** 2 <= radius ** 2

        # Take account of tower footprint
        # Due to overlap (see navigation.py) in tower placement could clash and will get first placed.
        # For that reason minus some overlap (margin) here.
        margin = 5
        w1 = (self.__class__.footprint[0] // 2) - margin
        h1 = (self.__class__.footprint[1] // 2) - margin
        return abs(self.position[0] - point[0]) < w1 and abs(self.position[1] - point[1]) < h1


    def attack_animate(self, window):
        pygame.draw.line(window, (255, 0, 0), self.position, self.target.position, self.beam_width)

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

# Poss names for upgrades - add when got all
# Fast Firing ??? Not sure with this tower. Descriptive (e.g Rapid firing) or name (e.g. Raptor)
# Blaze  Doomship, Rapid Fire, Assault Ship, Gold Knight, Destroyer, Annihilator, Warship
# Raptor
# Maybe Rapid Fire (green), Destroyer (Red), Raptor (Gold)
class Fighter(Tower):

    price = 50
    name = 'Fighter'
    image = fighter_img
    range = 100
    max_level = 4
    see_ghosts = False


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
        self.upgrade_name = "Rapid Fire"

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
            self.cost += self.upgrade_costs[0]
            # TODO does not curently give level name at top of inset. For that maybe want it to be on
            # level rather than one before - and upgrade will see level - or do list upgrade_costs
            # or level_name and a function that gets it for upgrade.
            self.upgrade_name = "Destroyer"
        if self.level == 3:
            self.attack_speed = 10  # lower is better currently
            self.range = 120
            self.image = fighter3_img
            self.cost += self.upgrade_costs[1]
            self.upgrade_name = "Raptor"
        if self.level == 4:
            self.attack_speed = 6  # lower is better currently - if dam 1 make faster
            self.range = 140
            self.image = fighter4_img
            self.cost += self.upgrade_costs[2]
            self.damage = 2  # compare
            self.beam_width = 7

# Poss names for upgrades - add when got all
# 'Extra Spicy' 'With Cheese' 'Spicy Deluxe' 'Whopper'  Maybe the last 3?
class Burger(Tower):

    price = 65
    name = 'Burger'
    image = burger_img
    range = 60
    max_level = 4 #5

    def __init__(self, position):
        super().__init__(position)
        self.range = Burger.range
        self.attack_speed = 75
        self.damage = 1
        self.cost = Burger.price
        self.image = Burger.image
        self.level = 1
        self.max_attacks = 4
        self.upgrade_costs = [95, 220, 680] # , 1200]
        self.splat_img = pygame.transform.scale(splat_img, (self.range+60, self.range+60))
        self.upgrade_name = "With cheese"

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
            self.upgrade_name = "Extra Spicy" # "Spicy Deluxe" too long currently
        if self.level == 3:
            self.attack_speed = 26  # lower is better currently
            self.range = 75
            self.image = burger3_img
            #self.image = pygame.transform.scale(burger_img, (55, 55))
            self.max_attacks = 8
            self.cost += self.upgrade_costs[1]
            self.splat_img = pygame.transform.scale(splat_img, (self.range+60, self.range+60))
            self.upgrade_name = "Whopper"
        if self.level == 4:
            self.attack_speed = 16  # lower is better currently
            self.range = 80
            self.image = burger4_img
            self.max_attacks = 12
            self.cost += self.upgrade_costs[2]
            self.splat_img = pygame.transform.scale(splat_img, (self.range+60, self.range+60))
            #either slower attack_speed (~20) and damage 2 or faster <15 and damage 1
            self.damage = 2 # not sure - with damage 2 and other stats nothing got past
        #if self.level == 5:
            #self.attack_speed = 8  # lower is better currently
            #self.range = 100
            #self.image = burger5_img
            #self.max_attacks = 20
            #self.cost += self.upgrade_costs[3]
            #self.splat_img = pygame.transform.scale(splat_img, (self.range+60, self.range+60))
            ##either slower attack_speed (~20) and damage 2 or faster <15 and damage 1
            #self.damage = 3 # not sure - with damage 2 and other stats nothing got past

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
            self.reset_attack_timer()
            self.is_attacking = True  # Set to True when attacking
        else:
            self.is_attacking = False  # Set to False otherwise
        return score


    def draw(self, window, enemies=None):
        """Dont rotate burger"""
        new_rect = self.image.get_rect(center=self.image.get_rect(center=self.position).center)
        self.general_draw(window, self.image, new_rect)


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

# Need to fit
# Top: Arch Mage, Enchanter, Sorceror, Mage (Sorceror sounds evil to me)
class Wizard(Tower):

    price = 125
    name = 'Wizard'
    image = wizard_img
    range = 120
    max_level = 4
    see_ghosts = True


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
        self.upgrade_costs = [200, 600, 1400]  # [200]  4th level prob 1800 or 2000 -but for now less
        self.beam_width = 6
        self.see_ghosts = True
        self.max_attacks = 2
        self.max_cloud_attacks = 8
        self.cloud_type = 1
        self.upgrade_name = "Enchanter"

    def draw(self, window, enemies=None):
        """Dont rotate wizard"""
        new_rect = self.image.get_rect(center=self.image.get_rect(center=self.position).center)
        self.general_draw(window, self.image, new_rect)

    def level_up(self):
        self.level +=1
        if self.level == 2:
            self.attack_speed = 30  # lower is better currently
            self.range = 130
            self.image = wizard2_img
            self.cloud_freq = 5  # ironially i think this needs to be less as attack speed is faster
            self.cost += self.upgrade_costs[0]
            self.beam_width = 7
            self.max_attacks = 3
            self.max_cloud_attacks = 14
            self.upgrade_name = "Mage"
        if self.level == 3:
            # I really want to introduce a new spell - maybe blow enemies back or something else.
            self.attack_speed = 15  # lower is better currently
            self.range = 150
            self.image = wizard3_img
            self.cloud_freq = 6  # less freq
            self.cost += self.upgrade_costs[1]
            self.beam_width = 8
            self.max_attacks = 4
            self.max_cloud_attacks = 25
            self.upgrade_name = "Arch Mage"
        if self.level == 4:
            # I really want to introduce a new spell - maybe blow enemies back or something else.
            self.attack_speed = 8  # lower is better currently
            self.range = 170
            self.image = wizard4_img
            self.cloud_freq = 7  # less freq
            self.cost += self.upgrade_costs[2]
            self.beam_width = 9
            self.max_attacks = 5
            self.max_cloud_attacks = 45

    def _is_cloud_attack(self):
        # The slow but elegant way - can do one line also x=y=z
        if self.attack_count % self.cloud_freq == 0:
            #self.cloud_attack = True
            self.cloud_attack = True
            self.cloud_type = 1
            if self.level >= 4:
                if self.attack_count % (2*self.cloud_freq) == 0:
                    self.cloud_type = 2
        else:
            #self.cloud_attack = False
            self.cloud_attack = False
        return self.cloud_attack

    def _is_multi_attack(self):
        # The slow but elegant way - can do one line also x=y=z
        if self.attack_count % self.cloud_freq == 2:
            self.multi_attack = True
        else:
            self.multi_attack = False
        return self.multi_attack


    def get_color(self, cloud_type):
        if cloud_type == 1:
            return 128, 0, 128
        elif cloud_type == 2:
            #return 63, 0, 255
            return 0, 255, 255


    def create_cloud(self, radius):
        c1, c2, c3 = self.get_color(self.cloud_type)
        c_alpha = 128
        cloud = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(cloud, (c1, c2, c3, c_alpha), (radius, radius), radius)
        return cloud

    #def create_cloud2(self, radius):
        #cloud = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        #pygame.draw.circle(cloud, (255, 192, 0, 128), (radius, radius), radius)
        #return cloud


    def draw_lightning(self, screen, start_pos, end_pos, divisions, color):
        if divisions == 0:
            pygame.draw.line(screen, color, start_pos, end_pos, self.beam_width)
        else:
            mid_x = (start_pos[0] + end_pos[0]) // 2 + random.randint(-20, 20)
            mid_y = (start_pos[1] + end_pos[1]) // 2 + random.randint(-20, 20)
            mid_pos = (mid_x, mid_y)

            self.draw_lightning(screen, start_pos, mid_pos, divisions - 1, color)
            self.draw_lightning(screen, mid_pos, end_pos, divisions - 1, color)


    def show_viz_persist(self, window):
        # Currently only cloud persists - could also change in size/color etc
        # TODO avoid duplication

        #cloud = self.create_cloud(self.range)
        # try changing somwhow
        radius = max(0, self.range - 100//self.viz_persist)
        #color = 128
        #color = max(128 - 5*self.viz_persist, 0)
        #cloud = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        #pygame.draw.circle(cloud, (color, 0, color, color), (radius, radius), radius)

        #color = max(128 - 5*self.viz_persist, 0)
        #cloud = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        #pygame.draw.circle(cloud, (color, 0, color, color), (radius, radius), radius)

        #print(f"{self.cloud_attack=}")
        c1, c2, c3 = self.get_color(self.cloud_type)
        #c_alpha = 128
        c_alpha = max(128 - 5*self.viz_persist, 0)
        cloud = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(cloud, (c1, c2, c3, c_alpha), (radius, radius), radius)



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
        elif self.level == 4:
            return (self.position[0]-18, self.position[1]-21)  #update

    # To be every so many attacks but for now replace
    def attack_animate(self, window):
        staff_position = self.get_staff_pos()
        if self.cloud_attack:
            #cloud = pygame.transform.scale(cloud_image, (tower.attack_radius*2, tower.attack_radius*2))
            cloud = self.create_cloud(self.range)
            cloud_rect = cloud.get_rect(center=self.position)
            window.blit(cloud, cloud_rect)

            #cloud = self.create_cloud2(self.range)
            #cloud_rect = cloud.get_rect(center=self.position)
            #window.blit(cloud, cloud_rect)

            pygame.draw.circle(window, (255, 0, 0), staff_position, 15)  # Tower
            self.viz_persist = 5
        else:
            #pygame.draw.line(window, (255,0,255), self.position, self.target.position, self.beam_width)
            if type(self.target) is list:
                for target in self.target:
                    #pygame.draw.line(window, (255,0,255), staff_position, target.position, self.beam_width)
                    self.draw_lightning(window, staff_position, target.position, 3, (255,0,255))

            else:
                #pygame.draw.line(window, (255,0,255), staff_position, self.target.position, self.beam_width)
                #testing lightning strike animation instead of straight line
                if self.level >= 4 and self.target.size > 1:
                    for nn in range(self.target.size):
                        self.draw_lightning(window, staff_position, self.target.position, 3, (255, 192, 0))
                else:
                    self.draw_lightning(window, staff_position, self.target.position, 3, (255,0,255))


    #def find_target(self, enemies):
        ## Only place to call function - after just check self.cloud_attack
        #tmp_target = []
        #self.target = []
        #for enemy in enemies:
            #if self.in_range(enemy) and self.is_visible(enemy):
                #tmp_target.append(enemy)
        #if tmp_target:
            #self.target = self.create_sublist(tmp_target, self.max_attacks)


    #new tired..- need test new one - and prob improve efficiency - cloud ad multi-attack basically same but for N
    #also calls find_enemies even when not attacking - attack_timer test in attack() - why not only
    #do find_target when attack timer is on!!!! Will fix this inefficiency also
    def find_target(self, enemies):
        # Only place to call function - after just check self.cloud_attack
        if self._is_cloud_attack():
            tmp_target = []
            self.target = []

            for enemy in enemies:
                if self.in_range(enemy):
                    tmp_target.append(enemy)
                    #self.target.append(enemy)
            if tmp_target:

                #compare as before all
                #self.target = tmp_target

                self.target = self.create_sublist(tmp_target, self.max_cloud_attacks)
                #print(f"cloud {len(self.target)}")

            # why this - dont remember - not there for burger - could now set to None before
            # but why needed here and not for burger!
            if not self.target:
                self.target = None

        elif self._is_multi_attack():
            tmp_target = []
            self.target = []
            for enemy in enemies:
                if self.in_range(enemy):
                    tmp_target.append(enemy)
            if tmp_target:
                self.target = self.create_sublist(tmp_target, self.max_attacks)
                #print(f"Multi {len(self.target)}")

                #self.target.append(tmp_target[0])
                #if len(tmp_target) > 1:
                    ##could be strongest (if not same as first) - but try last
                    #self.target.append(tmp_target[-1])
        else:
            super().find_target(enemies)



    #old - need test new one - and prob improve efficiency - cloud ad multi-attack basically same but for N
    #def find_target(self, enemies):
        ## Only place to call function - after just check self.cloud_attack
        #if self._is_cloud_attack():
            #self.target = []
            #for enemy in enemies:
                #if self.in_range(enemy):
                    #self.target.append(enemy)
            #if not self.target:
                #self.target = None
        #elif self._is_multi_attack():
            #tmp_target = []
            #self.target = []
            #for enemy in enemies:
                #if self.in_range(enemy):
                    #tmp_target.append(enemy)
            #if tmp_target:
                #self.target.append(tmp_target[0])
                #if len(tmp_target) > 1:
                    ##could be strongest (if not same as first) - but try last
                    #self.target.append(tmp_target[-1])
        #else:
            #super().find_target(enemies)

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
                    if self.cloud_type == 2:
                        multiplier += 1
                    score += target.take_damage(self.damage * multiplier)
            else:
                #For lev 4 I may make special power attack against size 2/3 enemies.
                #Animattin diff color - maybe multiple lightning strikes to same target
                #or slightly displaced at end but I should see if I can make animate
                #combined with attack - why called separately? If combined
                #dont need to store things like attack type....
                #for now may make every 'single' attack so dont need to store - testing
                multiplier = 1
                if self.level >= 4:
                    multiplier = self.target.size
                score = self.target.take_damage(self.damage*multiplier)
            self.reset_attack_timer()
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
            self.reset_attack_timer()
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

# TODO - PROB PUT glue gunner before wizard in side panel
# Big Blobs (or Splatter), Toxic, Toxic Storm (or Toxic Deluge/Tsunami/drench/barrage or similar)
class GlueGunner(Tower):

    price = 80
    name = 'Glue Gunner'
    image = gluegun_img
    range = 100
    max_level = 4

    def __init__(self, position):
        super().__init__(position)
        self.range = GlueGunner.range
        self.attack_speed = 40 # 30
        self.damage = 1
        self.cost = GlueGunner.price
        self.image = GlueGunner.image
        self.level = 1
        self.upgrade_costs = [120, 280, 900]
        self.beam_width = 7
        self.slow_factor = [0.5, 0.8, 0.9]
        self.glue_layers = 2
        self.image_angle_offset = 130
        self.glue_color = (244, 187, 68)
        self.max_attacks = 2
        self.upgrade_name = "Big Blobs"  # could do better!
        self.attack_tower = False

    def level_up(self):
        self.level +=1
        if self.level == 2:
            self.attack_speed = 35
            self.range = 110
            self.image = gluegun2_img
            self.cost += self.upgrade_costs[0]
            self.glue_layers = 3
            self.beam_width = 9
            self.max_attacks = 3
            self.slow_factor = [0.4, 0.8, 0.9]
            self.upgrade_name = "Toxic Glue"

        if self.level == 3:
            self.attack_speed = 30
            #self.range = 110
            self.image = gluegun3_img
            self.cost += self.upgrade_costs[1]
            self.slow_factor = [0.4, 0.75, 0.8]
            self.beam_width = 10
            # try colors - want to show up on green enemies
            self.glue_color = (124, 252, 0) # (15, 255, 80)
            self.toxic_time = 150
            #self.glue_layers = 4
            #self.glue_layers = 1  # testing for regluding
            self.max_toxic_big_reattacks = 1
            self.max_toxic_giant_reattacks = 2
            self.upgrade_name = "Toxic Storm"
            self.attack_tower = True

        if self.level == 4:
            self.attack_speed = 22
            self.range = 120
            self.image = gluegun4_img
            self.cost += self.upgrade_costs[2]
            self.slow_factor = [0.4, 0.6, 0.7]
            self.beam_width = 12
            # try colors - want to show up on green enemies
            self.glue_color = (124, 252, 0) # (15, 255, 80)
            self.toxic_time = 75
            self.glue_layers = 4
            self.max_attacks = 4
            #self.max_toxic_reattacks = 5
            self.max_toxic_big_reattacks = 2
            self.max_toxic_giant_reattacks = 5
            #self.max_toxic_reattacks = 20  # TESTING
            # TODO At level 4 more toxic damage to big opponents and show more glue on them (and others)
            # also in general green glue needs to show up more on green enemies.
            self.attack_tower = True

    #def find_target(self, enemies):
        #for enemy in enemies:
            #if self.level >= 3 and self.in_range(enemy) and self.is_visible(enemy) and not enemy.toxic_glued:
                #self.target = enemy
                #break
            #elif self.in_range(enemy) and self.is_visible(enemy) and not enemy.glued:
                #self.target = enemy
                #break
        #else:
            #self.target = None


    def can_I_reglue(self, enemy):
        if not enemy.toxic_glued:
            return True
        if self.level >= 3:
            if enemy.size > 2 and enemy.toxic_attacks <= self.max_toxic_giant_reattacks:
                return True
            elif enemy.size > 1 and enemy.toxic_attacks <= self.max_toxic_big_reattacks:
                #print(f"{enemy.toxic_attacks=}")
                return True
        return False


    # test shoot slower hit multiple targets - closest - not spread
    # could avoid some duplication here
    def find_target(self, enemies):
        self.target = []
        count = 0

        #print('in find target')

        if not enemies:
            self.target = None

        for enemy in enemies:

            #tesitng
            #if enemy.toxic_glued:
                #print('Nope - hes toxic')

            if self.level >= 3 and self.in_range(enemy) and self.is_visible(enemy) and self.can_I_reglue(enemy):
                count += 1  # TODO this updates whether same enemy or different...
                self.target.append(enemy)
                enemy.toxic_attacks += 1
                if count >= self.max_attacks:
                    break
            elif self.in_range(enemy) and self.is_visible(enemy) and not enemy.glued:
                count += 1
                self.target.append(enemy)
                if count >= self.max_attacks:
                    break
        #else:
            #self.target = None


    # Needs to take account of rotation
    #def get_nozzle_pos(self):
        #if self.level == 1:
            #return self.position
            #return (self.position[0]+20, self.position[1]-10)
        #elif self.level == 2:
            #return (self.position[0]-17, self.position[1]-15)
        #elif self.level == 3:
            #return (self.position[0]+15, self.position[1]-16)





    def attack_animate(self, window):
        #nozzle = self.get_nozzle_pos()
        #print("In animate")
        nozzle = self.position
        for target in self.target:
            pygame.draw.line(window, self.glue_color, nozzle, target.position, self.beam_width)

    # TODO - work out how more than one lev 4 toxic glue gunner combine - can they both attack
    # prob should be so they can both attack either no. times or until so many glue strikes on big target...
    # slow - currently not quite right - they both attack but only one claims the toxic hits!!!!
    # cos enemy has only one attribute toxic_glued_by - but really needs one for each hit!
    # prob need an obj or list of dictionaries to do this. Not sorting this out right now.
    # For each tower hit - record damage per toxic drain.
    def attack(self):
        score = 0
        if self.target and self.attack_timer <= 0:
            self.attack_count += 1
            sounds.play('glue')
            #score = self.target.take_damage(self.damage)
            for target in self.target:
                target.slow_factor = self.slow_factor[target.size-1]
                target.speed = target.base_speed * target.slow_factor
                target.glued = self.glue_layers
                target.glue_color = self.glue_color
                if self.level >= 3:
                    # Do one damage straight away
                    score += target.take_damage(1)
                    target.toxic_glued = True
                    target.toxic_glued_by = self
                    target.toxic_timer = self.toxic_time
                    target.toxic_time = self.toxic_time  # do another pass on this - very tired - dont want to set two values here.
            self.reset_attack_timer()
            self.is_attacking = True  # Set to True when attacking
        else:
            self.is_attacking = False  # Set to False otherwise
        return score

    # return to previous path index - blower
    #def attack(self):
        #score = 0
        #if self.target and self.attack_timer <= 0:
            #self.attack_count += 1
            ##score = self.target.take_damage(self.damage)
            #self.target.path_index -= 1
            #self.reset_attack_timer()
            #self.is_attacking = True  # Set to True when attacking
        #else:
            #self.is_attacking = False  # Set to False otherwise
        #return score

# Maybe the Demons need more than ghost sight - 3rd level wizard or 3rd level totem.
# Top level can blast from peak - lot of damage to big enemies - or some laser
# More ambitious some sort of summoning ability or time limited power - glows during that.
# Or something like prince of darkness power to harvest enemies and send back along track - but
# that would suddenly require being in range of track!
# another idea eyes glow (translucent cirles over eyes) when ghosts are present (from level 2)
# level 3 and/or 4 - eyes glow and blow blobs back to entrance (path_index=0) - from whatever
# is nearest point on track (regardless of range) - can use code in placements to find nearest point on track.
#   - maybe call level something like "Mystic Breath" or something similar or "Divine Breath" or "Divine Wind" (ummm)
class Totem(Tower):

    price = 200  # Prob first level energizes towers - 2nd level see ghosts - but need to make few more easy levels early on.
    name = 'Totem'
    image = totem_img
    in_game_image = totem_img_ingame
    range = 100
    max_level = 4
    footprint = (60,70)

    def __init__(self, position):
        super().__init__(position)
        self.range = Totem.range
        #self.attack_speed = 40 # 30
        #self.damage = 1
        self.cost = Totem.price
        self.image = Totem.in_game_image
        self.level = 1
        self.upgrade_costs = [250, 500, 1000]
        self.upgrade_name = "Ghost Sight"
        self.attack_tower = False

    def level_up(self):
        self.level +=1
        if self.level == 2:
            self.image = totem2_img
            self.cost += self.upgrade_costs[0]
            # Divine Breath if do blow ability - but I don't like that its position dependent (though I want it in game)
            self.upgrade_name = "Arcane Energy"  # For now.
        if self.level == 3:
            self.image = totem3_img
            self.cost += self.upgrade_costs[1]
            self.upgrade_name = "Eye of Moloch"
        if self.level == 4:
            self.image = totem4_img
            self.cost += self.upgrade_costs[2]
            self.attack_tower = True
            self.attack_speed = 10  # maybe constant

    def find_target(self, enemies):
        self.target = None
        for enemy in enemies:
            if enemy.size >= 3:
                self.target = enemy
                break
        if self.target is None:
            self.is_attacking = False

    def attack(self):
        score = 0
        if self.target and self.attack_timer <= 0:
            self.attack_count += 1
            score = self.target.take_damage(self.damage)
            self.reset_attack_timer()
            self.is_attacking = True  # Set to True when attacking
        #else:
            #self.is_attacking = False  # Set to False otherwise
        return score

    def update(self, enemies):
        if self.level < 4:
            return 0
        score = 0
        self.attack_timer -= 1
        #if self.attack_timer <= 0:  # not havingt this is why multi-toxic glue agaist big enenmy is not working
        self.find_target(enemies)
        score = self.attack()
        self.total_score += score
        #else:
            #self.is_attacking = False
        return score

    def _get_eye_pos(self):
        if self.level == 2:
            return (self.position[0]-2, self.position[1]-24), (self.position[0]+8, self.position[1]-24)
        elif self.level == 3:
            return (self.position[0]-6, self.position[1]-25), (self.position[0]+9, self.position[1]-25)
        elif self.level == 4:
            return (self.position[0]-9, self.position[1]-18), (self.position[0]+11, self.position[1]-18)

    def attack_animate(self, window):
        eye_pos = self._get_eye_pos()
        glow_color = (220, 20, 60)
        glow_radius = 9
        c_alpha = 150  # higher is more opaque
        self._make_eye_glow(window, glow_radius, glow_color, c_alpha, eye_pos[0])
        self._make_eye_glow(window, glow_radius, glow_color, c_alpha, eye_pos[1])
        pygame.draw.line(window, glow_color, eye_pos[0], self.target.position, 8)
        pygame.draw.line(window, glow_color, eye_pos[1], self.target.position, 8)
        # this is actually circle on target
        # Animate target glow (an alt could be to use mini burger splat).
        targx = self.target.position[0] + random.randint(-2, 2)
        targy = self.target.position[1] + random.randint(-2, 2)
        target_pos = (targx, targy)
        self._make_eye_glow(window, glow_radius, glow_color, c_alpha, target_pos)

    def _make_eye_glow(self, window, glow_radius, col, c_alpha, eye_pos):
        eyeglow = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(eyeglow, (col[0], col[1], col[2], c_alpha), (glow_radius,glow_radius), glow_radius)
        glow_rect = eyeglow.get_rect(center=eye_pos)
        window.blit(eyeglow, glow_rect)

    def draw(self, window, enemies):
        """Dont rotate toetem"""
        new_rect = self.image.get_rect(center=self.image.get_rect(center=self.position).center)
        self.general_draw(window, self.image, new_rect)

        # If ghosts/spirits on screen eyes glow - oh will have to change position based on level.
        if self.level >= 2 and any(enemy.invis for enemy in enemies):
            c_alpha = 128 + 15*self.level
            glow_radius = self.level + 3
            eye_pos = self._get_eye_pos()
            glow_color = (250, 250, 51)
            self._make_eye_glow(window, glow_radius, glow_color, c_alpha, eye_pos[0])
            self._make_eye_glow(window, glow_radius, glow_color, c_alpha, eye_pos[1])

    def tower_in_range(self, tower):
        distance = ((self.position[0] - tower.position[0])**2 + (self.position[1] - tower.position[1])**2)**0.5
        return distance <= self.range

    #prob remove hit count for inset window for towers that cant attack.
    #currently totems mods dont stack - but more powerful one in radius should take effect.
    #add range range_mod and at least at highest level increase range on totem itself.
    def boost(self, tower):
        # Not changing range for now.
        if self.level >= 1:
            tower.speed_mod = 0.9
        if self.level >= 2:
            tower.see_ghosts = True
        #below here experimenting late at night. Also range wld need a mod.
        if self.level >= 3:
            #tower.speed_mod = 0.8 # may add demon sight here
            tower.speed_mod = 0.75 # while addin nothing else - boost a bit
        if self.level >= 4:
            # maybe laser eyes that attack and/or some long-range attack:
            #tower.speed_mod = 0.7 # may add demon sight here
            tower.speed_mod = 0.6 # while addin nothing else - boost a bit

tower_types = [Fighter, Burger, GlueGunner, Wizard, Totem]

