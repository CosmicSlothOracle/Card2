import pygame
import math
from typing import Tuple, Optional, Dict, Callable

class CardAnimation:
    def __init__(self, start_pos: Tuple[float, float], end_pos: Tuple[float, float],
                 duration: int, easing: str = "ease_out_cubic",
                 on_complete: Optional[Callable] = None):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.duration = duration
        self.current_frame = 0
        self.easing = easing
        self.on_complete = on_complete
        self.finished = False
        
    def update(self) -> Tuple[float, float]:
        """Update animation and return current position"""
        if self.finished:
            return self.end_pos
            
        self.current_frame += 1
        progress = self.current_frame / self.duration
        
        if progress >= 1:
            self.finished = True
            if self.on_complete:
                self.on_complete()
            return self.end_pos
            
        # Apply easing function
        t = self._ease(progress)
        
        # Calculate current position
        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * t
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * t
        
        return (x, y)
        
    def _ease(self, t: float) -> float:
        """Apply easing function to progress"""
        if self.easing == "linear":
            return t
        elif self.easing == "ease_out_cubic":
            return 1 - pow(1 - t, 3)
        elif self.easing == "ease_out_bounce":
            n1 = 7.5625
            d1 = 2.75
            
            if t < 1 / d1:
                return n1 * t * t
            elif t < 2 / d1:
                t -= 1.5 / d1
                return n1 * t * t + 0.75
            elif t < 2.5 / d1:
                t -= 2.25 / d1
                return n1 * t * t + 0.9375
            else:
                t -= 2.625 / d1
                return n1 * t * t + 0.984375

class CardAnimator:
    def __init__(self):
        self.animations: Dict[int, CardAnimation] = {}
        
    def animate_card(self, card_id: int, start_pos: Tuple[float, float],
                    end_pos: Tuple[float, float], duration: int = 30,
                    easing: str = "ease_out_cubic",
                    on_complete: Optional[Callable] = None):
        """Start a new card animation"""
        self.animations[card_id] = CardAnimation(
            start_pos, end_pos, duration, easing, on_complete
        )
        
    def update(self):
        """Update all active animations"""
        finished_animations = []
        
        for card_id, animation in self.animations.items():
            if animation.finished:
                finished_animations.append(card_id)
                
        for card_id in finished_animations:
            del self.animations[card_id]
            
    def get_card_position(self, card_id: int) -> Optional[Tuple[float, float]]:
        """Get current position of animated card"""
        if animation := self.animations.get(card_id):
            return animation.update()
        return None 