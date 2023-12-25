import maps

class Account():
    def __init__(self, name='Guest'):
        self.name = name
        self.maps_complete = []
        self.maps_aced = []

    # map is keyword, use gmap (game map)
    def complete_map(self, gmap, aced=False):
        if not gmap in self.maps_complete:
            self.maps_complete.append(gmap)

        if aced:
            if not gmap in self.maps_aced:
                self.maps_aced.append(gmap)
