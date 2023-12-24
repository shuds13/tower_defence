import pygame
import sounds
import random

ghost_img = pygame.image.load('ghost.png')
ghost_img = pygame.transform.scale(ghost_img, (50, 50))
big_ghost_img = pygame.transform.scale(ghost_img, (70, 70))

devil_img = pygame.image.load('devil.png')
devil_img = pygame.transform.scale(devil_img, (50, 50))

troll_img = pygame.image.load('troll.png')
troll_img = pygame.transform.scale(troll_img, (50, 50))
giant_troll_img = pygame.transform.scale(troll_img, (90, 90))
king_img = pygame.image.load('kingblob.png')
king_img = pygame.transform.scale(king_img, (100, 100))
king2_img = pygame.image.load('kingblob_green.png')
king2_img = pygame.transform.scale(king2_img, (110, 110))

# TODO may not need value and health - will they always be the same?
# may make enemy0 as way of making a gap - inivisible no value etc...

class Enemy:
    def __init__(self, path, position=None, path_index=0):
        self.path = path
        self.path_index = path_index
        #self.position = self.path[0]


        self.base_speed = 2  # help with things like gluing from a stronger glue gunner
        self.speed = 2
        #self.base_speed = 1  # TESTING
        #self.speed = 1


        self.reached_end = False  # Indicates if the enemy has reached the end of the path
        self.health = 1
        self.value = 1
        self.color = (255, 0, 0)
        self.image = None
        self.invis = False
        self.fortified = False
        self.spawn_on_die = False  # not used for regular colors - those change attributes.
        self.position = position or self.path[0]
        self.size = 1
        self.slowable = True
        self.glue_reset()

    def glue_reset(self):
        self.slow_factor = 1
        self.glued = 0
        self.glue_color = None
        self.toxic_glued = False
        self.toxic_glued_by = None
        self.toxic_timer = None
        self.toxic_time = None
        self.toxic_attacks = 0


    def draw_glue_splat(self, window, color, x, y, esize):
        #print(f'drawing splat at {x} {y}')
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
                #print('yes toxic glued')
                #print(f"{self.toxic_attacks=}")
                if self.toxic_attacks > 1:
                    #import pdb;pdb.set_trace()
                    #print('yes attacks more tha ne')
                    # check if effects other things -like wizard lightning.
                    random.seed(1)
                    for splat in range(1, self.toxic_attacks+1):

                        # Hack try make king blob look better
                        if isinstance(self, KingBlob):
                            xn = x + random.randint(-25, 25)
                            yn = y + random.randint(-5, 30)
                        else:
                            xn = x + random.randint(-15, 15)
                            yn = y + random.randint(-15, 15)

                        #x += splat * 5 * factor
                        #y += splat * 5 * factor
                        self.draw_glue_splat(window, self.glue_color, xn, yn, self.size)
                        # or make it grow bigger?
                    #TODO STILL got to do correct damage
                #self.toxic_attacks += 1


    def move(self):
        # Move towards the next point in the path
        if self.path_index < len(self.path) - 1:
            #target_pos = target or self.path[self.path_index + 1]  # for backwards move just make -1
            target_pos = self.path[self.path_index + 1]  # for backwards move just make -1

            dx, dy = target_pos[0] - self.position[0], target_pos[1] - self.position[1]
            distance = (dx**2 + dy**2)**0.5
            if distance > self.speed:
                dx, dy = dx / distance * self.speed, dy / distance * self.speed
            self.position = (self.position[0] + dx, self.position[1] + dy)

            # Check if the enemy has reached the target position
            if abs(self.position[0] - target_pos[0]) < self.speed and abs(self.position[1] - target_pos[1]) < self.speed:
                self.path_index += 1

        # Check if the enemy has reached the end of the path
        if self.path_index >= len(self.path) - 1:
            self.reached_end = True

    def take_damage(self, damage):
        score = min(self.health, damage)  # Make sure don't score more than remaining health
        self.health -= damage
        if self.fortified and self.fort_health > 0:
            self.fort_health -= damage
            sounds.play('ting')
        else:
            sounds.play('blop')
        #print('eememy hit')
        if self.health <= 0:
            #print('en reached end')
            self.reached_end = True  # Treat the enemy as "dead" or "reached the end"
        return score

    def spawn_func(self, enemies):
        for i in range(self.spawn_count):
            #print(self.path_index)
            enemy = self.spawn_type(self.path, self.position, self.path_index)
            # Spread out slightly
            # not clear to see if just one apart - might help if I draw circle round them (as already do for fortified)
            for j in range(i*2):
                enemy.move()
            enemies.append(enemy)  # Also puts on end - so will not attack first!

    ## create a cloud like he burst that then move to the track
    #def cloud_spawn(self):
        ## Move towards the next point in the path
        #if self.path_index < len(self.path) - 1:
            #target_pos = self.position
            #self.move(target_pos)

    # TODO - NEED TO MAKE SAME CHANGE FOR MIN
    def toxic_damage(self):
        if self.glued <= 0:
            self.glue_reset()
            #self.toxic_glued = False
            #self.toxic_glued_by = None
            #self.toxic_timer = None
            #self.toxic_time = None
            #print('glued < 0')
            return 0
        score = 0
        if self.toxic_timer > 0:
            self.toxic_timer -= 1
        else:
           #self.toxic_attacks += 1
           score = self.take_damage(self.toxic_attacks)  # damage could be variable also
           self.toxic_glued_by.total_score += score  # what if tower is sold - guess obj still exists but not in tower list
           self.toxic_timer = self.toxic_time
        return score


