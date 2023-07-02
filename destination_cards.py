class DestinationCard:
    def __init__(self, end_cities, points, short_type) -> None:
        self.end_cities = end_cities
        self.points = points
        self.short_type = short_type
        self.owner = None

    def set_owner(self, player):
        self.owner = player

    def verify(self):
        return self.end_cities[0].search(self.end_cities[1], self.owner)

    def __str__(self):
        pass
