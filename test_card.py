import pytest
from game.card import Card

def test_card_creation():
    card_data = {
        "name": "Faithful Shepherd",
        "card_type": "BELIEVER",
        "attribute": "HOLY",
        "effect": "Gains 300 FP for each Scripture in play",
        "level": 3,
        "faith_points": 1200,
        "divinity_points": 1000,
        "skp_cost": 3,
        "faction": "GOD"
    }
    
    card = Card(**card_data)
    assert card.name == "Faithful Shepherd"
    assert card.faith_points == 1200
    assert card.skp_cost == 3
