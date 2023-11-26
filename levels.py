# Dictionaries or classes

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



class Level1(Level):
    def __init__(self):
        Level.__init__(self)
        # This means 10 bloons at spawn interval of 40 and another 10 at interval of 15
        self.level_id = 1
        self.num_enemies = 20
        self.spawn_intervals = [40, 15]
        self.phase_counts = [10, 20]  # How many in each phase - no currently accum at end of each phase
        #self.interval = self.spawn_intervals[0]


class Level2(Level):
    def __init__(self):
        Level.__init__(self)
        # This means 10 bloons at spawn interval of 40 and another 10 at interval of 15
        self.level_id = 2
        self.num_enemies = 30
        self.spawn_intervals = [30, 8]
        self.phase_counts = [20, 30]  # How many in each phase - no currently accum at end of each phase
        #self.interval = self.spawn_intervals[0]


class Level3(Level):
    def __init__(self):
        Level.__init__(self)
        # This means 10 bloons at spawn interval of 40 and another 10 at interval of 15
        self.level_id = 3
        self.num_enemies = 30
        self.spawn_intervals = [25, 5, 15]
        self.phase_counts = [10, 20, 30]  # How many in each phase - no currently accum at end of each phase
        #self.interval = self.spawn_intervals[0]


levels = {1: Level1, 2: Level2, 3: Level3}
max_level = 3
