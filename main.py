from card_colors import CardColors
from cities import City
from destination_cards import DestinationCard
from links import Link
from players import Player

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
        self.destination_cards = [DestinationCard(dest_card[0], dest_card[1]) for dest_card in DESTINATION_CARDS]
