from enum import Enum


class Competitions(Enum):
    FOOTBALL = (1, "Football")

    def __init__(self, ID, NAME):
        self.ID = ID
        self.NAME = NAME