class Enemy2(Enemy):
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.health = 2
        self.value = 2

        self.base_speed = 3
        self.speed = 3
        #self.base_speed = 1.5  # TESTING
        #self.speed = 1.5

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
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.health = 3
        self.value = 3
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
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.health = 4
        self.value = 4
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
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.health = 5
        self.value = 5
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

# next put circle round outside to be fortified...
# or maybe whole thing fortified look - can crack

# maybe should be an option in Enemy1
class Enemy101(Enemy):
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.fortified = True
        self.fort_health = 3
        self.health += self.fort_health
        self.value = self.health

class Enemy102(Enemy2):
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.fortified = True
        self.fort_health = 4
        self.health += self.fort_health
        self.value = self.health

class Enemy103(Enemy3):
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.fortified = True
        self.fort_health = 5
        self.health += self.fort_health
        self.value = self.health

class Enemy104(Enemy4):
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.fortified = True
        self.fort_health = 6
        self.health += self.fort_health
        self.value = self.health

class Ghost(Enemy):
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.health = 2
        self.value = 2
        self.base_speed = 3
        self.speed = 3
        self.image = ghost_img
        self.invis = True

    # TODO - is this needed - check difference to original function
    def take_damage(self, damage):
        score = min(self.health, damage)
        self.health -= damage
        self.value = self.health
        sounds.play('blop')
        if self.health <= 0:
            self.reached_end = True
        return score

class BigGhost(Ghost):
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.health = 20
        self.value = 20
        self.base_speed = 3
        self.speed = 3
        self.image = big_ghost_img
        self.spawn_on_die = True
        self.spawn_type = Ghost
        self.spawn_count = 8

class Devil(Ghost):
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.health = 8
        self.value = 8
        self.base_speed = 4
        self.speed = 4
        self.image = devil_img
        self.size = 2


class Troll(Enemy):
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.health = 20
        self.value = 20
        self.base_speed = 2
        self.speed = 2
        self.image = troll_img
        self.spawn_on_die = True
        self.spawn_type = Enemy3
        self.spawn_count = 3
        self.size = 2

    # TODO - is this needed - check difference to original function
    def take_damage(self, damage):
        score = min(self.health, damage)
        self.health -= damage
        self.value = self.health
        sounds.play('blop')
        if self.health <= 0:
            self.reached_end = True
        return score


