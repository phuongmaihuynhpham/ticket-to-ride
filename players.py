from card_colors import CardColors


class Player:
    def __init__(self, color) -> None:
        self.color = color
        self.trains = 45
        self.points = 0

        self.player_cards = {color: 0 for color in CardColors}

        self.destination_cards = []

    def add_player_card(self, color1, color2):
        self.player_cards[color1] += 1
        self.player_cards[color2] += 1

    def add_destination_cards(self, dest_card):
        self.destination_cards.append(dest_card)

    def place_trains(self, city1, city2):
        pass
