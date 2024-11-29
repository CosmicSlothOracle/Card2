from enum import Enum, auto

class Phase(Enum):
    INVOCATION = auto()
    PREPARATION = auto()
    BATTLE = auto()
    END = auto()

class CardType(Enum):
    CREATURE = "Creature"
    BELIEVER = "BELIEVER"
    SCRIPTURE = "SCRIPTURE"
    MIRACLE = "MIRACLE"
    RELIC = "RELIC"

class Faction(Enum):
    GOD = "GOD"
    CHURCH = "CHURCH"
    HUMANITY = "HUMANITY"

class Position(Enum):
    HAND = auto()
    FIELD = auto()
    GRAVEYARD = auto() 