class GiantTroll(Troll):
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.health = 60
        self.value = 60
        self.base_speed = 2
        self.speed = 2
        self.image = giant_troll_img
        self.spawn_on_die = True
        self.spawn_type = Enemy103
        self.spawn_count = 6
        self.size = 3
        #self.slowable = False


class Meteor(Enemy):
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.health = 10
        self.value = 10

        self.base_speed = 8
        #self.base_speed = 2 # tmp for testing
        self.speed = self.base_speed

        self.spawn_on_die = True
        self.spawn_type = Enemy4
        self.spawn_count = 5
        self.size = 2
        self.color =  (193, 154, 107) #(150, 121, 105)
        self.fortified = True
        self.fort_health = self.health


class KingBlob(Enemy):
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.health = 100 #200
        self.value = 100 #200
        self.base_speed = 1
        self.speed = 1
        self.image = king_img
        self.spawn_on_die = True
        #self.spawn_type = Enemy102
        self.spawn_type = Enemy2 #proper one
        #self.spawn_type = Ghost
        #self.spawn_count = 20
        self.spawn_count = 100
        self.size = 3
        #self.slowable = False

    # TODO - is this needed - check difference to original function
    def take_damage(self, damage):
        score = min(self.health, damage)
        self.health -= damage
        self.value = self.health
        sounds.play('blop')
        if self.health <= 0:
            sounds.play('pop')
            self.reached_end = True
        return score

    def generate_point_cloud(self, central_point, n_points, spread=1.0):
        """
        Generates a cloud of 2D points around a central point.

        :param central_point: A tuple (x, y) representing the central point.
        :param n_points: Number of points to generate.
        :param spread: The range around the central point for generating points.
        :return: A list of tuples, each representing a point (x, y).
        """
        x_center, y_center = central_point
        return [(x_center + random.uniform(-spread, spread),
                y_center + random.uniform(-spread, spread)) for _ in range(n_points)]

    def spawn_func(self, enemies):
        points = self.generate_point_cloud(self.position, self.spawn_count, spread=100)

        for point in points:
            #print(self.path_index)
            enemy = self.spawn_type(self.path, point, self.path_index)
            # Spread out slightly
            # not clear to see if just one apart - might help if I draw circle round them (as already do for fortified)
            #for j in range(i*2):
                ##enemy.move(self.position)  #may not need this function
                #enemy.move()
                ##enemy.cloud_spawn()
            enemies.append(enemy)


class KingBlob2(KingBlob):
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.health = 200
        self.value = 200
        self.base_speed = 1
        self.speed = 1
        self.image = king2_img
        self.spawn_on_die = True
        self.spawn_type = Enemy3
        self.spawn_count = 150
        self.size = 3

#class Ghost2(Enemy):
    #def __init__(self, path, position=None, path_index=0):
        #super().__init__(path, position, path_index)
        #self.health = 6
        #self.value = 6
        #self.base_speed = 3
        #self.speed = 3
        #self.image = ghost_img2
        #self.invis = True


# Idea is you kill heart you get lives.
# but in play - would be to send in a player object, so can update lives instead of money.
# ie. not yet usable - also need heart image.
class Heart(Enemy):
    def __init__(self, path, position=None, path_index=0):
        super().__init__(path, position, path_index)
        self.health = 5
        self.value = 10  #testing a diff value
        self.base_speed = 4
        self.speed = 4
        #self.color = (127, 0, 255)

    def take_damage(self, damage):
        self.health -= damage
        #self.value = self.health
        sounds.play('blop')
        if self.health <= 0:
            self.reached_end = True
            return self.value  # but will be lives
        return 0

enemy_types = {1: Enemy, 2: Enemy2, 3: Enemy3, 4: Enemy4, 5: Enemy5,
               10: Ghost, 11: Troll, 12: GiantTroll, 13: Devil, 14: BigGhost, 15: Meteor,
               101: Enemy101, 102: Enemy102, 103: Enemy103, 104: Enemy104,
               201: KingBlob, 301: KingBlob2}
