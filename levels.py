# Dictionaries or classes

from enemy import enemy_types

class Level():
    def __init__(self):
        self.num_spawned = 0
        self.phase = 0
        #self.done = False

    def done(self):
        return self.num_spawned >= self.num_enemies

    def interval(self):
        #return self.interval
        return self.spawn_intervals[self.phase]

    def update(self):
        self.num_spawned += 1
        #print(f"{self.num_spawned=}")
        if self.num_spawned >= self.phase_counts[self.phase]:
            self.phase += 1
            #print(f"{self.phase=}")

    def spawn_enemy(self, enemies, path):
        enemy_id = self.enemy_types[self.phase]
        enemy_class = enemy_types[enemy_id]
        enemies.append(enemy_class(path))


class Level1(Level):
    def __init__(self):
        Level.__init__(self)
        # This means 10 bloons at spawn interval of 40 and another 10 at interval of 15
        self.level_id = 1
        self.num_enemies = 20
        self.spawn_intervals = [40, 15]
        self.phase_counts = [10, 20]  # How many in each phase - no currently accum at end of each phase
        self.enemy_types = [1, 1, 1]


class Level2(Level):
    def __init__(self):
        Level.__init__(self)
        self.level_id = 2
        self.num_enemies = 30
        self.spawn_intervals = [30, 8]
        self.phase_counts = [20, 30]  # How many in each phase - no currently accum at end of each phase
        self.enemy_types = [1, 1, 1]


class Level3(Level):
    def __init__(self):
        Level.__init__(self)
        self.level_id = 3
        self.num_enemies = 30
        self.spawn_intervals = [25, 5, 15]
        self.phase_counts = [10, 20, 30]  # How many in each phase - no currently accum at end of each phase
        self.enemy_types = [2, 1, 1]


class Level4(Level):
    def __init__(self):
        Level.__init__(self)
        self.level_id = 4
        self.num_enemies = 30
        self.spawn_intervals = [20, 20, 12]
        self.phase_counts = [10, 20, 30]  # How many in each phase - no currently accum at end of each phase
        self.enemy_types = [1, 2, 2]

class Level5(Level):
    def __init__(self):
        Level.__init__(self)
        self.level_id = 5
        self.num_enemies = 30
        self.spawn_intervals = [20, 20, 20]
        self.phase_counts = [10, 20, 30]  # How many in each phase - no currently accum at end of each phase
        self.enemy_types = [1, 2, 3]

class Level6(Level):
    def __init__(self):
        Level.__init__(self)
        self.level_id = 6
        self.num_enemies = 6
        self.spawn_intervals = [20]
        self.phase_counts = [6]  # How many in each phase - no currently accum at end of each phase
        self.enemy_types = [10]  # TODO ghosts will need magic attacks to kill or some such

class Level7(Level):
    def __init__(self):
        Level.__init__(self)
        self.level_id = 7
        self.num_enemies = 35
        self.spawn_intervals = [10, 20, 14]
        self.phase_counts = [10, 22, 35]
        self.enemy_types = [1,2,2]

class Level8(Level):
    def __init__(self):
        Level.__init__(self)
        self.level_id = 8
        self.num_enemies = 25
        self.spawn_intervals = [25, 15]
        self.phase_counts = [15, 25]
        self.enemy_types = [3,3]

class Level9(Level):
    def __init__(self):
        Level.__init__(self)
        self.level_id = 9
        self.num_enemies = 12
        self.spawn_intervals = [15]
        self.phase_counts = [12]
        self.enemy_types = [4]

class Level10(Level):
    def __init__(self):
        Level.__init__(self)
        self.level_id = 10
        self.num_enemies = 50
        self.spawn_intervals = [25, 15, 8]
        self.phase_counts = [20, 32, 50]
        self.enemy_types = [2,2,2]

class Level11(Level):
    def __init__(self):
        Level.__init__(self)
        self.level_id = 11
        self.num_enemies = 60
        self.spawn_intervals = [6, 12, 15, 12]
        self.phase_counts = [15, 30, 45, 60]
        self.enemy_types = [2,1,3,4]


# TODO auto-add
levels = {1: Level1, 2: Level2, 3: Level3, 4: Level4, 5: Level5, 6: Level6, 7: Level7, 8: Level8, 9: Level9, 10: Level10, 11: Level11}
max_level = 11
