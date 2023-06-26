from card_colors import CardColors

class Player:
    def __init__(self, color) -> None:
        self.color = color
        self.trains = 45
        
        card_colors = ["purple", "blue", "orange", "white", "green", "yellow", "black", "red", "rainbow"]
        self.player_cards = {color: 0 for color in card_colors}
        
        self.destination_cards = []

    def verify(self):
        pass