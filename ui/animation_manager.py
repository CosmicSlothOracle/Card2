import pygame
from typing import Dict, List, Callable
from dataclasses import dataclass
import math

@dataclass
class Animation:
    target: pygame.Surface
    start_pos: tuple
    end_pos: tuple
    duration: int
    easing: Callable
    callback: Callable = None
    
class AnimationManager:
    def __init__(self):
        self.animations: List[Animation] = []
        self.completed_animations: List[Animation] = []
        
    def add_animation(self, animation: Animation):
        """Add new animation to queue"""
        self.animations.append(animation)
        
    def update(self, dt: float):
        """Update all active animations"""
        remaining_animations = []
        
        for anim in self.animations:
            progress = min(1.0, dt / anim.duration)
            eased_progress = anim.easing(progress)
            
            # Calculate new position
            current_x = anim.start_pos[0] + (anim.end_pos[0] - anim.start_pos[0]) * eased_progress
            current_y = anim.start_pos[1] + (anim.end_pos[1] - anim.start_pos[1]) * eased_progress
            
            # Update target position
            anim.target.rect.x = current_x
            anim.target.rect.y = current_y
            
            if progress < 1.0:
                remaining_animations.append(anim)
            else:
                if anim.callback:
                    anim.callback()
                self.completed_animations.append(anim)
                
        self.animations = remaining_animations
        
    def clear_completed(self):
        """Clear completed animations"""
        self.completed_animations.clear() 