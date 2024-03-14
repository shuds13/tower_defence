import copy
import pygame
import sounds
from accounts import Account, load_profile
from tower import Totem, tower_types


# tmp for debugging saves
def find_surface_attributes(obj, parent_name=""):
    # Check if the object has the __dict__ attribute
    if not hasattr(obj, '__dict__'):
        return

    for attr_name, attr_value in obj.__dict__.items():
        full_attr_name = f"{parent_name}.{attr_name}" if parent_name else attr_name

        if isinstance(attr_value, pygame.Surface):
            print(f"Attribute containing pygame.Surface found: {full_attr_name}")
        else:
            find_surface_attributes(attr_value, full_attr_name)


class Game():
    def __init__(self, initial_money, initial_level, initial_lives, init_last_round_restarts,
                 lev, print_total_money, inset_window, test_setup=[]):
        self.player_money = initial_money
        self.total_money = initial_money
        self.level_num = initial_level
        self.print_total_money = print_total_money
        self.level = lev.levels[self.level_num]()
        self.towers = []
        self.enemies = []
        self.lives = initial_lives
        self.running = True
        self.enemy_spawn_timer = 0
        self.game_over = False
        self.active = False
        self.current_tower_type = None
        self.inset_window = inset_window
        self.inset_window['active'] = False
        self.money_per_hit = self.set_money_per_hit() # 1.0
        self.failed = False

        self.start_round_money = initial_money
        self.start_round_lives = initial_lives
        self.start_round_towers = []
        self.last_round_restarts = init_last_round_restarts
        self.path_id = 0  # if had gmap here - could make sure correct even when start on later level.

        self.total_hits = 0
        self.start_round_total_hits = 0
        self.start_round_total_money = initial_money
        self.lives_highlight = 0
        self.totems = []
        self.shown_hint = False
        self.lives_lost = 0
        self.lives_lost_round = 0
        self.map_complete = False
        self.aced = False
        self.displayed_game_over = False
        self.round_bonus = 20
        self.highlight_time = 20
        self.test_setup = test_setup
        self.test_tower_setup()
        self.removables = []

    def set_map(self, gmap):
        self.removables = gmap.get_removables()
        self.start_round_removables = copy.deepcopy(self.removables)

    def test_tower_setup(self):
        """ test_setup is a list of tuples of the form (tower_type, pos, lev)
        # So [(3, (100,100), 2)] would be a wizard at position (100,100) at level 2.
        # pos is the position of the center of the tower
        """
        for tower in self.test_setup:
            self.test_placement(*tower)

    def test_placement(self, tower_id, pos, lev):
        #testing a setup
        tower_type = tower_types[tower_id]
        newtower = tower_type(position=pos)
        for i in range(lev-1):
            newtower.level_up()

        self.towers.append(newtower)
        self.start_round_towers.append(copy.copy(newtower))

    #def __reduce__(self):
        ## Get the object's state (equivalent to the output of __getstate__)
        #state = self.__dict__.copy()

        ## Iterate over the state items
        #for key, value in state.items():
            #if isinstance(value, pygame.Surface):
                #print(f"Non-picklable pygame.Surface found in attribute: {key}")
                ## Handle or remove the pygame.Surface object
                ## e.g., state[key] = None or remove the key-value pair entirely
                #del state[key]

        ## Return a tuple that pickle uses for serialization:
        ## - Callable (usually the class itself)
        ## - Tuple of arguments for the callable (usually empty)
        ## - State to be pickled
        #return (self.__class__, (), state)

    # this might help - you can delete anything thats reset in restart_round
    # but for towers they will be stored in start_round_towers
    # but I think enemies may be the issue as only faling when fail map and enemies exist.
    def __getstate__(self):
        state = self.__dict__.copy()
        # does this fix the intermittent save error?
        del state['current_tower_type']
        del state['enemies']
        del state['towers']
        del state['totems']
        for key, value in state.items():
            if isinstance(value, pygame.Surface):
                print(f"Non-picklable pygame.Surface found in attribute: {key}")
                # Handle or remove the pygame.Surface object
                # e.g., state[key] = None or remove the key-value pair entirely
                del state[key]
        return state

    def __setstate__(self, state):
        self.__dict__ = state
        self.current_tower_type = None
        self.inset_window['active'] = False  # If set current_tower_type to None - need this
        self.enemies = []
        self.towers = []
        self.totems = []

    def reset_level(self, gmap):
        self.enemies = []
        self.running = True
        self.enemy_spawn_timer = 0
        self.active = False
        gmap.set_removables(self.removables)
        if gmap.alternate_paths:
            self.path_id = (self.level_num - 1) % len(gmap.paths)
        else:
            self.path_id = 0
        self.shown_hint = False

    def failed_map(self, gmap, account):
        # Update to only remove save if last round restarts are exhausted.
        self.failed = True
        if self.last_round_restarts <= 0:
            account.failed_map(gmap)
        find_surface_attributes(self)
        try:
            account.save()  # could do inside failed_map/save_map/complete_map
        except TypeError:
            print('Save failed')

    def restart_round(self, lev, gmap, decrement=True):
        self.player_money = self.start_round_money
        self.total_money = self.start_round_money
        self.lives = self.start_round_lives
        self.total_hits = self.start_round_total_hits
        self.total_money = self.start_round_total_money
        self.removables = copy.deepcopy(self.start_round_removables)
        gmap.set_removables(self.removables)
        self.towers = []
        self.totems = []
        for tower in self.start_round_towers:
            ctower = copy.copy(tower)
            self.towers.append(ctower)
            if isinstance(ctower, Totem):
                self.totems.append(ctower)

        if decrement or self.failed:
            self.last_round_restarts -= 1

        self.failed = False
        self.game_over = False
        self.level = lev.levels[self.level_num]()  # reset this level (phase num / num_spawned)
        self.lives_highlight = 0
        self.map_complete = False
        self.aced = False
        #lives_lost -= lives_lost_round  # no cos if died was not done - so this will be needed if restart when not dead
        #or calc lives lost even when die and then always do it.

    def process_hits(self, hits):
        self.total_hits += hits
        self.player_money += hits * self.money_per_hit
        self.total_money += hits * self.money_per_hit
        #print(f"process_hits {self.money_per_hit=}")

    def set_money_per_hit(self):
        if self.level_num < 10:
            self.money_per_hit = 1.0
        elif self.level_num < 20:
            self.money_per_hit = 0.7
        elif self.level_num < 30:
            self.money_per_hit = 0.5
        elif self.level_num < 40:
            self.money_per_hit = 0.4
        elif self.level_num < 50:
            self.money_per_hit = 0.3
        elif self.level_num < 60:
            self.money_per_hit = 0.2
        else:
            self.money_per_hit = 0.15

        #print(f"{self.money_per_hit=}")

        return self.money_per_hit

    def level_complete(self, display, window, window_size, lev, gmap, init_last_round_restarts, account):
        font = pygame.font.SysFont(None, 72)
        win_text = font.render("Win!", True, (0, 255, 0))  # Green color for the win text
        text_rect = win_text.get_rect(center=((window_size[0] - 100) / 2, window_size[1] / 2))
        window.blit(win_text, text_rect)
        display.flip()  # Update the full display Surface to the screen
        self.player_money += self.round_bonus
        self.total_money += self.round_bonus

        # for stats
        self.lives_lost_round = self.start_round_lives - self.lives
        self.lives_lost += self.lives_lost_round

        gmap.map_update(self.level_num)  # for rare maps that may update after certain levels

        if self.level_num % 10 == 0:
            self.lives += 10
            self.lives_highlight = self.highlight_time

        # Pause for a second to display the win message
        pygame.time.wait(1000)

        if self.level_num == lev.max_level:
            self.game_over = True
            self.current_tower_type = None
            self.map_complete = True
            self.current_tower_type = None
            # I'm thinking I may actually allow last round restarts for an ACE.
            # but if so prob want to have option to restart round even when dont die - for going for ace!
            if self.last_round_restarts == init_last_round_restarts and self.lives_lost == 0:
                self.aced = True
            else:
                self.aced = False

            account.complete_map(gmap, self.aced)
            account.save()
            sounds.play('victory')

            if self.print_total_money:
                rbe = self.total_hits + self.lives_lost
                round_money = self.total_money - self.start_round_total_money
                #print(f"At finish: level {self.level_num} {total_hits=} {total_money=:.2f} {lives_lost=} {rbe=} {round_money=}")
        else:
            round_money = self.total_money - self.start_round_total_money

            self.start_round_money = self.player_money
            self.start_round_lives = self.lives
            self.start_round_total_hits = self.total_hits
            self.start_round_total_money = self.total_money
            self.start_round_towers = []
            for tower in self.towers:
                self.start_round_towers.append(copy.copy(tower))
            self.start_round_removables = copy.deepcopy(self.removables) #gmap.get_removables()
            self.level_num += 1
            self.set_money_per_hit()
            self.level = lev.levels[self.level_num]()
            self.reset_level(gmap)
            # Will be in stats option in options window.
            if self.print_total_money:
                rbe = self.total_hits + self.lives_lost
                #print(f"Before level {self.level_num} {total_hits=} {total_money=:.2f} {lives_lost=} {rbe=}")
                print(f"At finish: level {self.level_num} {self.total_hits=} {self.total_money=:.2f} {self.lives_lost=} {rbe=} {round_money=}")
            # ok it saves if have no towers so def towres that are the problem - but what surface is in towres
            account.save_map(gmap.name, self)
            account.save()
