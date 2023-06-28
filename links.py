class Link:
    def __init__(self, connecting_cities, length, color) -> None:
        self.connecting_cities = connecting_cities
        self.length = length
        self.color = color
        self.owner = None

    def set_owner(self, player):
        self.owner = player

    def place_trains(self, player):
        pass