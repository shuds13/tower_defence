import math
import pygame
import random
import sounds

fighter_img = pygame.image.load('images/tower1.png')
fighter_img = pygame.transform.scale(fighter_img, (50, 50))
fighter2_img = pygame.image.load('images/tower1_lev2.png')
fighter2_img = pygame.transform.scale(fighter2_img, (50, 50))
fighter3_img = pygame.image.load('images/tower1_lev3.png')
fighter3_img = pygame.transform.scale(fighter3_img, (55, 55))
fighter4_img = pygame.image.load('images/tower1_lev4.png')
fighter4_img = pygame.transform.scale(fighter4_img, (60, 60))

burger_img = pygame.image.load('images/burger.png')
burger_img = pygame.transform.scale(burger_img, (50, 50))
burger2_img = pygame.image.load('images/burger2.png')
burger2_img = pygame.transform.scale(burger2_img, (52, 52))
burger3_img = pygame.image.load('images/burger3.png')
burger3_img = pygame.transform.scale(burger3_img, (55, 55))
burger4_img = pygame.image.load('images/burger4.png')
burger4_img = pygame.transform.scale(burger4_img, (60, 60))
#burger5_img = pygame.image.load('images/burger5.png')
#burger5_img = pygame.transform.scale(burger5_img, (60, 60))
splat_img = pygame.image.load('images/splat.png')

wizard_img = pygame.image.load('images/wizard.png')
wizard_img = pygame.transform.scale(wizard_img, (50, 50))
wizard2_img = pygame.image.load('images/wizard2.png')
wizard2_img = pygame.transform.scale(wizard2_img, (55, 55))
wizard3_img = pygame.image.load('images/wizard3.png')
wizard3_img = pygame.transform.scale(wizard3_img, (58, 58))
wizard4_img = pygame.image.load('images/wizard4.png')
wizard4_img = pygame.transform.scale(wizard4_img, (58, 60))

gluegun_img = pygame.image.load('images/glue_gun.png')
gluegun_img = pygame.transform.scale(gluegun_img, (50, 50))
gluegun2_img = pygame.image.load('images/glue_gun2.png')
gluegun2_img = pygame.transform.scale(gluegun2_img, (50, 50))
gluegun3_img = pygame.image.load('images/glue_gun3.png')
gluegun3_img = pygame.transform.scale(gluegun3_img, (50, 50))
gluegun4_img = pygame.image.load('images/glue_gun4.png')
gluegun4_img = pygame.transform.scale(gluegun4_img, (55, 55))

totem_img = pygame.image.load('images/totem.png')
totem_img = pygame.transform.scale(totem_img, (50, 50))
totem_img_ingame = pygame.transform.scale(totem_img, (70, 70))
totem2_img = pygame.image.load('images/totem2.png')
totem2_img = pygame.transform.scale(totem2_img, (73, 73))
totem3_img = pygame.image.load('images/totem3.png')
totem3_img = pygame.transform.scale(totem3_img, (80, 80))
totem4_img = pygame.image.load('images/totem4.png')
totem4_img = pygame.transform.scale(totem4_img, (90, 90))


cannon_img = pygame.image.load('images/cannon.png')
cannon_img = pygame.transform.scale(cannon_img, (50, 50))


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
        self.range_mod = 1
        self.range =  Tower.range
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
        self.image_angle_offset = 0
        self.upgrade_name = "Upgrade"
        self.speed_mod = 1
        self.highlight = False
        self.attack_tower = True

    def current_range(self):
        return self.range * self.range_mod

    def level_up(self):
        pass

    def show_viz_persis(self, window):
        pass

    def reset_attack_timer(self):
        self.attack_timer = max(int(self.attack_speed * self.speed_mod), 1)

    def is_visible(self, enemy):
        return not enemy.invis or self.see_ghosts

    # Goes through enemies - finds first (could find strongest etc...)
    # Note that enemy order is order came on to screen but may not be at the front at any point in time!
    def find_target(self, enemies):
        for enemy in enemies:
            if self.in_range(enemy) and self.is_visible(enemy) and not enemy.reached_end:
                self.target = enemy
                break
        else:
            self.target = None

    def in_range(self, enemy):
        distance = ((self.position[0] - enemy.position[0])**2 + (self.position[1] - enemy.position[1])**2)**0.5
        return distance <= self.current_range()

    def attack(self):
        score = 0
        if self.target and self.attack_timer <= 0:
            self.attack_count += 1
            score = self.target.take_damage(self.damage)
            self.reset_attack_timer()
            self.is_attacking = True
        else:
            self.is_attacking = False
        return score

    def update(self, enemies):
        score = 0
        self.attack_timer -= 1
        if self.attack_timer <= 0:
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


