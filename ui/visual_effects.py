import pygame
import math
import random
from enum import Enum
from typing import Tuple, Optional, Dict, Any, List

class EffectType(Enum):
    GLOW = "glow"
    FLASH = "flash"
    HIGHLIGHT = "highlight"
    FADE = "fade"
    SHAKE = "shake"
    BOUNCE = "bounce"
    SPARKLE = "sparkle"
    SLIDE = "slide"

class VisualEffect:
    def __init__(self, effect_type: EffectType, duration: int = 30, 
                 color: Tuple[int, int, int] = (255, 255, 255),
                 **kwargs):
        self.type = effect_type
        self.duration = duration
        self.current_frame = 0
        self.color = color
        self.finished = False
        self.properties = kwargs
        
        # Effect-specific properties
        self.offset_x = 0
        self.offset_y = 0
        self.scale = 1.0
        self.particles = []
        
        if effect_type == EffectType.SPARKLE:
            self._init_particles()
            
    def _init_particles(self, count: int = 10):
        """Initialize particles for sparkle effect"""
        for _ in range(count):
            angle = random.random() * 2 * math.pi
            speed = random.uniform(1, 3)
            self.particles.append({
                'x': 0,
                'y': 0,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'life': random.randint(10, 20)
            })
            
    def update(self):
        """Update effect state"""
        self.current_frame += 1
        progress = self.current_frame / self.duration
        
        if self.type == EffectType.SHAKE:
            amplitude = 5 * (1 - progress)
            self.offset_x = random.uniform(-amplitude, amplitude)
            self.offset_y = random.uniform(-amplitude, amplitude)
            
        elif self.type == EffectType.BOUNCE:
            self.offset_y = -20 * math.sin(progress * math.pi) * (1 - progress)
            
        elif self.type == EffectType.SPARKLE:
            self._update_particles()
            
        elif self.type == EffectType.SLIDE:
            start_pos = self.properties.get('start_pos', (0, 0))
            end_pos = self.properties.get('end_pos', (0, 0))
            self.offset_x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
            self.offset_y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress
            
        if self.current_frame >= self.duration:
            self.finished = True
            
    def _update_particles(self):
        """Update sparkle particles"""
        for particle in self.particles:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            
        self.particles = [p for p in self.particles if p['life'] > 0]
        
    def get_alpha(self) -> int:
        """Get current alpha based on effect type and progress"""
        progress = self.current_frame / self.duration
        
        if self.type == EffectType.FLASH:
            return int(255 * (1 - progress))
        elif self.type == EffectType.FADE:
            return int(255 * progress)
        elif self.type == EffectType.GLOW:
            return int(128 + 127 * abs(math.sin(progress * math.pi)))
        else:
            return 128
            
    def apply_to_surface(self, surface: pygame.Surface) -> pygame.Surface:
        """Apply effect to a surface"""
        if self.type in [EffectType.SHAKE, EffectType.BOUNCE, EffectType.SLIDE]:
            new_rect = surface.get_rect(center=(
                surface.get_rect().centerx + self.offset_x,
                surface.get_rect().centery + self.offset_y
            ))
            return surface, new_rect
            
        elif self.type == EffectType.SPARKLE:
            effect_surface = surface.copy()
            for particle in self.particles:
                pygame.draw.circle(
                    effect_surface,
                    self.color,
                    (int(particle['x']), int(particle['y'])),
                    1
                )
            return effect_surface, surface.get_rect()
            
        return surface, surface.get_rect()

class VisualFeedbackManager:
    def __init__(self, screen):
        self.screen = screen
        self.active_effects: Dict[str, List[VisualEffect]] = {}
        
    def add_effect(self, target_id: str, effect_type: EffectType, 
                  duration: int = 30, color: Tuple[int, int, int] = (255, 255, 255),
                  **kwargs):
        """Add a new visual effect"""
        if target_id not in self.active_effects:
            self.active_effects[target_id] = []
            
        effect = VisualEffect(effect_type, duration, color, **kwargs)
        self.active_effects[target_id].append(effect)
        
    def update(self):
        """Update all active effects"""
        for target_id in list(self.active_effects.keys()):
            self.active_effects[target_id] = [
                effect for effect in self.active_effects[target_id]
                if not effect.finished and effect.update() is not None
            ]
            if not self.active_effects[target_id]:
                del self.active_effects[target_id]
                
    def draw_effect(self, target_id: str, surface: pygame.Surface, position: Tuple[int, int]):
        """Draw all effects for a target"""
        if target_id not in self.active_effects:
            return surface, position
            
        result_surface = surface.copy()
        result_position = position
        
        for effect in self.active_effects[target_id]:
            new_surface, new_rect = effect.apply_to_surface(result_surface)
            result_surface = new_surface
            result_position = (
                position[0] + new_rect.x - surface.get_rect().x,
                position[1] + new_rect.y - surface.get_rect().y
            )
            
        return result_surface, result_position 