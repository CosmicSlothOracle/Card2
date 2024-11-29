from ..types import Phase

class PhaseManager:
    def __init__(self, game):
        self.game = game
        self.phase_handlers = {
            Phase.INVOCATION: self.handle_invocation,
            Phase.PREPARATION: self.handle_preparation,
            Phase.SUMMONING: self.handle_summoning,
            Phase.MISSION: self.handle_mission,
            Phase.REFLECTION: self.handle_reflection
        }
        
    def handle_invocation(self):
        """Handle draw phase"""
        current_player = self.game.players[self.game.active_player_index]
        if self.game.turn_count > 1 or self.game.active_player_index == 1:
            current_player.draw_card()
            
    def handle_preparation(self):
        """Handle card playing phase"""
        current_player = self.game.players[self.game.active_player_index]
        # Allow playing Scriptures and Relics
        return True
        
    def handle_summoning(self):
        """Handle believer summoning phase"""
        current_player = self.game.players[self.game.active_player_index]
        # Allow summoning Believers
        return True
        
    def handle_mission(self):
        """Handle mission assignment phase"""
        current_player = self.game.players[self.game.active_player_index]
        # Allow assigning missions and attacking
        return True
        
    def handle_reflection(self):
        """Handle end phase"""
        # Reset phase-specific states and prepare for next turn
        return True 