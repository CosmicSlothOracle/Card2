import pytest
from game.card import Card
from game.types.enums import CardType, Faction, Position
from game.card_types import Attribute, ScriptureType, MiracleType

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

def test_believer_combat():
    attacker_data = {
        "name": "Archangel Michael",
        "card_type": "BELIEVER",
        "attribute": "HOLY",
        "faith_points": 2500,
        "divinity_points": 2000,
        "skp_cost": 6,
        "faction": "GOD"
    }
    
    defender_data = {
        "name": "Faithful Guardian",
        "card_type": "BELIEVER",
        "attribute": "HOLY",
        "faith_points": 1400,
        "divinity_points": 1300,
        "skp_cost": 2,
        "faction": "CHURCH"
    }
    
    attacker = Card(**attacker_data)
    defender = Card(**defender_data)
    
    # Test combat resolution
    assert attacker.faith_points > defender.divinity_points
    assert attacker.can_attack(defender)

def test_relic_equipping():
    believer_data = {
        "name": "Holy Guardian",
        "card_type": "BELIEVER",
        "attribute": "HOLY",
        "faith_points": 1600,
        "divinity_points": 1800,
        "skp_cost": 4,
        "faction": "GOD"
    }
    
    relic_data = {
        "name": "Crown of Thorns",
        "card_type": "RELIC",
        "attribute": "HOLY",
        "effect": "Equipped Believer gains immunity to Miracles",
        "skp_cost": 3,
        "faction": "CHURCH"
    }
    
    believer = Card(**believer_data)
    relic = Card(**relic_data)
    
    believer.position = Position.SANCTUARY
    assert relic.can_equip(believer)
