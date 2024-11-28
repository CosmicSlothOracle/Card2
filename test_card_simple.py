import pygame
import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from enum import Enum

# Mock the required types
class CardType(Enum):
    CREATURE = "Creature"

class Timing(Enum):
    ON_ATTACK = "on_attack"
    ON_DEFEND = "on_defend"

class Effect:
    def __init__(self, name, timing, condition, action):
        self.name = name
        self.timing = timing
        self.condition = condition
        self.action = action

# Constants
CARD_WIDTH = 100
CARD_HEIGHT = 150
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
DARK_BLUE = (0, 0, 139)

# Import the Card class with local constants
from game.core.card import Card

# Initialize pygame for testing
pygame.init()

def test_basic_card_creation():
    """Test creating a basic card"""
    card = Card(
        name="Test Card",
        card_type=CardType.CREATURE,
        effect=None,
        faction="NEUTRAL"
    )
    
    assert card.name == "Test Card"
    assert card.card_type == CardType.CREATURE
    assert card.faction == "NEUTRAL"
    assert not card.is_destroyed
    assert not card.is_face_down
    assert not card.is_selected

if __name__ == "__main__":
    pytest.main([__file__]) 