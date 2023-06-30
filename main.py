from card_colors import CardColors
from cities import City
from destination_cards import DestinationCard
from routes import Route
from players import Player
from collections import deque
import random

PLAYER_COLORS = ["red", "white", "yellow", "purple", "black"]
CITIES = ["Denmark", "Bremerhaven", "Bremen", "Hamburg", "Kiel", "Schwerin"]

ROUTES = [
    (["Denmark", "Bremerhaven"], CardColors.GREEN, 5),
    (["Bremerhaven", "Bremen"], CardColors.WHITE, 1),
    (["Bremen", "Hamburg"], CardColors.ORANGE, 3),
    (["Bremerhaven", "Hamburg"], None, 3),
    (["Bremerhaven", "Kiel"], None, 3),
    (["Denmark", "Kiel"], None, 2),
    (["Kiel", "Schwerin"], CardColors.YELLOW, 3),
    (["Hamburg", "Schwerin"], CardColors.GREEN, 2),
    (["Hamburg", "Kiel"], CardColors.PURPLE, 2)
    # TODO: there's another Hamburg-Kiel route that is black, but we'll implement that later
]

SHORT_DESTINATION_CARDS = [
    (["Bremen", "Kiel"], 4),
    (["Bremerhaven", "Schwerin"], 5),
    (["Denmark", "Schwerin"], 5)
]

LONG_DESTINATION_CARDS = [
    (["Denmark", "Bremen"], 6),
]


class GameManager:
    def __init__(self, player_count) -> None:
        self.players = [Player(PLAYER_COLORS[i]) for i in range(player_count)]
        self.cities = {city: City(city) for city in CITIES}
        self.routes = [Route(route[0], route[1], route[2]) for route in ROUTES]

        self.player_cards = random.shuffle([color for color in CardColors] * 12 + [CardColors.RAINBOW] * 2)
        self.short_destination_cards = deque(random.shuffle([DestinationCard(dest_card[0], dest_card[1])
                                                             for dest_card in SHORT_DESTINATION_CARDS]))
        self.long_destination_cards = deque(random.shuffle([DestinationCard(dest_card[0], dest_card[1])
                                                            for dest_card in LONG_DESTINATION_CARDS]))

        self.available_player_cards = self.player_cards[-5:]
        self.player_cards = self.player_cards[:-5]
        self.player_discard_pile = []

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
                             "if you want to pick a random card from the player cards deck. ")

        if color_string.upper() == "DECK":
            return {"deck": True, "color": self.player_cards[-1], "success": True}

        elif color_string.upper() in CardColors and CardColors[color_string.upper()] in self.available_player_cards:
            color = CardColors[color_string.upper()]
            self.draw_player_card_deck(color)
            return {"deck": False, "color": color, "success": True}

        else:
            print("The color you chose is not valid or not available. Please try again.")
            return {"success": False}

    def draw_player_card_deck(self, color):
        self.available_player_cards.remove(color)
        self.available_player_cards.append(self.player_cards[-1])
        del self.player_cards[-1]

    def handle_claim_route(self, player):
        case_insensitive_cities = {city.upper(): city for city in CITIES}
        print("Which route would you like to claim? Please input the two end-cities of that route.")

        first_city_string = input("Please input the first city: ")
        if first_city_string.upper() not in case_insensitive_cities:
            print("This is not a valid city. Please try again.")
            return False

        second_city_string = input("Please input the second city: ")
        if second_city_string.upper() not in case_insensitive_cities:
            print("This is not a valid city. Please try again.")

        first_city = self.cities[case_insensitive_cities[first_city_string.upper()]]
        route = first_city.connected_routes[case_insensitive_cities[second_city_string.upper()]]

        return route.claim_route(player)
        # TODO: add discarded cards to discard pile

    def handle_pick_destination_cards(self, player):
        dest_cards = []

        short_cards = input("You will be drawing a total of 4 Destination Cards.\n"
                       "How many SHORT Destination Cards would you like to pick? ")
        
        long_cards = 4 - short_cards
        
        if 

    def draw_destination_card_deck(self):
    