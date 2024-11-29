import json
from typing import Dict, List
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class GameState:
    turn_number: int
    active_player: int
    current_phase: str
    players: List[Dict]
    board_state: Dict
    
class GameStateManager:
    def __init__(self):
        self.state_history: List[GameState] = []
        self.current_index = -1
        
    def save_state(self, game_state: GameState):
        """Save current game state"""
        # Remove any states after current index (for undo/redo)
        if self.current_index < len(self.state_history) - 1:
            self.state_history = self.state_history[:self.current_index + 1]
            
        self.state_history.append(game_state)
        self.current_index += 1
        
    def undo(self) -> GameState:
        """Undo last action"""
        if self.current_index > 0:
            self.current_index -= 1
            return self.state_history[self.current_index]
        return None
        
    def redo(self) -> GameState:
        """Redo last undone action"""
        if self.current_index < len(self.state_history) - 1:
            self.current_index += 1
            return self.state_history[self.current_index]
        return None
        
    def save_to_file(self, filename: str):
        """Save game state to file"""
        state_data = {
            "timestamp": datetime.now().isoformat(),
            "states": [asdict(state) for state in self.state_history]
        }
        
        with open(filename, 'w') as f:
            json.dump(state_data, f, indent=2)
            
    def load_from_file(self, filename: str):
        """Load game state from file"""
        with open(filename, 'r') as f:
            state_data = json.load(f)
            self.state_history = [
                GameState(**state) for state in state_data["states"]
            ]
            self.current_index = len(self.state_history) - 1 