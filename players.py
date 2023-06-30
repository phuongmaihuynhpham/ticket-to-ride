from card_colors import CardColors


class Player:
    def __init__(self, color) -> None:
        self.color = color
        self.trains = 45
        self.points = 0

        self.player_cards = {color: 0 for color in CardColors}

        self.destination_cards = []

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.color == other.color
        return False

    def add_player_card(self, color1, color2=None):
        self.player_cards[color1] += 1
        if not color2:
            self.player_cards[color2] += 1
        return True

    def use_player_cards(self, color, num_cards):
        self.player_cards[color] -= num_cards

    def add_destination_cards(self, dest_card):
        self.destination_cards.append(dest_card)
        return True

    def use_trains(self, num_trains):
        self.trains -= num_trains

    def earn_points(self, num_points):
        self.points += num_points
