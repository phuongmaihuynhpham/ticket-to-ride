class City:
    def __init__(self, name) -> None:
        self.name = name
        self.connected_routes = {}

    def set_connected_routes(self, routes):
        self.connected_routes = routes

    def search(self, target_city, player):
        # graph search algorithm
        pass
