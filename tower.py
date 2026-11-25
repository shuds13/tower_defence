import math
import pygame
import random
import sounds
from enemy import make_goo, GOO_FILL, GOO_SHINE

fighter_img = pygame.image.load('images/tower1.png')
fighter_img = pygame.transform.scale(fighter_img, (50, 50))
fighter2_img = pygame.image.load('images/tower1_lev2.png')
fighter2_img = pygame.transform.scale(fighter2_img, (50, 50))
fighter3_img = pygame.image.load('images/tower1_lev3.png')
fighter3_img = pygame.transform.scale(fighter3_img, (55, 55))
fighter4_img = pygame.image.load('images/tower1_lev4.png')
fighter4_img = pygame.transform.scale(fighter4_img, (60, 60))
fighter5_img = pygame.image.load('images/tower1_lev5.png')  # placeholder art
fighter5_img = pygame.transform.scale(fighter5_img, (64, 64))

burger_img = pygame.image.load('images/burger.png')
burger_img = pygame.transform.scale(burger_img, (50, 50))
burger2_img = pygame.image.load('images/burger2.png')
burger2_img = pygame.transform.scale(burger2_img, (52, 52))
burger3_img = pygame.image.load('images/burger3.png')
burger3_img = pygame.transform.scale(burger3_img, (55, 55))
burger4_img = pygame.image.load('images/burger4.png')
burger4_img = pygame.transform.scale(burger4_img, (60, 60))
burger5_img = pygame.image.load('images/burger_king.png')  # trying the Burger King image (also used by the enemy)
burger5_img = pygame.transform.scale(burger5_img, (90, 90))  # image is narrow, so drawn larger to look bigger than the Whopper
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
gluegun5_img = pygame.image.load('images/glue_gun5.png')  # trial art
gluegun5_img = pygame.transform.smoothscale(gluegun5_img, (53, 75))

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
explosionMini_img = pygame.transform.scale(explosion_img, (50, 50))

ninja_img = pygame.image.load('images/ninja.png')
ninja_img = pygame.transform.scale(ninja_img, (50, 50))
ninja2_img = pygame.image.load('images/ninja2.png')
ninja2_img = pygame.transform.scale(ninja2_img, (50, 50))
ninja3_img = pygame.image.load('images/ninja3.png')
ninja3_img = pygame.transform.scale(ninja3_img, (50, 50))
ninja4_img = pygame.image.load('images/ninja4.png')
ninja4_img = pygame.transform.scale(ninja4_img, (50, 50))

