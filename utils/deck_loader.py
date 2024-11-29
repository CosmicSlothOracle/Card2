import json
from pathlib import Path
from ..types.enums import CardType
from ..core.card import Card

def load_deck(filepath: str) -> list:
    """Load deck from JSON file"""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Deck file not found: {filepath}")
        
    with open(path) as f:
        deck_data = json.load(f)
        
    deck = []
    for card_data in deck_data:
        card = Card(
            name=card_data["name"],
            card_type=CardType[card_data["card_type"]],
            effect=card_data["effect"],
            faith_points=card_data.get("faith_points"),
            divinity_points=card_data.get("divinity_points"),
            skp_cost=card_data["skp_cost"]
        )
        deck.append(card)
    return deck 