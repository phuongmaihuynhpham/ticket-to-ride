class DestinationCard:
    def __init__(self, end_cities, points) -> None:
        self.end_cities = end_cities
        self.points = points
        self.owner = None

    def set_owner(self, player):
        self.owner = player

    def verify(self):
        return self.end_cities[0].search(self.end_cities[1], self.owner)

    def __str__(self):
        pass
