from enum import Enum

class CardType(Enum):
    CREATURE = "Creature"
    SPELL = "Spell"
    SCRIPTURE = "Scripture"
    MIRACLE = "Miracle"

class Faction(Enum):
    NEUTRAL = "Neutral"
    LIGHT = "Light"
    DARK = "Dark"

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y 