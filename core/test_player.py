import pytest
from game.core.player import Player
from game.core.card import Card

@pytest.fixture
def player():
    test_deck = [Card("Test Card", "BELIEVER", None, 100, "path/to/image") for _ in range(5)]
    return Player("Test Player", test_deck)

def test_draw_card(player):
    result = player.draw_card()
    assert result == True
    assert len(player.hand) == 1

def test_full_hand(player):
    player.hand = [Card("Hand Card", "BELIEVER", None, 100, "path/to/image") for _ in range(player.MAX_HAND_SIZE)]
    result = player.draw_card()
    assert result == False

def test_empty_deck(player):
    player.deck = []
    result = player.draw_card()
    assert result == False
