from card_colors import CardColors
from cities import City
from destination_cards import DestinationCard
from links import Link
from players import Player
import random

PLAYER_COLORS = ["red", "white", "yellow", "purple", "black"]
CITIES = ["Denmark", "Bremerhaven", "Bremen", "Hamburg", "Kiel", "Schwerin"]
LINKS = [
    (["Denmark", "Bremerhaven"], CardColors.GREEN, 5),
    (["Bremerhaven", "Bremen"], CardColors.WHITE, 1),
    (["Bremen", "Hamburg"], CardColors.ORANGE, 3),
    (["Bremerhaven", "Hamburg"], None, 3),
    (["Bremerhaven", "Kiel"], None, 3),
    (["Denmark", "Kiel"], None, 2),
    (["Kiel", "Schwerin"], CardColors.YELLOW, 3),
    (["Hamburg", "Schwerin"], CardColors.GREEN, 2),
    (["Hamburg", "Kiel"], CardColors.PURPLE, 2)
    # TODO: there's another Hamburg-Kiel link that is black, but we'll implement that later
]

DESTINATION_CARDS = [
    (["Denmark", "Bremen"], 6),
    (["Bremen", "Kiel"], 4),
    (["Bremerhaven", "Schwerin"], 5),
    (["Denmark", "Schwerin"], 5)
]


class GameManager:
    def __init__(self, player_count) -> None:
        self.players = [Player(PLAYER_COLORS[i]) for i in range(player_count)]
        self.cities = {city: City(city) for city in CITIES}
        self.links = [Link(link[0], link[1], link[2]) for link in LINKS]

        self.player_cards = random.shuffle([color for color in CardColors] * 12 + [CardColors.RAINBOW] * 2)
        self.destination_cards = random.shuffle([DestinationCard(dest_card[0], dest_card[1])
                                                 for dest_card in DESTINATION_CARDS])

        self.available_player_cards = self.player_cards[-5:]
        self.player_cards = self.player_cards[:-5]
        self.discard_pile = []

    def handle_pick_player_cards(self, player):
        first_card_response = self.pick_player_card()
        if not first_card_response["success"]:
            return False
        if not first_card_response["deck"] and first_card_response["color"] == CardColors.RAINBOW:
            return player.add_player_cards(CardColors.RAINBOW)

        second_card_response = self.pick_player_card()
        if not second_card_response["success"]:
            return False

        return player.add_player_cards(first_card_response["color"], second_card_response["color"])

    def pick_player_card(self):
        print(f"The available player cards are: {', '.join([card.name for card in self.available_player_cards])}")
        color_string = input("Which card do you want to pick? Type a color or 'DECK' "
                             "if you want to pick a random card from the player cards deck.")

        if color_string.upper() == "DECK":
            return {"deck": True, "color": self.player_cards[-1], "success": True}

        elif color_string.upper() in CardColors and CardColors[color_string.upper()] in self.available_player_cards:
            color = CardColors[color_string.upper()]
            self.draw_card_player_deck(color)
            return {"deck": False, "color": color, "success": True}

        else:
            print("The color you chose is not valid or not available. Please try again.")
            return {"success": False}

    def draw_card_player_deck(self, color):
        self.available_player_cards.remove(color)
        self.available_player_cards.append(self.player_cards[-1])
        del self.player_cards[-1]
