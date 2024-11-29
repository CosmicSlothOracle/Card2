from enum import Enum, auto

class CardType(Enum):
    BELIEVER = auto()
    SCRIPTURE = auto()
    MIRACLE = auto()
    RELIC = auto()

class Attribute(Enum):
    HOLY = auto()
    RIGHTEOUS = auto()
    DIVINE = auto()
    BLESSED = auto()

class ScriptureType(Enum):
    BLESSING = auto()
    RITUAL = auto()
    TEACHING = auto()

class MiracleType(Enum):
    REBUKE = auto()
    JUDGMENT = auto()
    TRIAL = auto()