class Fighter(Tower):

    price = 50
    name = 'Fighter'
    image = fighter_img
    range = 100
    max_level = 4
    see_ghosts = False

    def __init__(self, position):
        super().__init__(position)
        self.range =  Fighter.range
        self.attack_speed = 40
        self.damage = 1
        self.cost = Fighter.price
        self.image = Fighter.image
        self.level = 1
        self.upgrade_costs = [40, 180, 400]
        self.beam_width = 5
        self.upgrade_name = "Rapid Fire"

    def level_up(self):
        self.level +=1
        if self.level == 2:
            self.attack_speed = 25  # lower is better currently
            self.range =  110
            self.image = fighter2_img
            self.cost += self.upgrade_costs[0]
            # TODO does not curently give level name in inset. For that maybe want it to be on
            # level rather than one before - and upgrade will see level - or do list upgrade_costs
            # or level_name and a function that gets it for upgrade.
            self.upgrade_name = "Destroyer"
        if self.level == 3:
            self.attack_speed = 10  # lower is better currently
            self.range =  120
            self.image = fighter3_img
            self.cost += self.upgrade_costs[1]
            self.upgrade_name = "Raptor"
        if self.level == 4:
            self.attack_speed = 6  # (if dam 1 then make faster)
            self.range =  140
            self.image = fighter4_img
            self.cost += self.upgrade_costs[2]
            self.damage = 2
            self.beam_width = 7


class Burger(Tower):

    price = 65
    name = 'Burger'
    image = burger_img
    range = 60
    max_level = 4 #5

    def __init__(self, position):
        super().__init__(position)
        self.range =  Burger.range
        self.attack_speed = 75
        self.damage = 1
        self.cost = Burger.price
        self.image = Burger.image
        self.level = 1
        self.max_attacks = 4
        self.upgrade_costs = [95, 220, 680] # , 1200]
        # range_mod cant be used here - so would have to update when update range_mod
        self.splat_img = pygame.transform.scale(splat_img, (self.range+60, self.range+60))
        self.upgrade_name = "With cheese"

    def level_up(self):
        self.level +=1
        if self.level == 2:
            self.attack_speed = 55  # lower is better currently
            self.range =  70
            self.image = burger2_img
            self.max_attacks = 6
            self.cost += self.upgrade_costs[0]
            self.splat_img = pygame.transform.scale(splat_img, (self.range+60, self.range+60))
            self.upgrade_name = "Extra Spicy"
        if self.level == 3:
            self.attack_speed = 26
            self.range =  75
            self.image = burger3_img
            self.max_attacks = 8
            self.cost += self.upgrade_costs[1]
            self.splat_img = pygame.transform.scale(splat_img, (self.range+60, self.range+60))
            self.upgrade_name = "Whopper"
        if self.level == 4:
            self.attack_speed = 12 # 16 (dam 2)
            self.range =  80
            self.image = burger4_img
            self.max_attacks = 15  # 12 (dam 2)
            self.cost += self.upgrade_costs[2]
            self.splat_img = pygame.transform.scale(splat_img, (self.range+60, self.range+60))
        #if self.level == 5:
            #self.attack_speed = 8  # lower is better currently
            #self.range =  100
            #self.image = burger5_img
            #self.max_attacks = 20
            #self.cost += self.upgrade_costs[3]
            #self.splat_img = pygame.transform.scale(splat_img, (self.range+60, self.range+60))
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
                    score += target.take_damage(self.damage * multiplier)
            else:
                # dont think ever here
                multiplier = self.target.size  # Do more damage to big enemies to simulate multiple projectiles hitting
                #print('single', multiplier)
                score = self.target.take_damage(self.damage * multiplier)
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
            if self.in_range(enemy) and self.is_visible(enemy) and not enemy.reached_end:
                tmp_target.append(enemy)
        if tmp_target:
            self.target = self.create_sublist(tmp_target, self.max_attacks)

    # Could do retention of image like wizard cloud but its actually ok
    def attack_animate(self, window):
        image_rect = self.splat_img.get_rect(center=self.position)
        window.blit(self.splat_img, image_rect)
        # draw burger back on top of splat
        self.draw(window)


