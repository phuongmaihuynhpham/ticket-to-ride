from card_colors import CardColors

LINK_POINTS = {
    1: 1,
    2: 2,
    3: 4,
    4: 7,
    5: 10,
    6: 15,
    7: 18
}


class Link:
    def __init__(self, connecting_cities, color, length) -> None:
        self.connecting_cities = connecting_cities
        self.connecting_cities[0].connected_links[self.connecting_cities[0].name] = self
        self.connecting_cities[1].connected_links[self.connecting_cities[1].name] = self

        self.color = color
        self.length = length
        self.points = LINK_POINTS[self.length]
        self.owner = None

    def set_owner(self, player):
        self.owner = player

    def place_trains(self, player):
        if self.owner:
            print("This Link is already occupied. Please try again.")
            return False

        if self.color is None:
            color_string = input("Which card color do you want to use? Note that you must \
                                 have enough cards of that color to build the train.")

            if color_string.upper() in CardColors:
                link_color = CardColors[color_string.upper()]
            else:
                print("This is not a valid color. Please try again.")
                return False

        else:
            link_color = self.color

        rainbow_num = player.player_cards[CardColors.RAINBOW]
        train_color_num = player.player_cards[link_color]

        if player.train >= self.length:
            if train_color_num >= self.length:
                self.set_owner(player)
                player.use_trains(self.length)
                player.use_player_cards(link_color, self.length)
                player.earn_points(self.points)
                return True

            elif train_color_num + rainbow_num >= self.length:
                self.set_owner(player)
                player.use_trains(self.length)
                player.use_player_cards(CardColors.RAINBOW, self.length - train_color_num)
                player.use_player_cards(link_color, train_color_num)
                player.earn_points(self.points)
                return True

        print("You do not have enough cards or trains remaining to place trains on this Link. Please try again.")
        return False
