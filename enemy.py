import math
import pygame
from assets import load_image, sys_font
import sounds
import random

ghost_img = load_image('images/ghost.png')
ghost_img = pygame.transform.scale(ghost_img, (50, 50))
big_ghost_img = pygame.transform.scale(ghost_img, (70, 70))
devil_img = load_image('images/devil.png')
devil_img = pygame.transform.scale(devil_img, (50, 50))
bigdevil_img = pygame.transform.scale(devil_img, (75, 75))
troll_img = load_image('images/troll.png')
troll_img = pygame.transform.scale(troll_img, (50, 50))
giant_troll_img = pygame.transform.scale(troll_img, (90, 90))
king_img = load_image('images/kingblob.png')
king_img = pygame.transform.scale(king_img, (100, 100))
king2_img = load_image('images/kingblob_green.png')
king2_img = pygame.transform.scale(king2_img, (110, 110))
troll_wagon_img = load_image('images/troll_wagon.png')
troll_wagon_img = pygame.transform.smoothscale(troll_wagon_img, (168, 120))  # faces right
troll_wagon_left_img = pygame.transform.flip(troll_wagon_img, True, False)
king3_img = load_image('images/kingblob_red.png')
king3_img = pygame.transform.scale(king3_img, (125, 125))
stone_head_img = load_image('images/stone_head.png')
stone_head_img = pygame.transform.smoothscale(stone_head_img, (stone_head_img.get_width() * 96 // stone_head_img.get_height(), 96))

armored_troll_img = load_image('images/armored_troll.png')
armored_troll_img = pygame.transform.scale(armored_troll_img, (65, 65))
giant_armored_troll_img = pygame.transform.scale(armored_troll_img, (100, 100))


# Toxic goo used by the tier 5 glue gunner's smother
GOO_FILL, GOO_EDGE, GOO_SHINE = (46, 130, 20), (20, 70, 8), (150, 220, 90)

def make_goo(rx, ry, seed, alpha=175):
    """A smooth, lumpy glob of dark toxic goo with drips and a highlight.
    Returns (surface, centre offset) - blit at (x - offset[0], y - offset[1])."""
    sc = 4  # draw large then shrink, for smooth edges
    rnd = random.Random(seed)
    a = [rnd.uniform(0, 6.3) for _ in range(3)]
    w, h = int(rx * 2.6), int(ry * 3.4)
    cx, cy = w / 2, ry * 1.3
    big = pygame.Surface((w * sc, h * sc), pygame.SRCALPHA)
    pts = []
    for i in range(72):
        t = 2 * math.pi * i / 72
        r = 1 + 0.10 * math.sin(3 * t + a[0]) + 0.07 * math.sin(5 * t + a[1]) + 0.04 * math.sin(7 * t + a[2])
        pts.append(((cx + math.cos(t) * rx * r) * sc, (cy + math.sin(t) * ry * r) * sc))
    for _ in range(3):  # drips hanging off the bottom
        x = (cx + rnd.uniform(-0.7, 0.7) * rx) * sc
        top = (cy + ry * 0.75) * sc
        length = rnd.uniform(0.35, 0.8) * ry * sc
        dw = rnd.uniform(0.08, 0.14) * rx * sc
        pygame.draw.rect(big, GOO_FILL, (x - dw, top, dw * 2, length))
        pygame.draw.ellipse(big, GOO_FILL, (x - dw * 1.4, top + length - dw * 1.4, dw * 2.8, dw * 2.8))
    pygame.draw.polygon(big, GOO_FILL, pts)
    pygame.draw.lines(big, GOO_EDGE, True, pts, 3 * sc)
    pygame.draw.ellipse(big, GOO_SHINE, ((cx - rx * 0.55) * sc, (cy - ry * 0.7) * sc, rx * 0.5 * sc, ry * 0.28 * sc))
    small = pygame.transform.smoothscale(big, (w, h))
    small.set_alpha(alpha)
    return small, (cx, cy)


class Enemy:
    health = 1
    spawn = False
    # Smothered by a tier 5 glue gunner: stopped while acid does damage, then briefly immune
    smother_timer = 0
    smother_immune = 0
    smother_tick = 0
    smothered_by = None
    smother_tick_frames = 15  # acid damage every this many frames while smothered
    smother_acid_damage = 2  # set by the tower that smothers it
    smother_immune_frames = 120
    coat_color = (150, 121, 105)  # concrete
    coat_points_per_px = 1  # coating hits shown by each pixel of ring thickness
    coat_sound = 'ting'
    def __init__(self, path, position=None, path_index=0):
        self.path = path
        self.path_index = path_index
        self.base_speed = 2  # help with things like gluing from a stronger glue gunner
        self.speed = 2
        self.reached_end = False  # Indicates if the enemy has reached the end of the path (or dead)
        self.spawn_on_die = self.__class__.spawn  # not used for regular color enemies - those change attributes.
        self.health = self.__class__.health
        self.value = self.__class__.health
         # for now not due to problem - right ans may be make spawn_count / spawn_type class attributes
        #self.value = self.recursive_value()
        self.color = (255, 0, 0)
        self.image = None
        self.invis = False
        self.fortified = False
        self.position = position or self.path[0]
        self.size = 1
        self.slowable = True
        self.glue_reset()
        self.distance = 0
        self.spawn_sep = 2

    def glue_reset(self):
        self.slow_factor = 1
        self.glued = 0  # hits left before the glue wears off
        self.glue_timer = 0  # frames left before the glue wears off
        self.glue_color = None
        self.toxic_glued = False
        self.toxic_glued_by = None
        self.toxic_timer = None
        self.toxic_time = None
        self.toxic_attacks = 0

    #problem set before or after super
    def recursive_value(self):
        value = self.health
        if self.spawn_on_die:
            value += self.spawn_count * self.spawn_type.recursive_value()
        return value

    def draw_glue_splat(self, window, color, x, y, esize):
        pygame.draw.circle(window, color, (int(x)-2, int(y)-3), 4+esize)
        pygame.draw.circle(window, color, (int(x)+2, int(y)+4), 4+esize)
        pygame.draw.circle(window, color, (int(x)+2, int(y)-3), 4+esize)

    def on_spawn(self, enemies):
        """Called when a level spawns this enemy, before it joins the list"""
        pass

    def draw(self, window):
        x = self.position[0]
        y = self.position[1]
        if self.image is not None:
            image_rect = self.image.get_rect(center=self.position)
            window.blit(self.image, image_rect.topleft)
        else:
            # TODO - check cant you use self.position - isn't it already int.
            pygame.draw.circle(window, self.color, (int(x), int(y)), 10*self.size)
            if self.fortified and self.fort_health > 0:
                w = math.ceil(self.fort_health / self.coat_points_per_px)
                # could be same size or bigger to go round outside
                pygame.draw.circle(window, self.coat_color, (int(x), int(y)), 10+w, w)
            else:
                pygame.draw.circle(window, (0, 0, 0), (int(x), int(y)), 11, 1)
        if self.glued:
            self.draw_glue_splat(window, self.glue_color, x, y, self.size)
            if self.toxic_glued:
                if self.toxic_attacks > 1:
                    rng = random.Random(1)  # fixed splat positions without touching the global RNG
                    for splat in range(1, self.toxic_attacks+1):

                        # Hack try make king blob look better
                        if isinstance(self, KingBlob):
                            xn = x + rng.randint(-25, 25)
                            yn = y + rng.randint(-5, 30)
                        else:
                            xn = x + rng.randint(-15, 15)
                            yn = y + rng.randint(-15, 15)

                        self.draw_glue_splat(window, self.glue_color, xn, yn, self.size)
        if self.smother_timer > 0:
            self.draw_smother(window)

    def can_be_smothered(self):
        return self.smother_timer == 0 and self.smother_immune == 0

    def smother(self, tower, frames, acid_damage):
        self.smother_timer = frames
        self.smother_acid_damage = acid_damage
        self.smother_tick = self.smother_tick_frames
        self.smothered_by = tower

    def smother_damage(self):
        """Acid damage while smothered (called each frame from the game loop). Returns the score."""
        if self.smother_timer <= 0:
            return 0
        score = 0
        self.smother_timer -= 1
        self.smother_tick -= 1
        if self.smother_tick <= 0:
            score = self.take_damage(self.smother_acid_damage)
            if self.smothered_by is not None:
                self.smothered_by.total_score += score
            self.smother_tick = self.smother_tick_frames
        if self.smother_timer == 0:
            self.smother_immune = self.smother_immune_frames
            self.smothered_by = None
        return score

    def draw_smother(self, window):
        """This enemy stuck in a glob of toxic goo, with bubbles rising through it."""
        if getattr(self, 'goo', None) is None:
            if self.image is not None:
                r = self.image.get_width() // 2 + 6
            else:
                r = 10 * self.size + 6
            self.goo = make_goo(r, r * 0.85, id(self))  # drawn once, reused every frame
        surface, (ox, oy) = self.goo
        x, y = self.position
        window.blit(surface, (int(x - ox), int(y - oy)))
        r = surface.get_width() / 2.6
        for i in range(3):
            phase = (self.smother_timer * 1.5 + i * 23) % 40
            bx = x + (i - 1) * r * 0.45
            by = y + r * 0.5 - phase / 40 * r * 1.1
            pygame.draw.circle(window, GOO_SHINE, (int(bx), int(by)), 2, 1)

    def move(self):
        self.update_glue()
        if self.smother_immune > 0:
            self.smother_immune -= 1
        if self.smother_timer > 0:
            return  # smothered: stuck in place
        # Move towards the next point in the path
        if self.path_index < len(self.path) - 1:
            target_pos = self.path[self.path_index + 1]  # for backwards move just make -1
            dx, dy = target_pos[0] - self.position[0], target_pos[1] - self.position[1]
            distance = (dx**2 + dy**2)**0.5
            if distance > self.speed:
                dx, dy = dx / distance * self.speed, dy / distance * self.speed
            self.position = (self.position[0] + dx, self.position[1] + dy)

            # Check if the enemy has reached the target position
            if abs(self.position[0] - target_pos[0]) < self.speed and abs(self.position[1] - target_pos[1]) < self.speed:
                self.path_index += 1

            self.distance += self.speed

        # Check if the enemy has reached the end of the path
        if self.path_index >= len(self.path) - 1:
            self.reached_end = True

    def unglue(self):
        self.glue_reset()
        self.speed = self.base_speed

    def glue_hit(self):
        # Each hit taken uses up one layer of glue
        if self.glued > 0:
            self.glued -= 1
            if self.glued <= 0:
                self.unglue()

    def update_glue(self):
        # Glue also wears off after a time
        if self.glued > 0:
            self.glue_timer -= 1
            if self.glue_timer <= 0:
                self.unglue()

    def take_damage(self, damage):
        score = min(self.health, damage)  # Make sure don't score more than remaining health
        self.health -= damage
        self.value -= damage
        self.glue_hit()
        if self.fortified and self.fort_health > 0:
            self.fort_health -= damage
            sounds.play(self.coat_sound)
        else:
            sounds.play('blop')
        if self.health <= 0:
            self.reached_end = True  # Treat the enemy as "dead" or "reached the end"
        return score

    def spawn_func(self, enemies):
        for i in range(self.spawn_count):
            enemy = self.spawn_type(self.path, self.position, self.path_index)
            enemy.distance = self.distance  # keep place in the first-to-last ordering
            # Spread out slightly
            for j in range(i*self.spawn_sep):
                enemy.move()
            enemies.append(enemy)  # Also puts on end - so will not attack first!

    def toxic_damage(self):
        if self.glued <= 0:
            self.glue_reset()
            return 0
        score = 0
        if self.toxic_timer > 0:
            self.toxic_timer -= 1
        else:
           #self.toxic_attacks += 1
           glued_by = self.toxic_glued_by  # the hit below may wear off the glue and clear this
           score = self.take_damage(self.toxic_attacks)
           glued_by.total_score += score  # if tower is sold - obj still exists but not in tower list
           self.toxic_timer = self.toxic_time
        return score


class Enemy2(Enemy):
    health = 2
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.base_speed = 3
        self.speed = 3
        self.color = (0, 0, 255)

    def take_damage(self, damage):
        val = super().take_damage(damage)
        if self.health == 1:
            self.color = (255, 0, 0)
            self.base_speed = 2
            self.speed = 2
            self.value = 1
            if self.glued > 0:
                self.speed *= self.slow_factor
        return val


class Enemy3(Enemy2):
    health = 3
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.base_speed = 4
        self.speed = 4
        self.color = (0, 255, 0)

    def take_damage(self, damage):
        val = super().take_damage(damage)
        if self.health == 2:
            self.color = (0, 0, 255)
            self.base_speed = 3
            self.speed = 3
            self.value = 2
            if self.glued > 0:
                self.speed *= self.slow_factor
        return val


class Enemy4(Enemy3):
    health = 4
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.base_speed = 5
        self.speed = 5
        self.color = (255, 255, 0)

    def take_damage(self, damage):
        val = super().take_damage(damage)
        if self.health == 3:
            self.color = (0, 255, 0)
            self.base_speed = 4
            self.speed = 4
            self.value = 3
            if self.glued > 0:
                self.speed *= self.slow_factor
        return val


class Enemy5(Enemy4):
    health = 5
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.base_speed = 6
        self.speed = 6
        self.color = (127, 0, 255)

    def take_damage(self, damage):
        val = super().take_damage(damage)
        if self.health == 4:
            self.color = (255, 255, 0)
            self.base_speed = 5
            self.speed = 5
            self.value = 4
            if self.glued > 0:
                self.speed *= self.slow_factor
        return val


class Enemy6(Enemy5):
    """Fastest blob - quicker than meteors"""
    health = 6
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.base_speed = 8
        self.speed = 8
        self.color = (255, 105, 180)

    def take_damage(self, damage):
        val = super().take_damage(damage)
        if self.health == 5:
            self.color = (127, 0, 255)
            self.base_speed = 6
            self.speed = 6
            self.value = 5
            if self.glued > 0:
                self.speed *= self.slow_factor
        return val


class Enemy101(Enemy):
    health = 4
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.fortified = True
        self.fort_health = 3


class Enemy102(Enemy2):
    health = 6
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.fortified = True
        self.fort_health = 4


class Enemy103(Enemy3):
    health = 8
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.fortified = True
        self.fort_health = 5


class Enemy104(Enemy4):
    health = 10
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.fortified = True
        self.fort_health = 6


class Enemy105(Enemy5):
    """Iron coated"""
    health = 30
    coat_color = (45, 48, 55)
    coat_points_per_px = 5
    coat_sound = 'ting_deep'
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.fortified = True
        self.fort_health = 25


class Enemy106(Enemy6):
    """Iron coated"""
    health = 56
    coat_color = (45, 48, 55)
    coat_points_per_px = 5
    coat_sound = 'ting_deep'
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.fortified = True
        self.fort_health = 50


class Ghost(Enemy):
    health = 2
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.base_speed = 3
        self.speed = 3
        self.image = ghost_img
        self.invis = True

    # TODO - is this needed - check difference to original function
    def take_damage(self, damage):
        score = min(self.health, damage)
        self.health -= damage
        self.value -= damage
        self.glue_hit()
        sounds.play('blop')
        if self.health <= 0:
            self.reached_end = True
        return score


class BigGhost(Ghost):
    health = 20
    spawn = True
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.health = self.__class__.health
        self.base_speed = 3
        self.speed = 3
        self.image = big_ghost_img
        #self.spawn_on_die = True
        self.spawn_type = Ghost
        self.spawn_count = 8
        self.value = self.health + self.spawn_count*self.spawn_type.health  # what if that also spawns?


class Devil(Ghost):
    health = 8
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.base_speed = 4
        self.speed = 4
        self.image = devil_img
        self.size = 2

class BigDevil(Devil):
    health = 80
    spawn = True
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.base_speed = 3
        self.speed = 3
        self.image = bigdevil_img
        self.size = 3
        self.spawn_type = Devil
        self.spawn_count = 10
        self.value = self.health + self.spawn_count*self.spawn_type.health

class Troll(Enemy):
    health = 20
    spawn = True
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.base_speed = 2
        self.speed = 2
        self.image = troll_img
        #self.spawn_on_die = True
        self.spawn_type = Enemy3
        self.spawn_count = 3
        self.size = 2
        self.value = self.health + self.spawn_count*self.spawn_type.health

    # TODO - is this needed - check difference to original function
    def take_damage(self, damage):
        score = min(self.health, damage)
        self.health -= damage
        self.value -= damage
        self.glue_hit()
        sounds.play('blop')
        if self.health <= 0:
            self.reached_end = True
        return score


class ArmoredTroll(Troll):
    health = 60 #70 60 more aesthetic - like original giant troll
    spawn = True
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.image = armored_troll_img
        self.spawn_type = Enemy103
        self.spawn_count = 3
        self.value = self.health + self.spawn_count*self.spawn_type.health


# Tempted to give this more health - and even maybe to swap for armored troll in earlier levels...
# of course will be a large giant armored troll also.
class GiantTroll(Troll):
    health = 120  # was 60 but thats now armored troll - up this
    spawn = True
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.base_speed = 2
        self.speed = 2
        self.image = giant_troll_img
        #self.spawn_on_die = True
        #self.spawn_type = Enemy103  # make same as troll
        self.spawn_sep = 1
        self.spawn_count = 20 # 6 Up number as not armored
        self.size = 3
        self.value = self.health + self.spawn_count*self.spawn_type.health


class ArmoredGiantTroll(GiantTroll):
    health = 240 # 220 - make at least 240 as double giant - but maybe should triple to 360?
    spawn = True
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.image = giant_armored_troll_img
        self.spawn_type = Enemy103
        self.value = self.health + self.spawn_count*self.spawn_type.health


class Meteor(Enemy):
    health = 10
    value = 30 # tmp until get new function working
    spawn = True
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.base_speed = 7
        self.speed = self.base_speed
        #self.spawn_on_die = True
        self.spawn_type = Enemy4
        self.spawn_count = 5
        self.size = 2
        self.color =  (193, 154, 107)
        self.fortified = True
        self.fort_health = self.health
        self.value = self.health + self.spawn_count*self.spawn_type.health

class BlackMeteor(Enemy):
    health = 40
    spawn = True
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.base_speed = 7  # could make faster also
        self.speed = self.base_speed
        #self.spawn_on_die = True
        self.spawn_type = Enemy104
        self.spawn_count = 10
        self.size = 2
        self.color = (0,0,0) # (255, 36, 0) # (139, 0, 0) # (253, 208, 23)  # (74, 4, 4) # (196, 180, 84)
        self.fortified = True
        self.fort_health = 10
        self.value = self.health + self.spawn_count*self.spawn_type.health



class KingBlob(Enemy):
    health = 100
    spawn = True
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.base_speed = 1
        self.speed = 1
        self.image = king_img
        #self.spawn_on_die = True
        self.spawn_type = Enemy2 #proper one
        self.spawn_count = 100
        self.size = 3
        self.value = self.health + self.spawn_count*self.spawn_type.health

    # TODO - is this needed - check difference to original function
    def take_damage(self, damage):
        score = min(self.health, damage)
        self.health -= damage
        self.value -= damage
        self.glue_hit()
        sounds.play('blop')
        if self.health <= 0:
            sounds.play('pop')
            self.reached_end = True
        return score

    def generate_point_cloud(self, central_point, n_points, spread=1.0):
        """ Generates a cloud of 2D points around a central point."""
        x_center, y_center = central_point
        return [(x_center + random.uniform(-spread, spread),
                y_center + random.uniform(-spread, spread)) for _ in range(n_points)]

    def spawn_func(self, enemies):
        points = self.generate_point_cloud(self.position, self.spawn_count, spread=100)

        for point in points:
            enemy = self.spawn_type(self.path, point, self.path_index)
            enemy.distance = self.distance
            enemies.append(enemy)


class KingBlob2(KingBlob):
    health = 200
    spawn = True
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.base_speed = 1
        self.speed = 1
        self.image = king2_img
        #self.spawn_on_die = True
        self.spawn_type = Enemy3
        self.spawn_count = 150
        self.size = 3
        self.value = self.health + self.spawn_count*self.spawn_type.health


class KingBlob3(KingBlob):
    health = 1000
    spawn = True
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.base_speed = 1
        self.speed = 1
        self.image = king3_img
        # Releases iron coated purple blobs
        self.spawns = [(Enemy105, 100)]
        self.spawn_type = Enemy105
        self.spawn_count = 100
        self.size = 3
        self.value = self.health + sum(count * cls(path).value for cls, count in self.spawns)

    def spawn_func(self, enemies):
        points = self.generate_point_cloud(self.position, self.spawn_count, spread=100)
        kinds = [cls for cls, count in self.spawns for _ in range(count)]
        for cls, point in zip(kinds, points):
            enemy = cls(self.path, point, self.path_index)
            enemy.distance = self.distance
            enemies.append(enemy)


class TrollWagon(KingBlob):
    """Pulled along by armoured trolls; armoured trolls burst out when it breaks"""
    health = 750
    spawn = True
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.base_speed = 2  # same as the trolls pulling it
        self.speed = 2
        self.image = troll_wagon_img
        self.spawn_type = ArmoredTroll
        self.spawn_count = 30
        self.size = 3
        self.value = self.health + self.spawn_count * self.spawn_type(path).value
        self.puller = None

    def on_spawn(self, enemies):
        # Chained to the nearest armoured giant troll or wagon ahead on the same path
        ahead = [e for e in enemies if isinstance(e, (ArmoredGiantTroll, TrollWagon)) and e.path is self.path]
        self.puller = min(ahead, key=lambda e: e.distance) if ahead else None

    def facing(self):
        return 1 if self.image is troll_wagon_img else -1

    def draw(self, window):
        # Face the way it is going (keeps the last facing on up/down stretches)
        if self.path_index < len(self.path) - 1:
            dx = self.path[self.path_index + 1][0] - self.position[0]
            if dx > 0.5:
                self.image = troll_wagon_img
            elif dx < -0.5:
                self.image = troll_wagon_left_img
        self.draw_chain(window)
        super().draw(window)

    def draw_chain(self, window):
        """Chain from the hitch to the troll pulling the wagon, while that troll is alive and close"""
        puller = self.puller
        if puller is None or puller.health <= 0 or puller.reached_end:
            return
        start = (self.position[0] + 76 * self.facing(), self.position[1] + 28)  # hitch ring
        if isinstance(puller, TrollWagon):
            end = (puller.position[0] - 80 * puller.facing(), puller.position[1] + 28)  # back of the wagon ahead
        else:
            tx, ty = puller.position[0], puller.position[1] + 12  # troll's hands
            dx, dy = tx - start[0], ty - start[1]
            length = math.hypot(dx, dy)
            end = (tx - dx / length * 28, ty - dy / length * 28) if length > 28 else start  # stop at the troll's back
        if math.hypot(end[0] - start[0], end[1] - start[1]) > 120:
            return  # separated (e.g. glued) - chain would look wrong
        n = max(2, int(math.hypot(end[0] - start[0], end[1] - start[1]) / 8))
        for i in range(n + 1):
            x = start[0] + (end[0] - start[0]) * i / n
            y = start[1] + (end[1] - start[1]) * i / n
            # links alternate flat and upright; dark edge so they show on any background
            rect = (x - 6, y - 4, 12, 8) if i % 2 else (x - 4, y - 6, 8, 12)
            pygame.draw.ellipse(window, (30, 30, 35), pygame.Rect(rect).inflate(2, 2), 4)
            pygame.draw.ellipse(window, (175, 175, 185), rect, 3)


# Not sure if this should release meteors or big ghosts.
class StoneHead(KingBlob):
    health = 250
    spawn = True
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.base_speed = 1 #1.5
        self.speed = 1 #1.5
        self.image = stone_head_img
        #self.spawn_on_die = True
        self.spawn_type = Meteor
        self.spawn_count = 25
        self.size = 3
        #self.value = self.health + self.spawn_count*self.spawn_type.health
        self.value = self.health + self.spawn_count*Meteor.value
        ##print(self.value)

    #def recursive_value(self):
        #value = self.health
        #if self.spawn_on_die:
            #value += self.spawn_count * self.spawn_type.recursive_value()
        #return value


enemy_types = {1: Enemy, 2: Enemy2, 3: Enemy3, 4: Enemy4, 5: Enemy5,
               10: Ghost, 11: Troll, 12: GiantTroll, 13: Devil, 14: BigGhost, 15: Meteor, 16: BigDevil,
               17: ArmoredTroll, 18: ArmoredGiantTroll,
               19: BlackMeteor,
               6: Enemy6,
               101: Enemy101, 102: Enemy102, 103: Enemy103, 104: Enemy104, 105:Enemy105, 106: Enemy106,
               110: StoneHead, 120: TrollWagon,
               201: KingBlob, 301: KingBlob2, 401: KingBlob3}