shuriken_img = pygame.image.load('images/shuriken.png')
shuriken_img = pygame.transform.scale(shuriken_img, (25, 25))
shuriken_img2 = shuriken_img
shuriken_img3 = shuriken_img
shuriken_img4 = shuriken_img
shuriken_dark_img = pygame.image.load('images/shuriken_darkpath.png')
shuriken_dark_img = pygame.transform.scale(shuriken_dark_img, (25, 25))
shuriken_red_img = pygame.image.load('images/shuriken_red.png')
shuriken_red_img = pygame.transform.scale(shuriken_red_img, (30, 30))


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
    max_level = 1
    footprint = (50,50)  # for distance to place towers - this should not change for a tower (image size may)
    new_tower = False
    target_modes = ()  # Targeting options offered in the inset window (empty = no choice)
    target_mode = "first"  # class default also covers towers loaded from older saves
    unlock_game_levels = {}  # tower level -> first game level where that upgrade can be bought

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
        self.ghostsight = False  # can this character see ghosts unassisted
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
        state.pop('smother_cloud', None)  # cached glue image, redrawn on the next spray
        #self.target = None  # can I do this rather than deleting
        return state

    def __setstate__(self, state):
        self.__dict__ = state
        self.image = self.__class__.image  # Restore the non-picklable attribute
        self.target = None
        self.load_images()

    def load_images(self):
        pass

    def new_round(self):
        """Called before each round starts."""
        pass

    def next_level_taken(self, towers):
        """True if the next upgrade is tier 5 and another tower of this type already has it (one of each allowed)."""
        return self.level + 1 >= 5 and any(other is not self and type(other) is type(self) and other.level >= 5
                                           for other in towers)

    def max_level_at(self, game_level, map_crowned=False):
        """Highest tower level that can be reached on this game level (some upgrades unlock later).
        Once the map's crown has been earned, every upgrade is available on it."""
        top = self.__class__.max_level
        if map_crowned:
            return top
        while top > 1 and self.__class__.unlock_game_levels.get(top, 0) > game_level:
            top -= 1
        return top

    def current_range(self):
        return self.range * self.range_mod

    def level_up(self):
        pass

    def show_viz_persis(self, window):
        pass

    def reset_attack_timer(self):
        # Keep the fraction of a frame left over from this shot, so speed boosts give their exact
        # percentage on average (e.g. a 1.8 frame interval fires at gaps of 2,2,2,2,1).
        # A tower that was waiting with nothing to shoot carries nothing over, so it cannot save up shots.
        leftover = self.attack_timer if self.attack_timer > -1 else 0
        self.attack_timer = leftover + self.attack_speed * self.speed_mod

    def is_visible(self, enemy, gmap):
        if enemy.invis and not self.see_ghosts:
            return False

        barriers = gmap.barriers()
        for barrier in barriers:
            if line_intersects_rect(self.position, enemy.position, barrier):
                return False
        return True

    def can_target(self, enemy, gmap):
        return self.in_range(enemy) and self.is_visible(enemy, gmap) and not enemy.reached_end

    # Enemies are sorted front first (by distance travelled) each frame.
    def find_target(self, enemies, gmap):
        if self.target_mode == "first":
            self.target = next((enemy for enemy in enemies if self.can_target(enemy, gmap)), None)
            return
        candidates = [enemy for enemy in enemies if self.can_target(enemy, gmap)]
        if not candidates:
            self.target = None
        elif self.target_mode == "strong":
            # value includes what the enemy spawns on death; ties go to the one further along
            self.target = max(candidates, key=lambda enemy: enemy.value)
        elif self.target_mode == "last":
            self.target = candidates[-1]
        elif self.target_mode == "close":
            self.target = min(candidates, key=lambda enemy: (enemy.position[0] - self.position[0])**2 + (enemy.position[1] - self.position[1])**2)
        else:
            self.target = candidates[0]

    def next_target_mode(self):
        modes = self.__class__.target_modes
        self.target_mode = modes[(modes.index(self.target_mode) + 1) % len(modes)]

    def option_text(self):
        """Text for the small clickable option in the tower box, or None if there is no option."""
        if self.__class__.target_modes:
            return f"Target: {self.target_mode.capitalize()}  >"
        return None

    def next_option(self):
        self.next_target_mode()

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

    def draw(self, window, enemies=None, active=False):
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
    max_level = 5
    target_modes = ("first", "strong", "last", "close")
    unlock_game_levels = {5: 61}  # Nighthawk after the 60 main levels (or any level once the map is crowned)
    death_star_damage = {1: 4, 2: 7, 3: 9}  # level 5 damage per shot by enemy size
    idle_frames = 60  # frames since the level 5 beam last had a target (class default covers older saves)

    def __init__(self, position):
        super().__init__(position)
        self.range =  Fighter.range
        self.attack_speed = 40
        self.damage = 1
        self.cost = Fighter.price
        self.image = Fighter.image
        self.level = 1
        self.upgrade_costs = [40, 180, 400, 2500]
        self.beam_width = 5
        self.upgrade_name = "Rapid Fire"

    def __setstate__(self, state):
        super().__setstate__(state)
        # Fighters saved before level 5 existed
        if len(self.upgrade_costs) < 4:
            self.upgrade_costs.append(2500)
        if self.level == 4:
            self.upgrade_name = "Nighthawk"

    def load_images(self):
        if self.level == 2:
            self.image = fighter2_img
        elif self.level == 3:
            self.image = fighter3_img
        elif self.level == 4:
            self.image = fighter4_img
        elif self.level == 5:
            self.image = fighter5_img

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
            self.upgrade_name = "Nighthawk"
        if self.level == 5:
            # Stealth jet: faster, ghost sight, and a Death Star beam (both nose beams join into one)
            self.attack_speed = 2
            self.range = 150
            self.image = fighter5_img
            self.cost += self.upgrade_costs[3]
            self.ghostsight = True

    def new_round(self):
        self.idle_frames = 60  # so the power-up sound plays on the first shot of each round

    def update(self, enemies, gmap):
        result = super().update(enemies, gmap)
        if self.level >= 5:
            # Power-up sound when the beam starts firing after being idle for a second
            if self.is_attacking:
                if self.idle_frames >= 60:
                    sounds.play('nighthawk')
                self.idle_frames = 0
            elif self.target is None:
                self.idle_frames += 1
        return result

    def attack(self):
        if self.level < 5:
            return super().attack()
        score = 0
        if self.target and self.attack_timer <= 0:
            self.attack_count += 1
            # Death Star beam: more damage against bigger enemies
            score = self.target.take_damage(self.__class__.death_star_damage[self.target.size])
            self.reset_attack_timer()
            self.is_attacking = True
        else:
            self.is_attacking = False
        return score, False

    def _get_nose_positions(self):
        # Level 5 image has two noses; offsets from centre in the unrotated (pointing up) image
        left = (self.position[0] - 6, self.position[1] - 29)
        right = (self.position[0] + 4, self.position[1] - 29)
        return self.rotate_point(self.position, left, self.angle), self.rotate_point(self.position, right, self.angle)

    def attack_animate(self, window):
        if self.level < 5:
            super().attack_animate(window)
            return
        # Beams from both noses meet just in front of the jet, then fire as one big beam
        left_nose, right_nose = self._get_nose_positions()
        mid = ((left_nose[0] + right_nose[0]) / 2, (left_nose[1] + right_nose[1]) / 2)
        tx, ty = self.target.position
        dx, dy = tx - mid[0], ty - mid[1]
        dist = max((dx**2 + dy**2)**0.5, 1)
        join_dist = min(18, dist / 2)
        join = (mid[0] + dx / dist * join_dist, mid[1] + dy / dist * join_dist)
        # Bigger enemies get a stronger beam: thicker, with red edges
        size = self.target.size
        green, core, red = (60, 255, 60), (220, 255, 220), (255, 30, 30)
        beam_width = 7 + 2 * size
        core_width = 2 + size
        pygame.draw.line(window, green, left_nose, join, 3)
        pygame.draw.line(window, green, right_nose, join, 3)
        pygame.draw.line(window, green, join, self.target.position, beam_width)
        pygame.draw.line(window, core, join, self.target.position, core_width)
        if size >= 2:
            # Red lines just outside each edge of the beam
            px, py = -dy / dist, dx / dist  # unit vector across the beam
            off = beam_width / 2 + 1
            for side in (1, -1):
                start = (join[0] + side * px * off, join[1] + side * py * off)
                end = (tx + side * px * off, ty + side * py * off)
                pygame.draw.line(window, red, start, end, 2)
        pygame.draw.circle(window, core, (int(join[0]), int(join[1])), 3 + size)

