import pygame
import json
from pathlib import Path
from .core.player import Player
from .core.card import Card
from .types.enums import Phase, CardType

class TestamentDuelGame:
    def __init__(self, screen, clock, debug=False):
        self.screen = screen
        self.clock = clock
        self.debug = debug
        
        # Load decks from JSON
        player1_deck = self._load_deck("assets/decks/player1_deck.json")
        player2_deck = self._load_deck("assets/decks/player2_deck.json")
        
        # Initialize players with proper decks
        self.players = [
            Player("Player 1", player1_deck),
            Player("Player 2", player2_deck)
        ]
        
        # Game state
        self.current_phase = Phase.INVOCATION
        self.active_player_index = 0
        self.turn_count = 1
        self.game_over = False
        
        # Draw starting hands
        for player in self.players:
            for _ in range(5):
                player.draw_card()
        self.active_player_index = 0

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            self._handle_key_press(event)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event)
            
        return True
        
    def _handle_key_press(self, event):
        if self.game_over:
            return
            
        if event.key == pygame.K_SPACE:  # Draw card
            if self.current_phase == Phase.INVOCATION:
                self.players[self.active_player_index].draw_card()
                self._advance_phase()
                
        elif event.key == pygame.K_TAB:  # End phase
            self._advance_phase()
            
        elif event.key == pygame.K_RETURN:  # End turn
            self._end_turn()
    
    def _handle_mouse_click(self, event):
        if self.game_over:
            return
            
        pos = pygame.mouse.get_pos()
        # TODO: Add card selection and playing logic
    
    def _advance_phase(self):
        phases = list(Phase)
        current_index = phases.index(self.current_phase)
        self.current_phase = phases[(current_index + 1) % len(phases)]
        
        if self.current_phase == Phase.INVOCATION:
            self._end_turn()
    
    def _end_turn(self):
        self.active_player_index = (self.active_player_index + 1) % 2
        self.turn_count += 1
        
    def update(self):
        if not self.game_over:
            self._check_win_condition()
            
    def _check_win_condition(self):
        for i, player in enumerate(self.players):
            if player.grace_points <= 0:
                self.game_over = True
                print(f"Game Over! {self.players[1-i].name} wins!")
                break
                
            if len(player.deck) == 0 and len(player.hand) == 0:
                self.game_over = True
                print(f"Game Over! {self.players[1-i].name} wins by deck out!")
                break
    
    def draw(self):
        self.screen.fill((50, 50, 50))  # Dark gray background
        
        # Draw game state info
        font = pygame.font.Font(None, 36)
        phase_text = font.render(f"Phase: {self.current_phase.name}", True, (255, 255, 255))
        player_text = font.render(f"Player {self.active_player_index + 1}'s Turn", True, (255, 255, 255))
        
        self.screen.blit(phase_text, (10, 10))
        self.screen.blit(player_text, (10, 50))
        
        if self.game_over:
            game_over_text = font.render("Game Over!", True, (255, 0, 0))
            self.screen.blit(game_over_text, (self.screen.get_width()//2 - 100, self.screen.get_height()//2))
            
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                running = self.handle_event(event)
                if not running:
                    break
            
            # Update game state
            self.update()
            
            # Draw everything
            self.screen.fill((50, 50, 50))  # Dark gray background
            self._draw()
            pygame.display.flip()
            
            # Cap the framerate
            self.clock.tick(60)
        
        pygame.quit()

    def _draw(self):
        # Draw player hands
        for i, player in enumerate(self.players):
            y_offset = 550 if i == 0 else 50  # Bottom for player 1, top for player 2
            for j, card in enumerate(player.hand):
                card.rect.x = 100 + j * (CARD_WIDTH + 20)
                card.rect.y = y_offset
                card.draw(self.screen)
        
        # Draw phase and turn information
        font = pygame.font.Font(None, 36)
        phase_text = font.render(f"Phase: {self.current_phase.name}", True, (255, 255, 255))
        turn_text = font.render(f"Turn {self.turn_count}: Player {self.active_player_index + 1}", True, (255, 255, 255))
        self.screen.blit(phase_text, (10, 10))
        self.screen.blit(turn_text, (10, 50))

    def get_card_at_position(self, pos):
        """Returns card at given position or None"""
        for player in self.players:
            for card in player.hand:
                if card.rect.collidepoint(pos):
                    return card
        return None
