from card_colors import *

class Link:
    def __init__(self, connecting_cities, length, color) -> None:
        self.connecting_cities = connecting_cities
        self.length = length
        self.color = color
        self.owner = None

    def set_owner(self, player):
        self.owner = player

    def place_trains(self, player):
        if self.owner:
            return False
        
        if self.color is None: # TODO: how to convert String to CardColors?
            color_string = input("Which train's color do you want to use? Note that you must have enough cards of that color to build the train.")
            link_color = color_string
        else:
            link_color = self.color
        
        rainbow_num = player.player_cards[CardColors.RAINBOW]
        train_color_num = player.player_cards[link_color]

        if player.train >= self.length:
            if train_color_num >= self.length:
                self.set_owner(player)
                player.train -= self.length
                player.player_cards[link_color] -= self.length
                return True
            else:
                if train_color_num + rainbow_num >= self.length:
                    self.set_owner(player)
                    player.train -= self.length
                    player.player_cards[CardColors.RAINBOW] -= (self.length - train_color_num)
                    player.player_cards[link_color] = 0
                    return True
        return False
