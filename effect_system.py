from typing import List, Callable
from dataclasses import dataclass
from enum import Enum, auto

class Timing(Enum):
    IMMEDIATE = auto()
    START_OF_TURN = auto()
    END_OF_TURN = auto()
    ON_ATTACK = auto()
    ON_DEFEND = auto()
    
@dataclass
class Effect:
    name: str
    timing: Timing
    condition: Callable
    action: Callable
    priority: int = 0
    
class EffectChain:
    def __init__(self):
        self.effects: List[Effect] = []
        
    def add_effect(self, effect: Effect):
        self.effects.append(effect)
        # Sort by priority
        self.effects.sort(key=lambda x: x.priority, reverse=True)
        
    def resolve(self, game_state):
        """Resolve all effects in chain"""
        for effect in self.effects:
            if effect.condition(game_state):
                effect.action(game_state)

class EffectManager:
    def __init__(self):
        self.active_effects = []
        self.pending_chain = EffectChain()
        
    def register_effect(self, effect: Effect):
        """Register a new effect to be resolved"""
        self.pending_chain.add_effect(effect)
        
    def resolve_effects(self, timing: Timing, game_state):
        """Resolve effects for a specific timing"""
        relevant_effects = [
            effect for effect in self.active_effects 
            if effect.timing == timing
        ]
        
        chain = EffectChain()
        for effect in relevant_effects:
            chain.add_effect(effect)
        
        chain.resolve(game_state) 