import pygame
import sounds
import random

ghost_img = pygame.image.load('images/ghost.png')
ghost_img = pygame.transform.scale(ghost_img, (50, 50))
big_ghost_img = pygame.transform.scale(ghost_img, (70, 70))
devil_img = pygame.image.load('images/devil.png')
devil_img = pygame.transform.scale(devil_img, (50, 50))
bigdevil_img = pygame.transform.scale(devil_img, (75, 75))
troll_img = pygame.image.load('images/troll.png')
troll_img = pygame.transform.scale(troll_img, (50, 50))
giant_troll_img = pygame.transform.scale(troll_img, (90, 90))
king_img = pygame.image.load('images/kingblob.png')
king_img = pygame.transform.scale(king_img, (100, 100))
king2_img = pygame.image.load('images/kingblob_green.png')
king2_img = pygame.transform.scale(king2_img, (110, 110))
burger_king_img = pygame.image.load('images/burger_king.png')
burger_king_img = pygame.transform.scale(burger_king_img, (120, 120))

armored_troll_img = pygame.image.load('images/armored_troll.png')
armored_troll_img = pygame.transform.scale(armored_troll_img, (60, 60))
giant_armored_troll_img = pygame.transform.scale(armored_troll_img, (100, 100))


class Enemy:
    health = 1
    spawn = False
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

    def glue_reset(self):
        self.slow_factor = 1
        self.glued = 0
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
                w = self.fort_health
                # could be same size or bigger to go round outside
                pygame.draw.circle(window, (150, 121, 105), (int(x), int(y)), 10+w, w)
            else:
                pygame.draw.circle(window, (0, 0, 0), (int(x), int(y)), 11, 1)
        if self.glued:
            self.draw_glue_splat(window, self.glue_color, x, y, self.size)
            if self.toxic_glued:
                if self.toxic_attacks > 1:
                    random.seed(1)
                    for splat in range(1, self.toxic_attacks+1):

                        # Hack try make king blob look better
                        if isinstance(self, KingBlob):
                            xn = x + random.randint(-25, 25)
                            yn = y + random.randint(-5, 30)
                        else:
                            xn = x + random.randint(-15, 15)
                            yn = y + random.randint(-15, 15)

                        self.draw_glue_splat(window, self.glue_color, xn, yn, self.size)

    def move(self):
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

    def take_damage(self, damage):
        score = min(self.health, damage)  # Make sure don't score more than remaining health
        self.health -= damage
        self.value -= damage
        if self.fortified and self.fort_health > 0:
            self.fort_health -= damage
            sounds.play('ting')
        else:
            sounds.play('blop')
        if self.health <= 0:
            self.reached_end = True  # Treat the enemy as "dead" or "reached the end"
        return score

    def spawn_func(self, enemies):
        for i in range(self.spawn_count):
            enemy = self.spawn_type(self.path, self.position, self.path_index)
            # Spread out slightly
            for j in range(i*2):
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
           score = self.take_damage(self.toxic_attacks)
           self.toxic_glued_by.total_score += score  # if tower is sold - obj still exists but not in tower list
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
                self.glued -= 1
            else:
                self.glue_reset()
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
                self.glued -= 1
            else:
                self.glue_reset()
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
                self.glued -= 1
            else:
                self.glue_reset()
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
                self.glued -= 1
            else:
                self.glue_reset()
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
    health = 15
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.fortified = True
        self.fort_health = 10


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
        sounds.play('blop')
        if self.health <= 0:
            self.reached_end = True
        return score


class ArmoredTroll(Troll):
    health = 70
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
    health = 60
    spawn = True
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.base_speed = 2
        self.speed = 2
        self.image = giant_troll_img
        #self.spawn_on_die = True
        self.spawn_type = Enemy103
        self.spawn_count = 6
        self.size = 3
        self.value = self.health + self.spawn_count*self.spawn_type.health


class ArmoredGiantTroll(GiantTroll):
    health = 220
    spawn = True
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.image = giant_armored_troll_img
        self.spawn_count = 25
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


# Not sure if this should release meteors or big ghosts.
class BurgerKing(KingBlob):
    health = 200
    spawn = True
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.base_speed = 1 #1.5
        self.speed = 1 #1.5
        self.image = burger_king_img  # could be 5th level burger - but here an enemy
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
               101: Enemy101, 102: Enemy102, 103: Enemy103, 104: Enemy104, 105:Enemy105,
               110: BurgerKing,
               201: KingBlob, 301: KingBlob2}
