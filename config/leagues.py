from enum import Enum


class Leagues(Enum):
    GERMAN_BUNDESLIGA = (59, "German Bundesliga")
    ENGLISH_PREMIER_LEAGUE = (10932509, "English Premier League")
    SPANISH_LA_LIGA = (117, "Spanish La Liga")
    ITALIAN_SERIE_A = (81, "Italian Serie A")
    FRENCH_LIGUE_1 = (55, "French Ligue 1")
    UEFA_CHAMPIONS_LEAGUE = (228, "UEFA - Champions League")
    UEFA_EURO_QUALIFIERS = (12552926, "UEFA Euro Qualifiers")

    def __init__(self, ID, NAME):
        self.ID = ID
        self.NAME = NAME