class Burger(Tower):

    price = 65
    name = 'Burger'
    image = burger_img
    range = 60
    max_level = 5
    unlock_game_levels = {5: 61}  # Burger King after the 60 main levels (or any level once the map is crowned)

    # Level 5 surge: ring of fire, red eyes and double damage for a short time
    surge_frames = 240  # how long a surge lasts (4 seconds at normal speed)
    surge_cooldown_frames = 480  # wait after a surge ends before the next can start (8 seconds)
    surge_min_value = 50  # surge when enemies in range add up to this much health (including what they spawn)
    surge_timer = 0  # frames of surge left (class defaults also cover older saves)
    surge_cooldown = 0
    surge_mode = "auto"  # "auto" surges by itself; "manual" waits for the surge button
    eye_offsets = ((-10, 3), (9, 4))  # eyes on the level 5 image (drawn at 90x90), from the centre

    def __init__(self, position):
        super().__init__(position)
        self.range =  Burger.range
        self.attack_speed = 65
        self.damage = 1
        self.cost = Burger.price
        #self.image = Burger.image  # all of these can be done in base class: self.thing = self.__class__.thing
        self.level = 1
        self.max_attacks = 4
        self.upgrade_costs = [85, 220, 680, 3200]
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
        elif self.level == 5:
            self.image = burger5_img

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
            self.upgrade_name = "Burger King"
        if self.level == 5:
            self.attack_speed = 6
            self.range =  100
            self.image = burger5_img
            self.max_attacks = 30
            self.cost += self.upgrade_costs[3]
            self.splat_img = pygame.transform.scale(splat_img, (self.range+60, self.range+60))
            self.damage = 3 # not sure - with damage 2 and other stats nothing got past

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
        # Burgers saved before level 5 existed
        if len(self.upgrade_costs) < 4:
            self.upgrade_costs.append(3200)
        if self.level == 4:
            self.upgrade_name = "Burger King"

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
                    if self.surge_timer > 0:
                        multiplier *= 2
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
        return score, False

    def new_round(self):
        self.surge_timer = 0
        self.surge_cooldown = 0

    def option_text(self):
        if self.level >= 5:
            return f"Surge: {self.surge_mode.capitalize()}  >"
        return None

    def next_option(self):
        self.surge_mode = "manual" if self.surge_mode == "auto" else "auto"

    def surge_ready(self):
        return self.level >= 5 and self.surge_timer == 0 and self.surge_cooldown == 0

    def start_surge(self):
        self.surge_timer = self.__class__.surge_frames
        sounds.play('fireball')

    def update(self, enemies, gmap):
        if self.level >= 5:
            self._update_surge(enemies, gmap)
        return super().update(enemies, gmap)

    def _update_surge(self, enemies, gmap):
        if self.surge_timer > 0:
            self.surge_timer -= 1
            if self.surge_timer == 0:
                self.surge_cooldown = self.__class__.surge_cooldown_frames
            return
        if self.surge_cooldown > 0:
            self.surge_cooldown -= 1
            return
        if self.surge_mode == "manual":
            return  # waits for the surge button
        strength = sum(enemy.value for enemy in enemies if self.can_target(enemy, gmap))
        if strength >= self.__class__.surge_min_value:
            self.start_surge()

    def _draw_ring_of_fire(self, window):
        cx, cy = self.position
        glow = pygame.Surface((120, 120), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 120, 0, 70), (60, 60), 50)
        window.blit(glow, glow.get_rect(center=(cx, cy)))
        flames = 18
        for i in range(flames):
            angle = 2 * math.pi * i / flames + random.uniform(-0.1, 0.1)
            ux, uy = math.cos(angle), math.sin(angle)
            px, py = -uy, ux  # across the flame
            base = 38
            length = random.uniform(8, 18)
            half = random.uniform(4, 6)
            b = (cx + ux * base, cy + uy * base)
            tip = (cx + ux * (base + length), cy + uy * (base + length))
            colour = random.choice(((255, 60, 0), (255, 140, 0), (255, 210, 40)))
            pygame.draw.polygon(window, colour, [(b[0] + px * half, b[1] + py * half), tip, (b[0] - px * half, b[1] - py * half)])

    def _draw_red_eyes(self, window):
        for ox, oy in self.__class__.eye_offsets:
            centre = (self.position[0] + ox, self.position[1] + oy)
            glow = pygame.Surface((24, 24), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 0, 0, 110), (12, 12), 11)
            window.blit(glow, glow.get_rect(center=centre))
            pygame.draw.circle(window, (255, 40, 40), centre, 4)
            pygame.draw.circle(window, (255, 220, 200), centre, 1)

    def draw(self, window, enemies=None, active=False):
        """Dont rotate burger"""
        surging = self.level >= 5 and self.surge_timer > 0
        if surging:
            self._draw_ring_of_fire(window)
        new_rect = self.image.get_rect(center=self.image.get_rect(center=self.position).center)
        self.general_draw(window, self.image, new_rect)
        if surging:
            self._draw_red_eyes(window)

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
    target_modes = ("first", "strong", "last", "close")

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
        self.ghostsight = True
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

    def draw(self, window, enemies=None, active=False):
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
        return score, False

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
    max_level = 5
    unlock_game_levels = {5: 61}  # tier 5 after the 60 main levels (or any level once the map is crowned)
    glue_times = {1: 180, 2: 240, 3: 300, 4: 360, 5: 360}  # frames before glue wears off (also wears off after glue_layers hits)
    nozzle_offsets = {1: (2, -24), 2: (-2, -25), 3: (5, -25), 4: (10, -24), 5: (11, -37)}  # nozzle tip from centre, unrotated image
    # Tier 5 smother: a big spray encases one enemy, stopping it while acid works
    smother_every_frames = 60  # time between big sprays
    smother_cooldown = 0
    smother_frames = 150  # how long a normal enemy is stopped
    smother_frames_large = 60  # large (size 3) enemies break free sooner
    smother_spray_frames = 10  # how long the big spray stays on screen
    smother_radius = 50  # every enemy this close to the sprayed enemy gets smothered too
    smother_max = 8  # most enemies smothered by one spray
    smother_acid = 4  # acid damage every quarter second while smothered
    smother_spray_target = None  # position the last big spray hit (class default covers older saves)

    def __init__(self, position):
        super().__init__(position)
        self.range =  GlueGunner.range
        self.attack_speed = 40
        self.damage = 1
        self.cost = GlueGunner.price
        #self.image = GlueGunner.image
        self.level = 1
        self.upgrade_costs = [120, 280, 900, 3800]
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
        elif self.level == 5:
            self.image = gluegun5_img

    def __setstate__(self, state):
        super().__setstate__(state)
        # Glue gunners saved before tier 5 existed
        if len(self.upgrade_costs) < 4:
            self.upgrade_costs.append(3800)
        if self.level == 4:
            self.upgrade_name = "Gloopocalypse"

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
            self.upgrade_name = "Gloopocalypse"

        if self.level == 5:
            self.image = gluegun5_img
            self.cost += self.upgrade_costs[3]
            self.beam_width = 22
            self.glue_color = (60, 160, 25)  # darker, stronger toxic glue
            self.toxic_time = 30  # toxic glue ticks twice as often as level 4
            self.attack_speed = 8
            self.range = 130
            self.max_attacks = 10

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
            if self.target and not self._in_spray_arc(self.target[0], enemy):
                continue  # one barrel: only glue enemies roughly in the direction of the first target
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

    spray_arc_degrees = 60  # glue only goes to enemies within this angle either side of the first target

    def _in_spray_arc(self, first, enemy):
        a1 = math.atan2(first.position[1] - self.position[1], first.position[0] - self.position[0])
        a2 = math.atan2(enemy.position[1] - self.position[1], enemy.position[0] - self.position[0])
        diff = abs((a2 - a1 + math.pi) % (2 * math.pi) - math.pi)
        return math.degrees(diff) <= self.__class__.spray_arc_degrees

    def get_target_angle(self):
        # Turn the barrel towards the big smother spray while it is showing
        if self.viz_persist > 0 and self.smother_spray_target is not None:
            dx = self.smother_spray_target[0] - self.position[0]
            dy = self.smother_spray_target[1] - self.position[1]
            return math.degrees(math.atan2(-dy, dx)) - 90
        return super().get_target_angle()

    # Needs to take account of rotation
    #def get_nozzle_pos(self):
        #if self.level == 1:
            #return self.position
            #return (self.position[0]+20, self.position[1]-10)
        #elif self.level == 2:
            #return (self.position[0]-17, self.position[1]-15)
        #elif self.level == 3:
            #return (self.position[0]+15, self.position[1]-16)

    def _get_nozzle_pos(self):
        # The image is drawn rotated by self.angle (see Tower.draw), so rotate the tip the same way
        ox, oy = self.__class__.nozzle_offsets[self.level]
        tip = (self.position[0] + ox, self.position[1] + oy)
        return self.rotate_point(self.position, tip, self.angle)

    def attack_animate(self, window):
        nozzle = self._get_nozzle_pos()
        for target in self.target:
            pygame.draw.line(window, self.glue_color, nozzle, target.position, self.beam_width)

    def new_round(self):
        self.smother_cooldown = 0
        self.viz_persist = 0

    def update(self, enemies, gmap):
        result = super().update(enemies, gmap)
        if self.level >= 5:
            if self.smother_cooldown > 0:
                self.smother_cooldown -= 1
            else:
                self._smother_one(enemies, gmap)
        return result

    def _smother_one(self, enemies, gmap):
        """Big spray at the strongest cluster in range (total health); globs everything clustered round it."""
        cls = self.__class__
        candidates = [e for e in enemies if e.can_be_smothered() and self.can_target(e, gmap)]
        if not candidates:
            return
        r2 = cls.smother_radius ** 2
        def cluster(centre):
            cx, cy = centre.position
            return [e for e in candidates if (e.position[0] - cx) ** 2 + (e.position[1] - cy) ** 2 <= r2]
        target = max(candidates, key=lambda c: sum(e.value for e in cluster(c)))  # ties go to the one further along
        self.smother_cooldown = cls.smother_every_frames
        group = cluster(target)
        for enemy in group[:cls.smother_max]:
            frames = cls.smother_frames_large if enemy.size >= 3 else cls.smother_frames
            enemy.smother(self, frames, cls.smother_acid)
        self.smother_spray_target = target.position
        # One big glob of goo where the spray lands, drawn once for this spray
        self.smother_cloud = make_goo(cls.smother_radius * 1.1, cls.smother_radius * 0.65, random.random())
        self.viz_persist = self.__class__.smother_spray_frames
        sounds.play('glue')

    def show_viz_persist(self, window):
        """The big smother spray: a wide cone of glue from the barrel that lingers for a few frames."""
        if self.smother_spray_target is not None:
            nozzle = self._get_nozzle_pos()
            tx, ty = self.smother_spray_target
            dx, dy = tx - nozzle[0], ty - nozzle[1]
            dist = max((dx * dx + dy * dy) ** 0.5, 1)
            px, py = -dy / dist, dx / dist
            near, far = 10, 30  # half widths at the barrel and at the target
            cone = [(nozzle[0] + px * near, nozzle[1] + py * near), (tx + px * far, ty + py * far),
                    (tx - px * far, ty - py * far), (nozzle[0] - px * near, nozzle[1] - py * near)]
            spray = pygame.Surface(window.get_size(), pygame.SRCALPHA)
            pygame.draw.polygon(spray, GOO_FILL + (170,), cone)
            pygame.draw.line(spray, GOO_SHINE + (200,), nozzle, (tx, ty), 5)
            window.blit(spray, (0, 0))
            cloud = getattr(self, 'smother_cloud', None)
            if cloud is not None:
                surface, (ox, oy) = cloud
                window.blit(surface, (int(tx - ox), int(ty - oy)))
        if self.viz_persist > 0:
            self.viz_persist -= 1

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
                target.glue_timer = self.__class__.glue_times[self.level]
                target.glue_color = self.glue_color
                if self.level >= 3:
                    target.toxic_glued = True
                    target.toxic_glued_by = self
                    target.toxic_timer = self.toxic_time
                    target.toxic_time = self.toxic_time  # do another pass on this - very tired - dont want to set two values here.
            self.reset_attack_timer()
            self.is_attacking = True  # Set to True when attacking
        else:
            self.is_attacking = False  # Set to False otherwise
        return score, False

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

    def draw(self, window, enemies=None, active=False):
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
    target_modes = ("first", "strong", "last", "close")
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


