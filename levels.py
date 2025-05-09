# Dictionaries or classes

from enemy import enemy_types

class Level():
    def __init__(self):
        self.num_spawned = 0
        self.phase = 0

    def done(self):
        return self.num_spawned >= self.num_enemies

    def interval(self):
        return self.spawn_intervals[self.phase]

    # TODO this can be combined into spawn_enemy now.
    def update(self):
        self.num_spawned += 1
        if self.num_spawned >= self.phase_counts[self.phase]:
            self.phase += 1

    def spawn_enemy(self, enemies, path):
        enemy_id = self.enemy_types[self.phase]
        enemy_class = enemy_types[enemy_id]
        enemies.append(enemy_class(path))


class Level1(Level):
    def __init__(self):
        Level.__init__(self)
        # This means 10 bloons at spawn interval of 40 and another 10 at interval of 15
        self.num_enemies = 20
        self.spawn_intervals = [40, 15]
        self.phase_counts = [10, 20]  # Accum number at end of each phase
        self.enemy_types = [1, 1, 1]

class Level2(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 30
        self.spawn_intervals = [30, 8]
        self.phase_counts = [20, 30]
        self.enemy_types = [1, 1, 1]

class Level3(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 30
        self.spawn_intervals = [25, 5, 15]
        self.phase_counts = [10, 20, 30]
        self.enemy_types = [2, 1, 1]

class Level4(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 30
        self.spawn_intervals = [20, 20, 15]
        self.phase_counts = [10, 20, 30]
        self.enemy_types = [1, 2, 2]

# tried swapping 5 and 6 so greens on round 6
class Level5(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 35
        self.spawn_intervals = [10, 20, 14]
        self.phase_counts = [10, 22, 35]
        self.enemy_types = [1,2,2]

class Level6(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 30
        self.spawn_intervals = [20, 20, 25]
        self.phase_counts = [10, 20, 30]
        self.enemy_types = [1, 2, 3]

class Level7(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 35
        self.spawn_intervals = [12, 15, 9]
        self.phase_counts = [12, 25, 35]
        self.enemy_types = [2,1,1]

class Level8(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 30
        self.spawn_intervals = [16, 6]
        self.phase_counts = [15, 30]
        self.enemy_types = [2,1]

class Level9(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 25
        self.spawn_intervals = [25, 13]
        self.phase_counts = [15, 25]
        self.enemy_types = [3,3]

class Level10(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 12
        self.spawn_intervals = [15]
        self.phase_counts = [12]
        self.enemy_types = [4]

class Level11(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 50
        self.spawn_intervals = [25, 15, 8]
        self.phase_counts = [20, 32, 50]
        self.enemy_types = [2,2,2]


class Level12(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 25
        self.spawn_intervals = [20, 15, 10]
        self.phase_counts = [2, 10, 25]
        self.enemy_types = [10,2,1]  # TODO ghosts will need magic attacks to kill or some such


class Level13(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 60
        self.spawn_intervals = [6, 12, 15, 12]
        self.phase_counts = [15, 30, 45, 60]
        self.enemy_types = [2,1,3,4]

class Level14(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 50
        self.spawn_intervals = [4, 8, 20]
        self.phase_counts = [22, 35, 50]
        self.enemy_types = [2,1,3]

class Level15(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 20
        self.spawn_intervals = [12]
        self.phase_counts = [20]
        self.enemy_types = [4]

#so confused now need to stop - i thought copied this to 18 - but thats got diff enemy count WTF!
#class Level14(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 45
        #self.spawn_intervals = [18, 12, 10]
        #self.phase_counts = [20, 33, 45]
        #self.enemy_types = [3, 10, 2]

class Level16(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 6
        self.spawn_intervals = [20]
        self.phase_counts = [6]
        self.enemy_types = [10]  # TODO ghosts will need magic attacks to kill or some such

#fix this - its somehow copy of level 5 - WTF!
class Level17(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 30
        self.spawn_intervals = [20, 20, 20]
        self.phase_counts = [10, 20, 30]
        self.enemy_types = [1, 2, 3]

class Level18(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 8
        self.spawn_intervals = [20]
        self.phase_counts = [8]
        self.enemy_types = [5]

class Level19(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 80
        self.spawn_intervals = [18, 12, 10]
        self.phase_counts = [20, 33, 80]
        self.enemy_types = [3, 10, 2]

class Level20(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 20
        self.spawn_intervals = [20]
        self.phase_counts = [20]
        self.enemy_types = [101]

class Level21(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 50
        self.spawn_intervals = [20, 2, 10]
        self.phase_counts = [15, 30, 50]
        self.enemy_types = [4, 1, 3]

# Test level - just to try and beat 4th level (gold) Fighter with current strenght
class Level22(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 80
        self.spawn_intervals = [5]
        self.phase_counts = [80]
        self.enemy_types = [3]

class Level23(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 50
        self.spawn_intervals = [15, 18]
        self.phase_counts = [25, 50]
        self.enemy_types = [2, 102]

class Level24(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 50
        self.spawn_intervals = [4, 8, 20]
        self.phase_counts = [22, 35, 50]
        self.enemy_types = [3,2,4]

class Level25(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 50
        self.spawn_intervals = [14,14]
        self.phase_counts = [20, 50]
        self.enemy_types = [2, 10]

# Test dense reds or blues
class Level26(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 80
        self.spawn_intervals = [3]
        self.phase_counts = [80]
        self.enemy_types = [2]

class Level27(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 125
        self.spawn_intervals = [4,4,4,5]
        self.phase_counts = [40, 70, 100, 125]
        self.enemy_types = [1,2,3,4]

class Level28(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 55
        self.spawn_intervals = [15, 8]
        self.phase_counts = [25, 55]
        self.enemy_types = [103, 10]

class Level29(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 100
        self.spawn_intervals = [10, 8, 1, 10]
        self.phase_counts = [25, 55, 80, 100]
        self.enemy_types = [5, 3, 1, 102]

class Level30(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 8
        self.spawn_intervals = [35]
        self.phase_counts = [8]
        self.enemy_types = [11]

class Level31(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 90
        self.spawn_intervals = [8,6,3]
        self.phase_counts = [30, 60, 90]
        self.enemy_types = [4,4,4]


class Level32(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 40
        self.spawn_intervals = [12]
        self.phase_counts = [40]
        self.enemy_types = [5]


class Level33(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 3
        self.spawn_intervals = [30]
        self.phase_counts = [3]
        self.enemy_types = [15]

#class Level33(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 75
        #self.spawn_intervals = [1, 10, 20]
        #self.phase_counts = [25, 50, 75]
        #self.enemy_types = [2, 102, 104]

class Level34(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 51
        self.spawn_intervals = [2, 3, 10, 20]
        self.phase_counts = [22, 35, 50, 51]
        self.enemy_types = [3,2,4, 13]

class Level35(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 50
        self.spawn_intervals = [14,14]
        self.phase_counts = [20, 50]
        self.enemy_types = [2, 10]

# Test dense reds or blues
class Level36(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 80
        self.spawn_intervals = [3]
        self.phase_counts = [80]
        self.enemy_types = [102]

class Level37(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 150
        self.spawn_intervals = [2,2,3,3,4]
        self.phase_counts = [40, 70, 100, 125, 150]
        self.enemy_types = [1,2,3,4,5]

# before money per hit reduction
#class Level38(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 47
        #self.spawn_intervals = [8, 10, 10, 10, 10]
        #self.phase_counts = [25, 35, 36, 46, 47]
        #self.enemy_types = [3, 11, 12, 11, 12]

# oroginal - currently too hard - but may reinstate if tower like bomb shooter helps or money maker tower.
#class Level38(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 47
        #self.spawn_intervals = [8, 15, 32, 32, 14, 32]
        #self.phase_counts = [25, 35, 36, 37, 46, 47]
        #self.enemy_types = [3, 11, 12, 11, 11, 12]


class Level38(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 64
        self.spawn_intervals = [8, 22, 10, 30, 20]
        self.phase_counts = [25, 35, 46, 55, 64]
        self.enemy_types = [3, 11, 10, 13, 11]


class Level39(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 125
        self.spawn_intervals = [6, 3, 1, 1, 10]
        self.phase_counts = [25, 55, 80, 100, 125]
        self.enemy_types = [5, 3, 1, 3, 102]


class Level40(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 1
        self.spawn_intervals = [1] # Irrelevant
        self.phase_counts = [1]
        self.enemy_types = [201]


class Level41(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 100
        self.spawn_intervals = [4, 8, 1, 2]
        self.phase_counts = [25, 55, 80, 100]
        self.enemy_types = [2, 3, 2, 3]


class Level42(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 100
        self.spawn_intervals = [2] # Irrelevant
        self.phase_counts = [100]
        self.enemy_types = [4]


class Level43(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 110
        self.spawn_intervals = [6, 2, 5, 2, 4, 2]
        self.phase_counts = [30,  40, 60,  70, 90, 110]
        self.enemy_types =  [2,  103,  2, 103,  2, 103]


class Level44(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 15
        self.spawn_intervals = [20]
        self.phase_counts = [15]
        self.enemy_types =  [13]

# old level 38 - still too hard here.
#class Level45(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 47
        #self.spawn_intervals = [8, 15, 32, 32, 14, 32]
        #self.phase_counts = [25, 35, 36, 37, 46, 47]
        #self.enemy_types = [3, 11, 12, 11, 11, 12]

class Level45(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 48 # 47
        self.spawn_intervals = [8, 20, 40, 40, 18, 40]
        #self.phase_counts = [25, 35, 36, 37, 46, 47]
        #self.enemy_types = [3, 11, 12, 11, 11, 12]
        self.phase_counts = [25, 35, 36, 37, 46, 48]
        self.enemy_types = [3, 11, 17, 11, 11, 17]  # changed giant to armoroed trolls

class Level46(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 40
        self.spawn_intervals = [3, 20]
        self.phase_counts = [30, 40]
        self.enemy_types = [10, 14]

# This is hard - may make easier - or keep as one of those levels - not proven on Valley
# but may be able to do it with the 4th tier wizard.
class Level47(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 350
        self.spawn_intervals = [1,3,1,2,2,3]  # may slow down last phase - interval or number.
        self.phase_counts = [100, 150, 200, 250, 300, 350]
        self.enemy_types = [2, 102, 3, 103, 4, 104]

# test levels
#class Level46(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 4
        #self.spawn_intervals = [100, 100, 200]
        #self.phase_counts = [2,3,4]
        #self.enemy_types = [11, 12, 201]

#class Level47(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 15
        #self.spawn_intervals = [15,15]
        #self.phase_counts = [10,15]
        #self.enemy_types = [10, 13]

class Level48(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 35
        self.spawn_intervals = [15,15,15,10]
        self.phase_counts = [10, 20, 25, 35]
        self.enemy_types = [2, 10, 13, 102]

class Level49(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 35
        self.spawn_intervals = [15,15,30, 15]
        self.phase_counts = [10,20,21, 35]
        self.enemy_types = [10, 13, 201, 13]


#class Level50(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 2
        #self.spawn_intervals = [30]
        #self.phase_counts = [3]
        #self.enemy_types = [201]


class Level50(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 50
        self.spawn_intervals = [15, 3, 80, 12]
        self.phase_counts = [15, 40, 41, 50]
        self.enemy_types = [15, 3, 15, 15]

#class Level50(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 20
        #self.spawn_intervals = [8,15]
        #self.phase_counts = [10,20]
        #self.enemy_types = [2, 10]

class Level51(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 200
        self.spawn_intervals = [2]
        self.phase_counts = [200]
        self.enemy_types = [5]

#class Level52(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 51
        #self.spawn_intervals = [8, 15, 30, 30, 12, 20, 25]
        #self.phase_counts = [25, 35, 36, 37, 46, 50, 51]
        #self.enemy_types = [103, 11, 12, 11, 11, 12, 201]

class Level52(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 55
        self.spawn_intervals = [8,   15, 50, 30,   30, 12, 50, 20, 50]
        self.phase_counts =    [25,  35, 36, 39,   40, 49, 50, 54, 55]
        self.enemy_types =     [103, 11, 17, 17,   11, 11, 17, 17, 12] # switch end to giant troll

# I want to introduc metors earlier like cermics - but they are very fast.
class Level53(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 160
        self.spawn_intervals = [3, 3, 1, 12, 3]
        self.phase_counts = [30, 45, 90, 130, 160]
        self.enemy_types = [3, 10, 2, 14, 5]

class Level54(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 250
        self.spawn_intervals = [2, 4, 12, 2, 4, 10, 2, 4, 9]
        self.phase_counts = [30, 60, 80, 110, 140, 160, 190, 220, 250]
        self.enemy_types = [3, 103, 15, 3, 103, 15, 3, 103, 15]

class Level55(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 4
        self.spawn_intervals = [30]
        self.phase_counts = [4]
        self.enemy_types = [201]

class Level56(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 150
        self.spawn_intervals = [3, 3, 1, 1, 5]
        self.phase_counts = [25, 55, 80, 100, 150]
        self.enemy_types = [5, 3, 1, 3, 102]

#class Level57(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 55
        #self.spawn_intervals = [8, 18, 30, 12, 20, 18]
        #self.phase_counts = [35, 38, 39, 46, 48, 55]
        #self.enemy_types = [11, 12, 11, 11, 12, 15]

class Level57(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 55
        self.spawn_intervals = [8, 22, 30, 12, 20, 18]
        self.phase_counts = [35, 38, 39, 46, 48, 55]
        self.enemy_types = [11, 12, 11, 11, 12, 15]

class Level58(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 350
        self.spawn_intervals = [1,3,1,2,2,1]  # may slow down last phase - interval or number.
        self.phase_counts = [100, 150, 200, 250, 300, 350]
        self.enemy_types = [2, 102, 3, 103, 4, 102]


# modified since testing RBE
class Level59(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 50
        self.spawn_intervals = [5,5,4,40,4]
        self.phase_counts = [10, 20, 40, 41, 50]
        self.enemy_types = [15, 14, 13, 15, 15]

class Level60(Level):
    def __init__(self):
        Level.__init__(self)
        self.num_enemies = 1
        self.spawn_intervals = [1]
        self.phase_counts = [1]
        self.enemy_types = [301]

#class Level61(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 150
        #self.spawn_intervals = [4,  40,  4,   40,  4,   40,  1,   40,  1]
        #self.phase_counts =    [40, 41,  60,  61,  100, 101, 130, 131, 150]
        #self.enemy_types =     [5,  103, 103, 105, 105, 104, 104, 105, 105]

## Troll army
#class Level62(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 194
        #self.spawn_intervals = [3,   12,  30,  15,  30,  10,  30,  15]
        #self.phase_counts =    [100, 135, 136, 142, 143, 183, 184, 194]
        #self.enemy_types =     [3,   11,  12,  12,  11,  11,  12,  12]

#class Level63(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 1
        #self.spawn_intervals = [1]
        #self.phase_counts = [1]
        #self.enemy_types = [110]

#class Level64(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 475
        #self.spawn_intervals = [2,  3,   3,  2,   4,   3,   2,   30,  60,   3,   2]
        #self.phase_counts =    [30, 60,  90, 140, 200, 250, 290, 291, 292,  400, 475]
        #self.enemy_types =     [3,  103, 15, 10,  103, 15,  3,   301, 103,  103, 15]

#class Level65(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 4
        #self.spawn_intervals = [30]
        #self.phase_counts = [4]
        #self.enemy_types = [301]

#class Level66(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 270
        #self.spawn_intervals = [2,   3,   6,   4,   3,   7]
        #self.phase_counts =    [100, 120, 150, 200, 260, 270]
        #self.enemy_types =     [5,   10,  14,  13,  4,   16]

#class Level67(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 300
        #self.spawn_intervals = [1,   3,   1,   5,   40,  20,  10]
        #self.phase_counts =    [100, 150, 200, 240, 241, 270, 300]
        #self.enemy_types =     [2,   102, 3,   11,  17,  17,  17]

#class Level68(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 100
        #self.spawn_intervals = [6,  5,  40, 18 ]
        #self.phase_counts =    [40, 80, 81, 100 ]
        #self.enemy_types =     [15, 3,  19, 19 ]

#class Level69(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 210
        #self.spawn_intervals = [5,  5,   12,  40,  14,  40,  30,  15,  60,  40,  20,  80,  20]
        #self.phase_counts =    [40, 80,  100, 101, 150, 151, 165, 175, 176, 180, 200, 201, 210]
        #self.enemy_types =     [3,  103, 11,  17,  17,  12,  12,  12,  18,  18,  17,  18,  18]

#class Level70(Level):
    #def __init__(self):
        #Level.__init__(self)
        #self.num_enemies = 4
        #self.spawn_intervals = [40]
        #self.phase_counts = [4]
        #self.enemy_types = [110]


max_level = 60  # TODO get this from last key in levels

levels = {i: globals()[f'Level{i}'] for i in range(1, max_level+1)}
