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
wizard3_img = pygame.transform.scale(wizard3_img, (60, 60))
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
cannon_img_ingame = pygame.transform.scale(cannon_img, (70, 70))
cannon2_img = pygame.image.load('images/cannon2.png')
cannon2_img = pygame.transform.scale(cannon2_img, (70, 70))
cannon3_img = pygame.image.load('images/cannon3.png')
cannon3_img = pygame.transform.scale(cannon3_img, (75, 75))
cannon4_img = pygame.image.load('images/cannon4.png')
cannon4_img = pygame.transform.scale(cannon4_img, (80, 80))


#alt to black circle
cannonball_img = pygame.image.load('images/cannonball.png')
cannonball1_img = pygame.transform.scale(cannonball_img, (25, 25))
cannonball2_img = pygame.transform.scale(cannonball_img, (32, 32))
cannonball3_img = pygame.transform.scale(cannonball_img, (38, 38))
cannonball4_img = pygame.transform.scale(cannonball_img, (45, 45))

explosion_img = pygame.image.load('images/explosion.png')
explosion1_img = pygame.transform.scale(explosion_img, (80, 80))
explosion2_img = pygame.transform.scale(explosion_img, (90, 90))
explosion3_img = pygame.transform.scale(explosion_img, (100, 100))
explosion4_img = pygame.transform.scale(explosion_img, (110, 110))


ninja_img = pygame.image.load('images/ninja.png')
ninja_img = pygame.transform.scale(ninja_img, (50, 50))

