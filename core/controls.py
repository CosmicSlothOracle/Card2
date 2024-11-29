import pygame
from typing import Optional, Tuple, Dict, List
from ..types.enums import GameState, CardAction

class ControlsManager:
    def __init__(self, game):
        self.game = game
        # Mouse state tracking
        self.dragging_card = None
        self.drag_start_pos = None
        self.selected_card = None
        self.hover_card = None
        self.right_click_menu = None
        self.zoomed_card = None
        
        # Drag settings
        self.is_dragging = False
        self.drag_threshold = 5
        self.drag_offset = (0, 0)

    def handle_mouse_event(self, event: pygame.event.Event) -> Dict:
        """Central handler for all mouse events, returns action dict"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                return self._handle_left_click_down(event.pos)
            elif event.button == 3:  # Right click
                return self._handle_right_click(event.pos)
            elif event.button == 4:  # Mouse wheel up
                return self._handle_scroll(1)
            elif event.button == 5:  # Mouse wheel down
                return self._handle_scroll(-1)
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                return self._handle_left_click_up(event.pos)
            elif event.button == 3:
                return self._handle_right_click_up(event.pos)
                
        elif event.type == pygame.MOUSEMOTION:
            return self._handle_mouse_motion(event.pos)
            
        return {}

    def _handle_left_click_down(self, pos: Tuple[int, int]) -> Dict:
        # Clear any existing menus/zooms
        self.right_click_menu = None
        self.zoomed_card = None
        
        # Check UI elements first
        ui_action = self.game.ui_manager.handle_click(pos)
        if ui_action:
            return {"action": "ui_click", "data": ui_action}
            
        # Check for card click
        clicked_card = self.game.get_card_at_position(pos)
        if clicked_card:
            self.selected_card = clicked_card
            self.drag_start_pos = pos
            self.drag_offset = (
                pos[0] - clicked_card.rect.x,
                pos[1] - clicked_card.rect.y
            )
            return {"action": "card_select", "card": clicked_card}
            
        # Click on empty space
        self.selected_card = None
        return {"action": "deselect"}

    def _handle_left_click_up(self, pos: Tuple[int, int]) -> Dict:
        if self.is_dragging:
            result = self._handle_card_drop(pos)
            self.is_dragging = False
            self.dragging_card = None
            return result
            
        elif self.selected_card:
            # Handle single click actions (like flipping)
            if self.selected_card.rect.collidepoint(pos):
                return self._handle_card_click(self.selected_card)
                
        self.drag_start_pos = None
        return {}

    def _handle_right_click(self, pos: Tuple[int, int]) -> Dict:
        card = self.game.get_card_at_position(pos)
        if card:
            self.right_click_menu = self._create_card_menu(card, pos)
            return {"action": "show_menu", "card": card}
        return {}

    def _handle_mouse_motion(self, pos: Tuple[int, int]) -> Dict:
        result = {}
        
        # Handle dragging
        if self.drag_start_pos and self.selected_card:
            dx = pos[0] - self.drag_start_pos[0]
            dy = pos[1] - self.drag_start_pos[1]
            if not self.is_dragging and (abs(dx) > self.drag_threshold or abs(dy) > self.drag_threshold):
                self.is_dragging = True
                self.dragging_card = self.selected_card
                
        # Update hover card
        self.hover_card = self.game.get_card_at_position(pos)
        
        return result
    
    def _handle_card_drop(self, pos: Tuple[int, int]) -> Dict:
        """Handle dropping a card on a valid zone"""
        target_zone = self.game.get_zone_at_position(pos)
        if target_zone and self._is_valid_drop_target(target_zone):
            self.game.play_card(self.dragging_card, target_zone)
            
    def _handle_card_click(self, card: Card) -> Dict:
        """Handle single clicking a card"""
        if card.can_be_flipped():
            card.is_face_down = not card.is_face_down
        elif card.can_be_previewed():
            self.game.ui_manager.show_card_preview(card)
            
    def _create_card_menu(self, card: Card, pos: Tuple[int, int]) -> Dict:
        """Create context menu for right-clicked card"""
        return {
            'position': pos,
            'options': [
                ('View', lambda: self.game.ui_manager.show_card_preview(card)),
                ('Flip', lambda: setattr(card, 'is_face_down', not card.is_face_down)),
                ('Info', lambda: self.game.ui_manager.show_card_info(card)),
                ('Cancel', lambda: None)
            ]
        }