class City:
    def __init__(self, name) -> None:
        self.name = name
        self.connected_links = {} # a dictionary with key is the connected city and values are the length and color of train rail

    def search(self, target_city, player):
        # graph search algorithm
        pass