# Should make projectile class - diff types and levels of projectile will be inherited.
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

    def update(self, enemies, gmap, window):
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

    def draw(self, window, enemies=None, active=False):
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


class Ninja(Tower):

    price = 100
    name = 'Ninja'
    image = ninja_img
    range = 80
    max_level = 4
    target_modes = ("first", "strong", "last", "close")
    footprint = (40,50)  # May make bigger

    shurikens = {1: shuriken_img, 2:shuriken_img2, 3:shuriken_img3, 4:shuriken_img4}

    def __init__(self, position):
        super().__init__(position)
        self.range =  Ninja.range
        self.cost = Ninja.price
        self.image = Ninja.image
        self.level = 1
        self.attack_speed = 60
        self.upgrade_costs = [160, 520, 1200] # rough - need to decide
        self.upgrade_name = "Spirit Eye"
        self.damage = 1  # same as normal shuriken
        self.multi_attack = 1
        self.spawn_attack_factor = 1
        self.tmp_score_check = 0
        self.darkpath = False  # set from the map each update

    def load_images(self):
        if self.level == 2:
            self.image = ninja2_img
        elif self.level == 3:
            self.image = ninja3_img
        elif self.level == 4:
            self.image = ninja4_img

    def level_up(self):
        self.level +=1
        if self.level == 2:
            self.attack_speed = 50
            self.image = ninja2_img
            self.cost += self.upgrade_costs[0]
            self.upgrade_name = "Iron Wind"   # provisional - working on it
            self.range = 90
            self.ghostsight = True
        if self.level == 3:
            self.attack_speed = 40
            self.image = ninja3_img
            self.cost += self.upgrade_costs[1]
            self.upgrade_name = "Red Reaper"
            self.ghostsight = True
            self.range = 100
            self.red_damage = 3  # red shuriken - dpeneds on enemy size.
        if self.level == 4:
            # "Reap the whirlwind"
            # different for spawn and non-spawn attacks
            self.image = ninja4_img
            self.attack_speed = 8
            self.spawn_attack_factor = 5
            self.multi_attack = 4
            #self.red_damage = 3  # should be same as shuriken damage - red shuriken - dpeneds on enemy size.
            self.cost += self.upgrade_costs[2]
            self.range = 100
            self.ghostsight = True

            self.orbit_angle = 0  # Starting angle in degrees
            self.orbit_radius = 30  # Radius of the orbit (adjust as needed)
            self.shuriken_rotation_angle = 0  # For shuriken spinning effect
            self.shuriken_rotation_speed = 45  # Degrees per frame for shuriken rotation
            self.orbit_speed = 5  # Degrees per frame for orbit movement


    # soon to make first/strong/close options
    # this is to get closest in range - else can use default find_target
    #def find_target(self, enemies, gmap):
        #tmp_target = []
        #self.target = []
        #for enemy in enemies:
            #if self.in_range(enemy) and self.is_visible(enemy, gmap) and not enemy.reached_end:
                #tmp_target.append(enemy)
        #if tmp_target:
            #self.target = self.find_close(tmp_target)

    #def find_close(self, enemies):
        #"""Return the closest enemy or None"""
        #closest_enemy = None
        #closest_dist = float('inf')  # Start with a very high value
        #for enemy in enemies:
            #dist = ((self.position[0] - enemy.position[0])**2 + (self.position[1] - enemy.position[1])**2)**0.5
            #if dist < closest_dist:
                #closest_dist = dist
                #closest_enemy = enemy
        #return closest_enemy

    def use_red_shuriken(self):
        # whether to realesae a red shuriken
        return self.level >= 3 and self.target.size >= 2

    def attack_score(self):
        if self.use_red_shuriken():
            score = self.target.take_damage(self.red_damage)
        else:
            score = self.target.take_damage(self.damage)
        self.tmp_score_check+=score
        return score

    def attack(self):
        score = 0
        spawn = False
        if self.target and self.attack_timer <= 0:  # why attack_timer here and in update?
            self.attack_count += 1
            # Hits first then spawns shuriken from that position
            score = self.attack_score()
            spawn = True
            self.reset_attack_timer()
            self.is_attacking = True
        else:
            self.is_attacking = False
        #self.tmp_score_check+=score
        return score, spawn

    def lev4_attack(self, enemies, gmap):
        score = 0
        spawn = False
        if self.target and self.attack_timer <= 0:  # why attack_timer here and in update?
        #if self.attack_timer <= 0:  # why attack_timer here and in update?
            self.attack_count += 1

            if self.attack_count % self.spawn_attack_factor == 0:
                # Hits first then spawns shuriken from that position
                score = self.attack_score()
                #self.tmp_score_check+=score
                spawn = True
            else:
                # even though found a target - going to calc multiple targets now.
                tmp_target = []
                self.target = []
                for enemy in enemies:
                    if self.in_range(enemy) and self.is_visible(enemy, gmap) and not enemy.reached_end:
                        self.target.append(enemy)
                        if len(self.target) > self.multi_attack:
                            break
                for target in self.target:
                    # shouldn't this be single damage or red damage for large....
                    score += target.take_damage(self.red_damage)
                self.tmp_score_check+=score
                spawn = False
            self.reset_attack_timer()
            self.is_attacking = True
        else:
            self.is_attacking = False
        return score, spawn

    def update(self, enemies, gmap):
        score = 0
        spawn = False
        self.darkpath = gmap.darkpath
        self.attack_timer -= 1
        if self.attack_timer <= 0:

            # Hits first then spawns shuriken from there
            self.find_target(enemies, gmap)
            if self.level==4:
                score, spawn = self.lev4_attack(enemies, gmap)
            else:
                #self.find_target(enemies, gmap)
                score, spawn = self.attack()
            self.total_score += score
            #self.tmp_score_check+=score
        else:
            self.is_attacking = False
        return score, spawn

    def get_projectile(self):
        if self.use_red_shuriken():
            projectile = RedShuriken(self)
        else:
            projectile = Shuriken(self)
        return projectile

    def draw(self, window, enemies=None, active=False):
        """Dont rotate burger"""
        new_rect = self.image.get_rect(center=self.image.get_rect(center=self.position).center)
        self.general_draw(window, self.image, new_rect)

        if self.level == 4 and active:
            if self.target:
                booster = 5 * self.speed_mod
            else:
                booster = 1

            self.orbit_angle = (self.orbit_angle + self.orbit_speed*booster) % 360
            self.shuriken_rotation_angle = (self.shuriken_rotation_angle + self.shuriken_rotation_speed) % 360

            # Calculate shuriken position around the ninja
            angle_rad = math.radians(self.orbit_angle)
            shuriken_x = self.position[0] + self.orbit_radius * math.cos(angle_rad)
            shuriken_y = self.position[1] + self.orbit_radius * math.sin(angle_rad)
            shuriken_position = (shuriken_x, shuriken_y)

            # Rotate the shuriken image
            rotated_image = pygame.transform.rotate(shuriken_red_img, self.shuriken_rotation_angle)
            image_rect = rotated_image.get_rect(center=shuriken_position)

            # Draw the shuriken
            window.blit(rotated_image, image_rect.topleft)

    def attack_animate(self, window):
        if type(self.target) is not list:
            if self.use_red_shuriken():
                image = shuriken_red_img
            elif self.darkpath:
                image = shuriken_dark_img
            else:
                image = self.shurikens[self.level]
            mid_point = ((self.position[0] + self.target.position[0]) // 2,
                        (self.position[1] + self.target.position[1]) // 2)
            shuriken_rect = image.get_rect(center=mid_point)
            window.blit(image, shuriken_rect)


# Should make projectile class - diff types and levels of projectile will be inherited.
class Shuriken(Tower):

    # For now same - but can be diff for each level
    image = shuriken_img
    image2 = shuriken_img2
    image3 = shuriken_img3
    image4 = shuriken_img4

    def __init__(self, tower):
        super().__init__(tower.target.position)
        self.launcher = tower
        self.angle
        self.speed = 8
        self.hit_tolerance = 8
        self.hit_enemies = [tower.target]  # Ninja already hit this enemy when throwing
        self.target_pos = tower.target.position  # position when shoot
        self.path = tower.target.path
        self.path_index = tower.target.path_index
        self.distance = 0
        self.distance_since_hit = 0
        self.num_hits = 0
        self.active = True
        self.max_attacks = 4
        self.damage = 1
        self.image = Shuriken.image
        self.expl_image = explosionMini_img
        self.hit_range = 80
        self.show_expl = False  # general option
        self.show_blast = False  # whether to show this cycle
        self.blast_cycles = 0

        if self.launcher.level == 2:
            self.image = Shuriken.image2
            self.hit_range = 100
            self.damage = 1
            self.max_attacks = 6
        if self.launcher.level == 3:
            self.image = Shuriken.image3
            self.hit_range = 160
            self.speed = 10
            self.damage = 1
            self.max_attacks = 32
        if self.launcher.level == 4:
            self.image = Shuriken.image4
            self.hit_range = 180
            self.damage = 1  # tried 2
            self.max_attacks = 64

        if self.launcher.darkpath:
            self.image = shuriken_dark_img  # RedShuriken overrides this after super().__init__

    def is_between(self, old_pos, new_pos, enemy_pos):
        # Check if enemy position is close to the line segment defined by old_pos and new_pos
        x0, y0 = enemy_pos
        x1, y1 = old_pos
        x2, y2 = new_pos

        dx = x2 - x1
        dy = y2 - y1
        line_length_sq = dx * dx + dy * dy

        if line_length_sq == 0:
            # The line segment is a point
            distance_sq = (x0 - x1) ** 2 + (y0 - y1) ** 2
            return distance_sq <= self.hit_tolerance ** 2

        # Parameter t of the projection of the enemy onto the line
        t = ((x0 - x1) * dx + (y0 - y1) * dy) / line_length_sq
        t = max(0, min(1, t))  # Clamp t to [0, 1] to stay within the segment

        # Closest point on the segment
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        # Distance from enemy to the closest point
        distance_sq = (x0 - closest_x) ** 2 + (y0 - closest_y) ** 2

        return distance_sq <= self.hit_tolerance ** 2

    def update(self, enemies, gmap, window):
        # Move towards the next point in the path
        score = 0
        self.see_ghosts = self.launcher.see_ghosts
        if self.path_index >= 0:
            target_pos = self.path[self.path_index]  # For backward movement
            dx, dy = self.position[0] - target_pos[0], self.position[1] - target_pos[1]
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance > self.speed:
                dx, dy = dx / distance * self.speed, dy / distance * self.speed

            old_position = self.position
            self.position = (self.position[0] - dx, self.position[1] - dy)

            self.distance += self.speed
            self.distance_since_hit += self.speed
            #print(f"{self.distance_since_hit=}  {self.distance=}")

            for enemy in enemies:
                if enemy in self.hit_enemies or enemy.reached_end:
                    continue  # Skip enemies already hit by this projectile

                if self.is_between(old_position, self.position, enemy.position):
                    score += enemy.take_damage(self.damage)

                    self.num_hits += 1
                    self.hit_enemies.append(enemy)  # Add enemy to hit list
                    self.distance_since_hit = 0

                    # To show mini-explosion (streak of ninja power) each hit
                    # self.attack_animate(window)
                    # todo - see why animate was separated - pass window to update....

                    if self.show_expl:
                        #explosion_rect = self.expl_image.get_rect(center=self.position)
                        #window.blit(self.expl_image, explosion_rect)
                        self.show_blast = True
                        self.blast_cycles = 1

                    if self.num_hits >= self.max_attacks:
                        self.active = False
                        break

                # shows up much more for some reason? And see rectangle???
                # explosion_rect = self.expl_image.get_rect(center=self.position)
                # window.blit(self.expl_image, explosion_rect)
                # if self.show_expl:
                    # print('here')
                    # explosion_rect = self.expl_image.get_rect(center=self.position)
                    # window.blit(self.expl_image, explosion_rect)

            # Check if reached the target position
            if abs(self.position[0] - target_pos[0]) < self.speed and \
               abs(self.position[1] - target_pos[1]) < self.speed:
                self.path_index -= 1

            #self.distance += self.speed

        # Check if the projectile has reached the end of the path
        if self.distance_since_hit > self.hit_range or self.path_index < 0:
            self.active = False

        self.launcher.tmp_score_check += score
        #print(f"tmp_score_check {self.launcher.tmp_score_check}")
        self.launcher.total_score += score

        return score, False  # Temporary return values - maybe right - launch gets score...


    def draw(self, window, enemies=None, active=False):
        x = self.position[0]
        y = self.position[1]
        if self.active:
            #self.angle = (self.angle + 45) % 360
            self.angle = (self.angle + 20) % 360  # try roate slower
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            image_rect = rotated_image.get_rect(center=self.position)
            window.blit(rotated_image, image_rect.topleft)
            #print(f"{self.target=}")


    def attack_animate(self, window):
        # quite like mini explosion effect except at end of level when looks like explosion
        if self.show_blast or not self.active:
            explosion_rect = self.expl_image.get_rect(center=self.position)
            window.blit(self.expl_image, explosion_rect)
            self.blast_cycles -= 1
            if self.blast_cycles <= 0:
                self.show_blast = False


class RedShuriken(Shuriken):

    # For now same - but can be diff for each level
    image = shuriken_red_img

    def __init__(self, tower):
        super().__init__(tower)
        self.hit_tolerance = 10
        self.max_attacks = 12
        self.damage = 3
        self.image = RedShuriken.image
        self.expl_image = explosionMini_img
        self.hit_range = 120
        self.show_expl = True


#tower_types = [Fighter, Burger, GlueGunner, Wizard, Cannon, Totem, Ninja]
tower_types = [Fighter, Burger, GlueGunner, Ninja, Wizard, Cannon, Totem]
