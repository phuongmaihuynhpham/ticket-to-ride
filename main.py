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
    def __init__(self) -> None:
        player_count = input("Welcome to Ticket to Ride Germany! How many players are playing today? ")
        while not self.player_count.isdigit() or int(self.player_count) not in range(1, 6):
            print("This is not a valid number. Please enter the number of players again. "
                  "Note that the game can accommodate a maximum of 5 players.")
            player_count = input("Welcome to Ticket to Ride Germany! How many players are playing today? ")

        self.player_count = int(player_count)
        self.players = [Player(PLAYER_COLORS[i]) for i in range(int(self.player_count))]
        self.current_player_index = 0

        self.cities = {city: City(city) for city in CITIES}
        self.routes = [Route(route[0], route[1], route[2]) for route in ROUTES]

        self.player_cards = random.shuffle([color for color in CardColors] * 12 + [CardColors.RAINBOW] * 2)
        self.short_destination_cards = deque(random.shuffle([DestinationCard(dest_card[0], dest_card[1], True)
                                                             for dest_card in SHORT_DESTINATION_CARDS]))
        self.long_destination_cards = deque(random.shuffle([DestinationCard(dest_card[0], dest_card[1], False)
                                                            for dest_card in LONG_DESTINATION_CARDS]))

        self.available_player_cards = self.player_cards[-5:]
        self.player_cards = self.player_cards[:-5]
        self.player_discard_pile = []

        self.turns_remaining = None

    def handle_pick_player_cards(self, player):
        first_card_response = self.pick_player_card()
        if not first_card_response["success"]:
            return False
        if not first_card_response["deck"] and first_card_response["color"] == CardColors.RAINBOW:
            return player.add_player_cards(CardColors.RAINBOW)

        print("Note that for your second card, you must not choose a RAINBOW card from the available player cards.")
        second_card_response = self.pick_player_card()

        while not second_card_response["success"] or (not second_card_response["deck"] and second_card_response["color"] == CardColors.RAINBOW):
            if second_card_response["success"]:
                print("You may not choose a RAINBOW card from the available player cards "
                      "as a second card. Please pick another card.")
                self.player_cards.append(self.available_player_cards[-1])
                self.available_player_cards[-1] = CardColors.RAINBOW

            second_card_response = self.pick_player_card()

        return player.add_player_cards(first_card_response["color"], second_card_response["color"])

    def pick_player_card(self):
        if self.available_player_cards.count(CardColors.RAINBOW) >= 3:
            self.player_discard_pile += self.available_player_cards
            self.available_player_cards = []
            self.draw_player_card_deck(5)

        # TODO: what if the new drawn cards also has 3 RAINBOW cards?

        print(f"The available player cards are: {', '.join([card.name for card in self.available_player_cards])}")
        color_string = input("Which card do you want to pick? Type a color or 'DECK' "
                             "if you want to pick a random card from the player cards deck. "
                             "If you wish to choose another action instead, enter Cancel. ")

        if color_string.upper() == "DECK":
            if len(self.player_cards) + len(self.player_discard_pile) == 0:
                print("There are no cards left in both the player cards deck and the discard pile. "
                      "Please pick one of the available player cards instead.")
                return {"success": False}

            color = self.draw_player_card_deck(1)[0]
            return {"deck": True, "color": color, "success": True}

        elif color_string.upper() in CardColors and CardColors[color_string.upper()] in self.available_player_cards:
            color = CardColors[color_string.upper()]
            self.available_player_cards.remove(color)
            self.draw_player_card_deck(1)
            return {"deck": False, "color": color, "success": True}

        else:
            print("The color you chose is not valid or not available. Please try again.")
            return {"success": False}

    def draw_player_card_deck(self, num_cards):
        drawn_cards = []

        for _ in range(num_cards):
            if len(self.player_cards) == 0:
                if len(self.player_discard_pile) == 0:
                    return

                self.player_cards = random.shuffle(self.player_discard_pile)
                self.player_discard_pile = []

            card = self.player_cards[-1]
            drawn_cards.append(card)
            del self.player_cards[-1]

            if len(self.available_player_cards) < 5:
                self.available_player_cards.append(card)

        return drawn_cards

    def handle_claim_route(self, player):
        case_insensitive_cities = {city.upper(): city for city in CITIES}
        print("Which route do you like to claim? Please input the two end-cities of that route.")

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
        if len(self.short_destination_cards) + len(self.long_destination_cards) <= 4:
            print("Since there are 4 or fewer Destination Cards left, these are all available Destination Cards.")
            available_cards = self.draw_destination_card_deck(len(self.short_destination_cards),
                                                              len(self.long_destination_cards))

        else:
            short_cards = input("You will be drawing a total of 4 Destination Cards.\n"
                                f"There are {len(self.long_destination_cards)} long Destination Cards "
                                f"and {len(self.short_destination_cards)} short Destination Cards left."
                                "How many SHORT Destination Cards would you like to pick? ")

            while not short_cards.isdigit() or int(short_cards) not in range(5):
                short_cards = input("This is not a valid number. Please re-enter a valid number "
                                    "of short Destination Cards you would like to pick. ")

            short_cards_num = int(short_cards)
            long_cards_num = 4 - int(short_cards)

            if short_cards_num >= len(self.short_destination_cards):
                print("There are not enough short Destination Cards left in the deck. Please try again.")
                return False
            elif long_cards_num >= len(self.long_destination_cards):
                print("There are not enough long Destination Cards left in the deck. Please try again.")
                return False

            available_cards = self.draw_destination_card_deck(short_cards_num, long_cards_num)

        print("Your available cards are: ")
        for i, card in enumerate(available_cards):
            print(f"{i+1}. {card}")

        while True:
            selection = input("Which cards do you want to pick? Please enter a space-separated string "
                              "consisting of the indices of the cards you wish to pick (for example, '1 3 4'): ")

            if selection.strip() == "":
                print("You need to select at least one card. Please try again.")
                continue

            try:
                selected_indices = [int(card) for card in selection.strip().split()]

                for i in range(len(available_cards)):
                    if i+1 in selected_indices:
                        available_cards[i].set_owner(player)
                        player.add_destination_cards(available_cards[i])
                    elif available_cards[i].short_types:
                        self.short_destination_cards.append(available_cards[i])
                    else:
                        self.long_destination_cards.append(available_cards[i])

                return True

            except Exception:
                print("The indices that you entered are not valid. Please try again.")

    def draw_destination_card_deck(self, short_cards_num, long_cards_num):
        drawn_cards = []

        for _ in range(short_cards_num):
            drawn_cards.append(self.short_destination_cards.popleft())
        for _ in range(long_cards_num):
            drawn_cards.append(self.long_destination_cards.popleft())

        return drawn_cards

    def check_endgame(self):
        for player in self.players:
            if player.trains <= 2:
                self.turns_remaining = self.player_count

    def endgame(self):
        # TODO: implement endgame calculations
        pass

    def run(self):
        while self.turns_remaining > 0:
            current_player = self.players[self.current_player_index]

            # TODO: print the current state of the board

            current_player.print_state()

            while True:
                # TODO: present the three valid actions (and pass) and prompt user to choose one
                action = input("...")

                if action == "1":
                    self.handle_pick_player_cards(current_player)
                    break
                elif action == "2":
                    self.handle_claim_route(current_player)
                    break
                elif action == "3":
                    self.handle_pick_destination_cards(current_player)
                    break
                elif action == "4":
                    break

            if not self.turns_remaining:
                self.check_endgame()
            else:
                self.turns_remaining -= 1

            if self.current_player_index != self.player_count - 1:
                self.current_player_index += 1
            else:
                self.current_player_index = 0

        self.endgame()


if __name__ == "__main__":
    game = GameManager()
    game.run()
