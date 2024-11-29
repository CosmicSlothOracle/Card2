from typing import Optional, List
from .card import Card
from .types import Position, Timing

class CombatManager:
    def __init__(self):
        self.pending_attacks = []
        self.damage_modifiers = []
        
    def declare_attack(self, attacker: Card, defender: Optional[Card], position: Position):
        if attacker.card_type != "BELIEVER":
            return False
            
        attack_data = {
            "attacker": attacker,
            "defender": defender,
            "position": position,
            "modifiers": []
        }
        if defender is None:
            attack_data["direct_attack"] = True
        self.pending_attacks.append(attack_data)
        return True

    def resolve_attacks(self):
        for attack in self.pending_attacks:
            total_damage = self._calculate_damage(attack)
            if attack.get("defender"):
                attack["defender"].take_damage(total_damage)
            else:
                # Direct attack to player
                attack["attacker"].player.opponent.take_damage(total_damage)
        self.pending_attacks.clear()

    def _calculate_damage(self, attack_data):
        base_damage = attack_data["attacker"].faith_points
        for modifier in attack_data["modifiers"] + self.damage_modifiers:
            if hasattr(modifier, 'apply'):
                base_damage = modifier.apply(base_damage)
            else:
                print("Error: Modifier missing apply method")
        return max(0, base_damage) 