# Possible level names Arch Mage, Enchanter, Sorceror, Mage (Sorceror sounds evil to me)
class Wizard(Tower):

    price = 125
    name = 'Wizard'
    image = wizard_img
    range = 120
    max_level = 4
    see_ghosts = True

    def __init__(self, position):
        super().__init__(position)
        self.range =  Wizard.range
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
            self.range =  130
            self.image = wizard2_img
            self.cloud_freq = 5  # ironially i think this needs to be less as attack speed is faster
            self.cost += self.upgrade_costs[0]
            self.beam_width = 7
            self.max_attacks = 3
            self.max_cloud_attacks = 14
            self.upgrade_name = "Mage"
        if self.level == 3:
            self.attack_speed = 15
            self.range =  150
            self.image = wizard3_img
            self.cloud_freq = 6  # less freq per regular attack (but more frequent in time)
            self.cost += self.upgrade_costs[1]
            self.beam_width = 8
            self.max_attacks = 4
            self.max_cloud_attacks = 25
            self.upgrade_name = "Arch Mage"
        if self.level == 4:
            # I want to introduce a new spell - maybe blow enemies back or something else.
            self.attack_speed = 8
            self.range =  170
            self.image = wizard4_img
            self.cloud_freq = 7
            self.cost += self.upgrade_costs[2]
            self.beam_width = 9
            self.max_attacks = 5
            self.max_cloud_attacks = 45

    def _is_cloud_attack(self):
        # The slow but elegant way
        if self.attack_count % self.cloud_freq == 0:
            self.cloud_attack = True
            self.cloud_type = 1
            if self.level >= 4:
                if self.attack_count % (2*self.cloud_freq) == 0:
                    self.cloud_type = 2
        else:
            self.cloud_attack = False
        return self.cloud_attack

    def _is_multi_attack(self):
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
        radius = max(0, self.current_range() - 100//self.viz_persist)
        c1, c2, c3 = self.get_color(self.cloud_type)
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
            return (self.position[0]-18, self.position[1]-21)

    def attack_animate(self, window):
        staff_position = self.get_staff_pos()
        if self.cloud_attack:
            cloud = self.create_cloud(self.current_range())
            cloud_rect = cloud.get_rect(center=self.position)
            window.blit(cloud, cloud_rect)
            pygame.draw.circle(window, (255, 0, 0), staff_position, 15)  # Tower
            self.viz_persist = 5
        else:
            #pygame.draw.line(window, (255,0,255), self.position, self.target.position, self.beam_width)
            if type(self.target) is list:
                for target in self.target:
                    # pygame.draw.line(window, (255,0,255), staff_position, target.position, self.beam_width)
                    self.draw_lightning(window, staff_position, target.position, 3, (255,0,255))
            else:
                # pygame.draw.line(window, (255,0,255), staff_position, self.target.position, self.beam_width)
                # testing lightning strike animation instead of straight line
                if self.level >= 4 and self.target.size > 1:
                    for nn in range(self.target.size):
                        self.draw_lightning(window, staff_position, self.target.position, 3, (255, 192, 0))
                else:
                    self.draw_lightning(window, staff_position, self.target.position, 3, (255,0,255))

    # Improve efficiency - cloud and multi-attack basically same
    def find_target(self, enemies):
        # Only place to call function - elsewhere just check self.cloud_attack
        if self._is_cloud_attack():
            tmp_target = []
            self.target = []
            for enemy in enemies:
                if self.in_range(enemy) and not enemy.reached_end:
                    tmp_target.append(enemy)
            if tmp_target:
                self.target = self.create_sublist(tmp_target, self.max_cloud_attacks)

            # why this - dont remember - not there for burger - could now set to None before
            # but why needed here and not for burger!
            if not self.target:
                self.target = None

        elif self._is_multi_attack():
            tmp_target = []
            self.target = []
            for enemy in enemies:
                if self.in_range(enemy) and not enemy.reached_end:
                    tmp_target.append(enemy)
            if tmp_target:
                self.target = self.create_sublist(tmp_target, self.max_attacks)
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
                    if self.cloud_type == 2:
                        multiplier += 1
                    score += target.take_damage(self.damage * multiplier)
            else:
                #For lev 4 special power attack against size 2/3 enemies.
                multiplier = 1
                if self.level >= 4:
                    multiplier = self.target.size
                score = self.target.take_damage(self.damage*multiplier)
            self.reset_attack_timer()
            self.is_attacking = True
        else:
            self.is_attacking = False
        return score

    # TODO can now use burger algorithm to attach >2 - check if this fumc is different
    # And also may be same as cloud but for animation.
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

    # Also could be generic to deal with lists - is this used for wizard - check.
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


# Level names: Big Blobs (or Splatter), Toxic, Toxic Storm (or Toxic Deluge/Tsunami/drench/barrage or similar)
class GlueGunner(Tower):

    price = 80
    name = 'Glue Gunner'
    image = gluegun_img
    range = 100
    max_level = 4

    def __init__(self, position):
        super().__init__(position)
        self.range =  GlueGunner.range
        self.attack_speed = 40
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
            self.attack_speed = 32
            self.range =  110
            self.image = gluegun2_img
            self.cost += self.upgrade_costs[0]
            self.glue_layers = 3
            self.beam_width = 9
            self.max_attacks = 3
            self.slow_factor = [0.4, 0.75, 0.9]
            self.upgrade_name = "Toxic Glue"

        if self.level == 3:
            self.attack_speed = 28
            self.image = gluegun3_img
            self.cost += self.upgrade_costs[1]
            self.slow_factor = [0.4, 0.7, 0.8]
            self.beam_width = 10
            # try colors - want to show up on green enemies
            self.glue_color = (124, 252, 0) # (15, 255, 80)
            self.toxic_time = 150
            self.max_toxic_big_reattacks = 1
            self.max_toxic_giant_reattacks = 2
            self.upgrade_name = "Toxic Storm"
            self.attack_tower = True

        if self.level == 4:
            self.attack_speed = 20
            self.range =  120
            self.image = gluegun4_img
            self.cost += self.upgrade_costs[2]
            self.slow_factor = [0.4, 0.5, 0.7]
            self.beam_width = 12
            # try colors - want to show up on green enemies
            self.glue_color = (124, 252, 0) # (15, 255, 80)
            self.toxic_time = 60 # 75
            self.glue_layers = 4
            self.max_attacks = 6
            self.max_toxic_big_reattacks = 2  # Repeatedly attack same enemy - takes toxic damage for each
            self.max_toxic_giant_reattacks = 5
            self.attack_tower = True

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


    # Shoot slower and hit multiple targets - closest - not spread
    # could avoid some duplication here
    def find_target(self, enemies):
        self.target = []
        count = 0

        if not enemies:
            self.target = None

        for enemy in enemies:
            if self.level >= 3 and self.in_range(enemy) and self.is_visible(enemy) and not enemy.reached_end and self.can_I_reglue(enemy):
                count += 1  # TODO this updates whether same enemy or different...
                self.target.append(enemy)
                enemy.toxic_attacks += 1
                if count >= self.max_attacks:
                    break
            elif self.in_range(enemy) and self.is_visible(enemy) and not enemy.reached_end and not enemy.glued:
                count += 1
                self.target.append(enemy)
                if count >= self.max_attacks:
                    break

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
        # nozzle = self.get_nozzle_pos()
        nozzle = self.position
        for target in self.target:
            pygame.draw.line(window, self.glue_color, nozzle, target.position, self.beam_width)

    # TODO - work out how more than one lev 4 toxic glue gunner combine - can they both attack
    # prob should be so they can both attack either no. times or until so many glue strikes on big target...
    # slow - currently not quite right - they both attack but only one claims the toxic hits!!!!
    # cos enemy has only one attribute toxic_glued_by - but really needs one for each hit!
    # Need an obj or list of dictionaries to do this. Not sorting this out right now.
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

# Maybe the Demons need more than ghost sight - 3rd level wizard or 3rd level totem.
class Totem(Tower):

    price = 200
    name = 'Totem'
    image = totem_img
    in_game_image = totem_img_ingame
    range = 100
    max_level = 4
    footprint = (60,70)

    def __init__(self, position):
        super().__init__(position)
        self.range =  Totem.range
        self.cost = Totem.price
        self.image = Totem.in_game_image
        self.level = 1
        self.upgrade_costs = [250, 500, 1000]
        self.upgrade_name = "Ghost Sight"
        self.attack_tower = False
        self.range_boost = 1.10

    def level_up(self):
        self.level +=1
        if self.level == 2:
            self.image = totem2_img
            self.cost += self.upgrade_costs[0]
            self.range =  110
            self.upgrade_name = "Arcane Energy"  # For now.
            self.range_boost = 1.15
        if self.level == 3:
            self.image = totem3_img
            self.cost += self.upgrade_costs[1]
            self.upgrade_name = "Eye of Moloch"
            self.range_boost = 1.15
        if self.level == 4:
            self.range =  120
            self.image = totem4_img
            self.cost += self.upgrade_costs[2]
            self.attack_tower = True
            self.attack_speed = 3
            self.range_boost = 1.20

    def find_target(self, enemies):
        self.target = None
        for enemy in enemies:
            if enemy.size >= 3 and not enemy.reached_end:
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
            self.is_attacking = True
        #else:
            #self.is_attacking = False
        return score

    def update(self, enemies):
        if self.level < 4:
            return 0
        score = 0
        self.attack_timer -= 1
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
            return (self.position[0]-6, self.position[1]-25), (self.position[0]+8, self.position[1]-25)
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
        return distance <= self.current_range()

    # Currently totem mods dont stack - but more powerful one in radius should take effect.
    def boost(self, tower):
        if tower.__class__.name == "Totem":
            # dont boost totems - including self
            return
        # Not changing range for now.
        tower.range_mod = self.range_boost  # should do attack_boost in same way.
        if self.level >= 1:
            tower.speed_mod = 0.9
        if self.level >= 2:
            tower.see_ghosts = True
        if self.level >= 3:
            tower.speed_mod = 0.75 # while addin nothing else - boost a bit
        if self.level >= 4:
            tower.speed_mod = 0.60 # while addin nothing else - boost a bit


class Cannon(Tower):

    price = 200
    name = 'Cannon'
    image = cannon_img
    range = 100
    max_level = 1
    footprint = (50,50)


    # Does projectile just go in direct target was when launch - or does it continue
    # to move towards target with each step (homing missile).
    def __init__(self, position):
        super().__init__(position)
        self.range =  Cannon.range
        self.cost = Cannon.price
        self.image = Cannon.image
        self.level = 1
        #self.upgrade_costs = [250, 500, 1000]
        #self.upgrade_name = "Ghost Sight"
        #self.attack_tower = False

    def attack(self):
        score = 0
        if self.target and self.attack_timer <= 0:
            self.attack_count += 1
            #score = self.target.take_damage(self.damage)
            score = -1  # tell it to release a projectile
            self.reset_attack_timer()
            self.is_attacking = True
        else:
            self.is_attacking = False
        return score

    def update(self, enemies):
        score = 0
        self.attack_timer -= 1
        if self.attack_timer <= 0:
            self.find_target(enemies)
            score = self.attack()
            self.total_score += score
        else:
            self.is_attacking = False
        # need to return more though - direction for projectile to move in.
        return score

    def get_projectile(self):
        projectile = CannonBall(self)
        return projectile


# Prob make projectile class - diff types and levels of projectile will be inherited.
class CannonBall(Tower):
    def __init__(self, tower):
        super().__init__(tower.position)
        self.launcher = tower
        self.speed = 8
        #self.speed = 4  # testing
        self.target_pos = tower.target.position  # position when shoot
        self.active = True
        self.max_attacks = 5
        print('new cannonball')


    def find_target(self, enemies):
        # Only place to call function - after just check self.cloud_attack
        tmp_target = []
        self.target = []
        for enemy in enemies:
            if self.in_range(enemy) and self.is_visible(enemy) and not enemy.reached_end:
                tmp_target.append(enemy)
        if tmp_target:
            self.target = self.create_sublist(tmp_target, self.max_attacks)


    def update(self, enemies):
    # from enemy
    #def move(self):
        # Move towards the next point in the path
        dx, dy = self.target_pos[0] - self.position[0], self.target_pos[1] - self.position[1]
        distance = (dx**2 + dy**2)**0.5
        print(f"{distance=} to {self.target_pos}")
        if distance > self.speed:
            dx, dy = dx / distance * self.speed, dy / distance * self.speed
        self.position = (self.position[0] + dx, self.position[1] + dy)
        print(f"new position {self.position}")

        # Check if the enemy has reached the target position
        if abs(self.position[0] - self.target_pos[0]) < self.speed and abs(self.position[1] - self.target_pos[1]) < self.speed:
            # This means blows up where original target was  but might want to hit
            # whenever cross path with enemy
            # an alternative  - dont blow up and more like you know death ball
            print(f"blowing up at {self.position}")
            self.find_target(enemies)
            score = self.attack()
            self.total_score += score
            #else:
                #self.is_attacking = False
            self.active = False  # if dont remove they stop on paths and look like mines
            return score
        return 0

    def draw(self, window):
        print('drawing it', self.position)
        x = self.position[0]
        y = self.position[1]
        pygame.draw.circle(window, (0,0,0), (int(x), int(y)), 20)

    #from burger
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
                    score += target.take_damage(self.damage * multiplier)
            else:
                # dont think ever here
                multiplier = self.target.size  # Do more damage to big enemies to simulate multiple projectiles hitting
                #print('single', multiplier)
                score = self.target.take_damage(self.damage * multiplier)
            self.reset_attack_timer()
            self.is_attacking = True  # Set to True when attacking
        else:
            self.is_attacking = False  # Set to False otherwise
        return score

tower_types = [Fighter, Burger, GlueGunner, Wizard, Totem, Cannon]