def line_intersects_rect(p1, p2, rect):
    """
    Check if a line segment intersects a rectangle.

    Args:
    p1, p2 (tuple): Points representing the line segment (x1, y1), (x2, y2).
    rect (tuple): The rectangle (x, y, width, height).

    Returns:
    bool: True if the line intersects the rectangle, False otherwise.
    """
    rect_x, rect_y, rect_w, rect_h = rect
    rect_top_left = (rect_x, rect_y)
    rect_top_right = (rect_x + rect_w, rect_y)
    rect_bottom_left = (rect_x, rect_y + rect_h)
    rect_bottom_right = (rect_x + rect_w, rect_y + rect_h)

    def ccw(A, B, C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    def intersect(A, B, C, D):
        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

    # Check if the line intersects any of the sides of the rectangle
    return (intersect(p1, p2, rect_top_left, rect_top_right) or
            intersect(p1, p2, rect_top_right, rect_bottom_right) or
            intersect(p1, p2, rect_bottom_right, rect_bottom_left) or
            intersect(p1, p2, rect_bottom_left, rect_top_left))

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
        self.image = self.__class__.image  # Might not need to put this in inherited towers now.
        self.target = None


    # For pickling override __getstate__
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['image']  # Remove the non-picklable attribute
        del state['target']
        #self.target = None  # can I do this rather than deleting
        return state

    def __setstate__(self, state):
        self.__dict__ = state
        self.image = self.__class__.image  # Restore the non-picklable attribute
        self.target = None
        self.load_images()

    def load_images(self):
        pass

    def current_range(self):
        return self.range * self.range_mod

    def level_up(self):
        pass

    def show_viz_persis(self, window):
        pass

    def reset_attack_timer(self):
        self.attack_timer = max(int(self.attack_speed * self.speed_mod), 1)

    def is_visible(self, enemy, gmap):
        if enemy.invis and not self.see_ghosts:
            return False

        barriers = gmap.barriers()
        for barrier in barriers:
            if line_intersects_rect(self.position, enemy.position, barrier):
                return False
        return True

    # Goes through enemies - finds first (could find strongest etc...)
    # Note that enemy order is order came on to screen but may not be at the front at any point in time!
    def find_target(self, enemies, gmap):
        for enemy in enemies:
            if self.in_range(enemy) and self.is_visible(enemy, gmap) and not enemy.reached_end:
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
        return score, False  # 2nd is whether to spawn a projectile

    def update(self, enemies, gmap):
        score = 0
        spawn = False
        self.attack_timer -= 1
        if self.attack_timer <= 0:
            self.find_target(enemies, gmap)
            score, spawn = self.attack()
            self.total_score += score
        else:
            self.is_attacking = False
        return score, spawn

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

    def load_images(self):
        if self.level == 2:
            self.image = fighter2_img
        elif self.level == 3:
            self.image = fighter3_img
        elif self.level == 4:
            self.image = fighter4_img

    def level_up(self):
        self.level +=1
        if self.level == 2:
            self.attack_speed = 27  # lower is better currently
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
        self.attack_speed = 65
        self.damage = 1
        self.cost = Burger.price
        #self.image = Burger.image  # all of these can be done in base class: self.thing = self.__class__.thing
        self.level = 1
        self.max_attacks = 4
        self.upgrade_costs = [85, 220, 680] # , 1200]
        # range_mod cant be used here - so would have to update when update range_mod
        self.splat_img = pygame.transform.scale(splat_img, (self.range+60, self.range+60))
        self.upgrade_name = "With cheese"

    def load_images(self):
        if self.level == 2:
            self.image = burger2_img
        elif self.level == 3:
            self.image = burger3_img
        elif self.level == 4:
            self.image = burger4_img

    def level_up(self):
        self.level +=1
        if self.level == 2:
            self.attack_speed = 50  # lower is better currently
            self.range =  70
            self.image = burger2_img
            self.max_attacks = 6
            self.cost += self.upgrade_costs[0]
            self.splat_img = pygame.transform.scale(splat_img, (self.range+60, self.range+60))
            self.upgrade_name = "Extra Spicy"
        if self.level == 3:
            self.attack_speed = 25
            self.range =  75
            self.image = burger3_img
            self.max_attacks = 8
            self.cost += self.upgrade_costs[1]
            self.splat_img = pygame.transform.scale(splat_img, (self.range+60, self.range+60))
            self.upgrade_name = "Whopper"
        if self.level == 4:
            self.attack_speed = 10 # 16 (if damage 2)
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

    # For pickling override __getstate__
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['image']
        del state['splat_img']  # Remove the non-picklable attribute
        del state['target']
        #print('im here')
        for k,v in state.items():
            if isinstance(v, pygame.Surface):
                print(k)
        return state

    def __setstate__(self, state):
        self.__dict__ = state
        self.image = self.__class__.image  # Restore the non-picklable attribute
        self.load_images()
        self.splat_img = pygame.transform.scale(splat_img, (self.range+60, self.range+60))
        self.target = None

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

    def find_target(self, enemies, gmap):
        # Only place to call function - after just check self.cloud_attack
        tmp_target = []
        self.target = []
        for enemy in enemies:
            if self.in_range(enemy) and self.is_visible(enemy, gmap) and not enemy.reached_end:
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
# Why did a make default cloud attack 2 damage - thats crazy.
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
        self.attack_speed = 50  # made a bit faster - but maybe reduce cloud freq.
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

    def load_images(self):
        if self.level == 2:
            self.image = wizard2_img
        elif self.level == 3:
            self.image = wizard3_img
        elif self.level == 4:
            self.image = wizard4_img

    def draw(self, window, enemies=None):
        """Dont rotate wizard"""
        new_rect = self.image.get_rect(center=self.image.get_rect(center=self.position).center)
        self.general_draw(window, self.image, new_rect)

    # thinking at first cloud should do 1 damage - maybe hit more though.
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
            self.attack_speed = 12
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
    def find_target(self, enemies, gmap):
        # Only place to call function - elsewhere just check self.cloud_attack
        if self._is_cloud_attack():
            tmp_target = []
            self.target = []
            for enemy in enemies:
                if self.in_range(enemy) and self.is_visible(enemy, gmap) and not enemy.reached_end:
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
                if self.in_range(enemy) and self.is_visible(enemy, gmap) and not enemy.reached_end:
                    tmp_target.append(enemy)
            if tmp_target:
                self.target = self.create_sublist(tmp_target, self.max_attacks)
        else:
            super().find_target(enemies, gmap)

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
        #self.image = GlueGunner.image
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

    def load_images(self):
        if self.level == 2:
            self.image = gluegun2_img
        elif self.level == 3:
            self.image = gluegun3_img
        elif self.level == 4:
            self.image = gluegun4_img

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
            self.slow_factor = [0.4, 0.7, 0.9]
            self.upgrade_name = "Toxic Glue"

        if self.level == 3:
            self.attack_speed = 28
            self.image = gluegun3_img
            self.cost += self.upgrade_costs[1]
            self.slow_factor = [0.4, 0.6, 0.8]
            self.beam_width = 10
            self.glue_layers = 4
            # try colors - want to show up on green enemies
            self.glue_color = (124, 252, 0) # (15, 255, 80)
            self.toxic_time = 150
            self.max_toxic_big_reattacks = 1
            self.max_toxic_giant_reattacks = 2
            self.upgrade_name = "Toxic Storm"
            self.attack_tower = True

        if self.level == 4:
            self.attack_speed = 12
            self.range =  120
            self.image = gluegun4_img
            self.cost += self.upgrade_costs[2]
            self.slow_factor = [0.3, 0.4, 0.7]
            self.beam_width = 12
            # try colors - want to show up on green enemies
            self.glue_color = (124, 252, 0) # (15, 255, 80)
            self.toxic_time = 60 # 75
            self.glue_layers = 6
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
    def find_target(self, enemies, gmap):
        self.target = []
        count = 0

        if not enemies:
            self.target = None

        for enemy in enemies:
            if self.level >= 3 and self.in_range(enemy) and self.is_visible(enemy, gmap) and not enemy.reached_end and self.can_I_reglue(enemy):
                count += 1  # TODO this updates whether same enemy or different...
                self.target.append(enemy)
                enemy.toxic_attacks += 1
                if count >= self.max_attacks:
                    break
            elif self.in_range(enemy) and self.is_visible(enemy, gmap) and not enemy.reached_end and not enemy.glued:
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

    def load_images(self):
        if self.level == 1:
            self.image = self.__class__.in_game_image
        if self.level == 2:
            self.image = totem2_img
        elif self.level == 3:
            self.image = totem3_img
        elif self.level == 4:
            self.image = totem4_img

    def level_up(self):
        self.level +=1
        if self.level == 2:
            self.image = totem2_img
            self.cost += self.upgrade_costs[0]
            self.range =  110
            self.upgrade_name = "Arcane Energy"  # For now.
            self.range_boost = 1.15
        if self.level == 3:
            self.range =  120
            self.image = totem3_img
            self.cost += self.upgrade_costs[1]
            self.upgrade_name = "Eye of Moloch"
            self.range_boost = 1.15
        if self.level == 4:
            self.range =  130
            self.image = totem4_img
            self.cost += self.upgrade_costs[2]
            self.attack_tower = True
            self.attack_speed = 2
            self.range_boost = 1.20

    def find_target(self, enemies, gmap):
        self.target = None
        for enemy in enemies:
            # No check vis for now - I think he should see everything.
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
        return score, False

    def update(self, enemies, gmap):
        spawn = False
        if self.level < 4:
            return 0, spawn
        score = 0
        self.attack_timer -= 1
        self.find_target(enemies, gmap)
        score, spawn = self.attack()
        self.total_score += score
        #else:
            #self.is_attacking = False
        return score, spawn

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

    def draw(self, window, enemies=None):
        """Dont rotate toetem"""
        new_rect = self.image.get_rect(center=self.image.get_rect(center=self.position).center)
        self.general_draw(window, self.image, new_rect)

        if enemies is None:
            return

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
            tower.speed_mod = 0.65 # while addin nothing else - boost a bit


# some ideas names
#
# Heavy Cannon (or Gun if not room) / Bombard
# Giant Cannon  / Big Bertha / Mons Meg
# Doomsday (Gun) / Thor
class Cannon(Tower):

    price = 150
    name = 'Cannon'
    image = cannon_img
    in_game_image = cannon_img_ingame
    range = 120
    max_level = 4
    footprint = (70,70)  # May make bigger

    # Does projectile just go in direct target was when launch - or does it continue
    # to move towards target with each step (homing missile).
    def __init__(self, position):
        super().__init__(position)
        self.range =  Cannon.range
        self.cost = Cannon.price
        self.image = Cannon.in_game_image
        self.level = 1
        self.attack_speed = 65
        self.upgrade_costs = [300, 750, 2000]
        self.glow_radius = 10
        self.glow_time = 5
        self.upgrade_name = "Heavy Gun"

    def load_images(self):
        if self.level == 1:
            self.image = self.__class__.in_game_image
        if self.level == 2:
            self.image = cannon2_img
        elif self.level == 3:
            self.image = cannon3_img
        elif self.level == 4:
            self.image = cannon4_img


    def level_up(self):
        self.level +=1
        if self.level == 2:
            self.attack_speed = 45
            self.image = cannon2_img
            #self.max_attacks = 7
            self.cost += self.upgrade_costs[0]
            self.upgrade_name = "Bombard"
            self.range = 130
            self.glow_radius = 16
        if self.level == 3:
            self.image = cannon3_img
            self.attack_speed = 33
            self.range = 140
            #self.image = cannon_img
            #self.max_attacks = 10
            self.cost += self.upgrade_costs[1]
            self.upgrade_name = "Doomsday"
            self.glow_radius = 20
        if self.level == 4:
            self.image = cannon4_img
            self.attack_speed = 22
            self.range = 150
            #self.image = cannon_img
            #self.max_attacks = 10
            self.cost += self.upgrade_costs[2]
            #self.upgrade_name = "Extra Spicy"
            self.glow_radius = 24 # 16

    def attack(self):
        score = 0
        spawn = False
        if self.target and self.attack_timer <= 0:
            self.attack_count += 1
            #score = self.target.take_damage(self.damage)
            # old -1  # tell it to release a projectile
            spawn = True
            self.reset_attack_timer()
            self.is_attacking = True
        else:
            self.is_attacking = False
        return score, spawn

    def update(self, enemies, gmap):
        score = 0
        spawn = False
        self.attack_timer -= 1
        if self.attack_timer <= 0:
            self.find_target(enemies, gmap)
            score, spawn = self.attack()
            #self.total_score += score
        else:
            self.is_attacking = False
        return score, spawn

    def get_projectile(self):
        projectile = CannonBall(self)
        return projectile


    def _get_start_nozzle_pos(self):
        if self.level == 1:
            return (self.position[0], self.position[1]+20)
        if self.level == 2:
            return (self.position[0], self.position[1]+23)
        elif self.level == 3:
            return (self.position[0], self.position[1]+21)
        elif self.level == 4:
            return (self.position[0], self.position[1]+24)

    def rotate_point(self, origin, point, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        Args:
        origin (tuple): The rotation center (x, y).
        point (tuple): The point to rotate (x, y).
        angle (float): The rotation angle in degrees.

        Returns:
        tuple: The new position of the point after rotation.
        """
        # Convert angle to radians
        angle_rad = math.radians(-angle)

        # Shift the point to the origin
        ox, oy = origin
        px, py = point

        # Rotate and shift back
        qx = ox + math.cos(angle_rad) * (px - ox) - math.sin(angle_rad) * (py - oy)
        qy = oy + math.sin(angle_rad) * (px - ox) + math.cos(angle_rad) * (py - oy)
        return qx, qy


    def _get_nozzle_pos(self):
        """
        Calculate the nozzle position of a rotating cannon.

        Args:
        cannon_center (tuple): The center position (x, y) of the cannon.
        cannon_angle (float): The current rotation angle of the cannon in degrees.
        nozzle_offset_y (int): The vertical offset of the nozzle from the cannon center.

        Returns:
        tuple: The position of the nozzle after rotation.
        """
        # Original position of the nozzle (assuming it starts at x, y - 20)
        nozzle_position = self._get_start_nozzle_pos()

        # Rotate the nozzle position around the cannon center
        return self.rotate_point(self.position, nozzle_position, self.current_angle)


    def _nozzle_glow(self, window, glow_radius, col, c_alpha, noz_pos):
        # translucent - prob better
        nozzle_glow = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(nozzle_glow, (col[0], col[1], col[2], c_alpha), (glow_radius,glow_radius), glow_radius)
        glow_rect = nozzle_glow.get_rect(center=noz_pos)
        window.blit(nozzle_glow, glow_rect)
        # opaque
        #pygame.draw.circle(window, col, noz_pos, glow_radius)


    def show_viz_persist(self, window):
        self._animate_nozzle(window)
        if self.viz_persist > 0:
            self.viz_persist -= 1

    def _animate_nozzle(self, window):
        noz_pos = self._get_nozzle_pos()
        time_glowed = self.glow_time - self.viz_persist
        glow_color = (255, 192, 0) # (220, 20, 60)
        glow_radius = self.glow_radius - 2*time_glowed
        c_alpha = max(250 - 20*time_glowed, 0)  # 150  # higher is more opaque
        self._nozzle_glow(window, glow_radius, glow_color, c_alpha, noz_pos)

    def attack_animate(self, window):
        # Would like to make nozzle glow as fire, but again need to deal with rotation.
        self.viz_persist = self.glow_time
        self._animate_nozzle(window)
        self.viz_persist -= 1

    def get_target_angle(self):
        if not self.target:
            return 0
        if type(self.target) is list:
            target = self.target[0]
        else:
            target = self.target
        dx = target.position[0] - self.position[0]
        dy = target.position[1] - self.position[1]
        # prevent having to recalculate for nozzle glow
        self.current_angle = math.degrees(math.atan2(-dy, dx)) + 90
        return self.current_angle


# Prob make projectile class - diff types and levels of projectile will be inherited.
class CannonBall(Tower):

    image = cannonball1_img

    def __init__(self, tower):
        super().__init__(tower.position)
        self.launcher = tower
        self.speed = 8
        self.target_pos = tower.target.position  # position when shoot
        self.active = True
        self.max_attacks = 4
        self.damage = 2
        self.image = CannonBall.image
        self.range = 50
        self.expl_image = explosion1_img
        if self.launcher.level == 2:
            self.speed = 10
            self.damage = 4
            self.max_attacks = 6
            self.image = cannonball2_img
            self.range = 60
            self.expl_image = explosion2_img
        if self.launcher.level == 3:
            # maybe add homing missiles
            self.speed = 12
            self.damage = 7
            self.max_attacks = 8
            self.image = cannonball3_img
            self.range = 70
            self.expl_image = explosion3_img
        if self.launcher.level == 4:
            # maybe add homing missiles
            self.speed = 15
            self.damage = 12
            self.max_attacks = 18
            self.image = cannonball4_img
            self.range = 90
            self.expl_image = explosion4_img  # Add fourth and prob viz perist

    def find_target(self, enemies, gmap):
        # Only place to call function - after just check self.cloud_attack
        tmp_target = []
        self.target = []
        self.see_ghosts = self.launcher.see_ghosts
        for enemy in enemies:
            if self.in_range(enemy) and self.is_visible(enemy, gmap) and not enemy.reached_end:
                tmp_target.append(enemy)
        if tmp_target:
            self.target = self.create_sublist(tmp_target, self.max_attacks)
            #print(f"{len(self.target)=}")

    def update(self, enemies, gmap):
        dx, dy = self.target_pos[0] - self.position[0], self.target_pos[1] - self.position[1]
        distance = (dx**2 + dy**2)**0.5
        #print(f"{distance=} to {self.target_pos}")
        if distance > self.speed:
            dx, dy = dx / distance * self.speed, dy / distance * self.speed
        self.position = (self.position[0] + dx, self.position[1] + dy)
        # Check if the enemy has reached the target position
        if abs(self.position[0] - self.target_pos[0]) < self.speed and abs(self.position[1] - self.target_pos[1]) < self.speed:
            #print(f"blowing up at {self.position}")
            self.find_target(enemies, gmap)
            score, _ = self.attack()
            self.launcher.total_score += score
            self.active = False  # if dont remove they stop on paths and look like mines
            return score, False
        return 0, False

    def draw(self, window, enemies=None):
        x = self.position[0]
        y = self.position[1]
        if self.active:
            image_rect = self.image.get_rect(center=self.position)
            window.blit(self.image, image_rect.topleft)

    def attack_animate(self, window):
        if not self.active:
            explosion_rect = self.expl_image.get_rect(center=self.position)
            window.blit(self.expl_image, explosion_rect)

    #modified from burger
    def attack(self):
        score = 0
        if self.target and self.attack_timer <= 0:
            # If using IF this could be in generic one
            self.attack_count += 1
            if type(self.target) is list:
                for target in self.target:
                    # Do more damage to big enemies to simulate multiple projectiles hitting
                    multiplier = target.size
                    #print(f"Damage: {self.damage * multiplier}")
                    score += target.take_damage(self.damage * multiplier)
            else:
                # dont think ever here
                multiplier = self.target.size  # Do more damage to big enemies to simulate multiple projectiles hitting
                score = self.target.take_damage(self.damage * multiplier)
            self.reset_attack_timer()
            self.is_attacking = True  # Set to True when attacking
        else:
            self.is_attacking = False  # Set to False otherwise
        return score, False


# yeah a bit of work to do here
# initial attack will be in his range and pick first target - that will decide path
# maybe i can get path from enemy - get path and path_index of enemy.
# then once hit first target (ninja hit) the shurken object will take over and travel in reverse along the path
# tried doing this very tired so made a mess so far.
# what if projectile misses first target? Should it be instant to first target?
class Ninja(Tower):

    price = 10
    name = 'Ninja'
    image = ninja_img
    #in_game_image = cannon_img_ingame
    range = 80
    max_level = 1
    footprint = (40,50)  # May make bigger

    # Does projectile just go in direct target was when launch - or does it continue
    # to move towards target with each step (homing missile).
    def __init__(self, position):
        super().__init__(position)
        self.range =  Ninja.range
        self.cost = Ninja.price
        self.image = Ninja.image
        self.level = 1
        self.attack_speed = 60
        self.upgrade_costs = [300, 750, 2000]
        #self.glow_radius = 10
        #self.glow_time = 5
        #self.upgrade_name = "Heavy Gun"

    def attack(self):
        score = 0
        spawn = False
        if self.target and self.attack_timer <= 0:  # why attack_timer here and in update?
            self.attack_count += 1
            # hmm the score -1 method is  aproblem if want ordinary hit - then releaes projectile.
            # alt is we release projectile - but when gets to orig target point - the target is hit
            # even if moved on - but it could be killed by something else by then!

            # Hits first then spawns shuriken from there
            score = self.target.take_damage(self.damage)
            #score = -1  # tell it to release a projectile
            spawn = True
            self.reset_attack_timer()
            self.is_attacking = True
        else:
            self.is_attacking = False
        return score, spawn

    def update(self, enemies, gmap):
        score = 0
        spawn = False
        self.attack_timer -= 1
        if self.attack_timer <= 0:
            self.find_target(enemies, gmap)
            score, spawn = self.attack()
            #self.total_score += score
        else:
            self.is_attacking = False
        return score, spawn

    def get_projectile(self):
        projectile = Shuriken(self)
        #projectile = CannonBall(self)
        return projectile

    def draw(self, window, enemies=None):
        """Dont rotate burger"""
        new_rect = self.image.get_rect(center=self.image.get_rect(center=self.position).center)
        self.general_draw(window, self.image, new_rect)


#class Shuriken(CannonBall):  # tmp inheritence
# Prob make projectile class - diff types and levels of projectile will be inherited.
# looks like cannonball for now - not most copy/pasted from cannonball for now but updating find_target/attack
# forgot how projectiles move
class Shuriken(Tower):

    image = cannonball1_img

    def __init__(self, tower):
        super().__init__(tower.target.position)
        self.launcher = tower
        self.speed = 8
        self.target_pos = tower.target.position  # position when shoot
        self.path = tower.target.path
        self.path_index = tower.target.path_index
        #print(f"initial {self.path_index}")
        self.distance = 0
        self.active = True
        self.max_attacks = 4
        self.damage = 1
        self.image = CannonBall.image
        self.range = 1
        self.expl_image = explosion1_img
        if self.launcher.level == 2:
            self.speed = 10
            self.damage = 4
            self.max_attacks = 6
            self.image = cannonball2_img
            self.range = 60
            self.expl_image = explosion2_img
        if self.launcher.level == 3:
            # maybe add homing missiles
            self.speed = 12
            self.damage = 7
            self.max_attacks = 8
            self.image = cannonball3_img
            self.range = 70
            self.expl_image = explosion3_img
        if self.launcher.level == 4:
            # maybe add homing missiles
            self.speed = 15
            self.damage = 12
            self.max_attacks = 18
            self.image = cannonball4_img
            self.range = 90
            self.expl_image = explosion4_img  # Add fourth and prob viz perist

    #def find_target(self, enemies, gmap):
        ## Only place to call function - after just check self.cloud_attack
        ##self.target = enemies # put all in here.
        ##tmp_target = []
        #self.target = []
        ##self.see_ghosts = self.launcher.see_ghosts
        #for enemy in enemies:
            #if self.is_visible(enemy, gmap) and not enemy.reached_end:
                #self.target.append(enemy)
            #if self.in_range(enemy) and self.is_visible(enemy, gmap) and not enemy.reached_end:
                #tmp_target.append(enemy)
        #if tmp_target:
            #self.target = self.create_sublist(tmp_target, self.max_attacks)
            #print(f"{len(self.target)=}")

    #def update(self, enemies, gmap):
        #dx, dy = self.target_pos[0] - self.position[0], self.target_pos[1] - self.position[1]
        #distance = (dx**2 + dy**2)**0.5
        ##print(f"{distance=} to {self.target_pos}")
        #if distance > self.speed:
            #dx, dy = dx / distance * self.speed, dy / distance * self.speed
        #self.position = (self.position[0] + dx, self.position[1] + dy)
        ## Check if the enemy has reached the target position
        #if abs(self.position[0] - self.target_pos[0]) < self.speed and abs(self.position[1] - self.target_pos[1]) < self.speed:
            ##print(f"blowing up at {self.position}")
            #self.find_target(enemies, gmap)
            #score = self.attack()
            #self.launcher.total_score += score
            #self.active = False  # if dont remove they stop on paths and look like mines
            #return score
        #return 0



# reverse of enemy movement
# enemy movement function

    #def move(self): #reversing
    def update(self, enemies, gmap):
        # Move towards the next point in the path
        spawn = False
        if self.path_index >= 0:
            print(f"{self.path_index=}")
            target_pos = self.path[self.path_index]  # for backwards move (rather than +1)
            dx, dy = self.position[0] - target_pos[0], self.position[1] - target_pos[1]
            distance = (dx**2 + dy**2)**0.5
            if distance > self.speed:
                dx, dy = dx / distance * self.speed, dy / distance * self.speed
            self.position = (self.position[0] - dx, self.position[1] - dy)

            # add for hit target - here or end?
            #if abs(self.position[0] - self.target_pos[0]) < self.speed and abs(self.position[1] - self.target_pos[1]) < self.speed:
                #self.find_target(enemies, gmap)
                #score, spawn = self.attack()
                #self.launcher.total_score += score
                ##self.active = False  # if dont remove they stop on paths and look like mines
                #return score, spawn

            # Check if the enemy has reached the target position
            if abs(self.position[0] - target_pos[0]) < self.speed and abs(self.position[1] - target_pos[1]) < self.speed:
                self.path_index -= 1

            self.distance += self.speed
            print(f"{self.distance=}")

        # Check if the enemy has reached the end of the path
        if self.path_index <  0:
            self.active = False  # if dont remove they stop on paths and look like mines
            #self.reached_end = True  # reached start

        #return score, spawn
        return 0, False # tmp - go to beginning of course without killing anything




    def draw(self, window, enemies=None):
        x = self.position[0]
        y = self.position[1]
        if self.active:
            image_rect = self.image.get_rect(center=self.position)
            window.blit(self.image, image_rect.topleft)

    def attack_animate(self, window):
        if not self.active:
            explosion_rect = self.expl_image.get_rect(center=self.position)
            window.blit(self.expl_image, explosion_rect)



    #def attack(self):
        #score = 0

        ## dont remember why find_target is separate from attack
        #if self.self.attack_timer > 0:
            #self.is_attacking = False
            #return score

        ## no this is going to be determined by initial range if do all at once....
        ##   want to do one at time no...
        #next_target = []
        #for enemy in self.target:
            #if self.in_range(enemy):  # CHECK - range of ninja or Shuriken - i think this is shuriken determined...
                #next_target.append(enemy)
                #if len(next_target) == self.max_attacks:
                    #break

        #if next_target:
            #self.attack_count += 1
            #score = self.target.take_damage(self.damage)
            #self.reset_attack_timer()
            #self.is_attacking = True
        #else:
            #self.is_attacking = False
        #return score

    #def attack(self):
        #score = 0
        #if self.target and self.attack_timer <= 0:
            ## If using IF this could be in generic one
            #self.attack_count += 1
            #if type(self.target) is list:
                #for target in self.target:
                    ## Do more damage to big enemies to simulate multiple projectiles hitting
                    #multiplier = target.size
                    ##print(f"Damage: {self.damage * multiplier}")
                    #score += target.take_damage(self.damage * multiplier)
            #else:
                ## dont think ever here
                #multiplier = self.target.size  # Do more damage to big enemies to simulate multiple projectiles hitting
                #score = self.target.take_damage(self.damage * multiplier)
            #self.reset_attack_timer()
            #self.is_attacking = True  # Set to True when attacking
        #else:
            #self.is_attacking = False  # Set to False otherwise
        #return score





tower_types = [Fighter, Burger, GlueGunner, Wizard, Cannon, Totem, Ninja]
