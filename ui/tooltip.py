import pygame
from typing import List, Tuple, Optional, Dict
from enum import Enum

class TooltipStyle(Enum):
    DEFAULT = "default"
    CARD = "card"
    ZONE = "zone"
    ACTION = "action"
    WARNING = "warning"

class TooltipTheme:
    def __init__(self, 
                 background_color: Tuple[int, int, int, int],
                 text_color: Tuple[int, int, int],
                 border_color: Tuple[int, int, int],
                 header_color: Optional[Tuple[int, int, int]] = None):
        self.background_color = background_color
        self.text_color = text_color
        self.border_color = border_color
        self.header_color = header_color or text_color

class Tooltip:
    def __init__(self, screen, font, padding: int = 10):
        self.screen = screen
        self.font = font
        self.padding = padding
        self.themes = self._init_themes()
        self.current_tooltip = None
        self.fade_progress = 0
        self.fade_duration = 10
        
    def _init_themes(self) -> Dict[TooltipStyle, TooltipTheme]:
        """Initialize tooltip themes"""
        return {
            TooltipStyle.DEFAULT: TooltipTheme(
                (30, 30, 30, 230),  # Dark gray background
                (255, 255, 255),    # White text
                (200, 200, 200)     # Light gray border
            ),
            TooltipStyle.CARD: TooltipTheme(
                (20, 35, 50, 240),  # Dark blue background
                (255, 255, 255),    # White text
                (0, 150, 255),      # Blue border
                (255, 215, 0)       # Gold header
            ),
            TooltipStyle.ZONE: TooltipTheme(
                (40, 20, 50, 240),  # Dark purple background
                (255, 255, 255),    # White text
                (180, 120, 255),    # Purple border
                (200, 200, 255)     # Light purple header
            ),
            TooltipStyle.ACTION: TooltipTheme(
                (20, 50, 20, 240),  # Dark green background
                (255, 255, 255),    # White text
                (100, 255, 100),    # Green border
                (150, 255, 150)     # Light green header
            ),
            TooltipStyle.WARNING: TooltipTheme(
                (50, 20, 20, 240),  # Dark red background
                (255, 255, 255),    # White text
                (255, 100, 100),    # Red border
                (255, 150, 150)     # Light red header
            )
        }
        
    def show(self, pos: Tuple[int, int], lines: List[str], 
             style: TooltipStyle = TooltipStyle.DEFAULT,
             header: Optional[str] = None,
             max_width: Optional[int] = None):
        """Show tooltip with fade-in effect"""
        self.current_tooltip = {
            'pos': pos,
            'lines': lines,
            'style': style,
            'header': header,
            'max_width': max_width
        }
        self.fade_progress = 0
        
    def hide(self):
        """Hide current tooltip"""
        self.current_tooltip = None
        
    def update(self):
        """Update tooltip state"""
        if self.current_tooltip and self.fade_progress < self.fade_duration:
            self.fade_progress += 1
            
    def draw(self):
        """Draw current tooltip if active"""
        if not self.current_tooltip:
            return
            
        pos = self.current_tooltip['pos']
        lines = self.current_tooltip['lines']
        style = self.current_tooltip['style']
        header = self.current_tooltip['header']
        max_width = self.current_tooltip['max_width']
        
        theme = self.themes[style]
        
        # Calculate dimensions
        text_surfaces = []
        if header:
            header_surface = self.font.render(header, True, theme.header_color)
            text_surfaces.append(header_surface)
            
        text_surfaces.extend([
            self.font.render(line, True, theme.text_color)
            for line in lines
        ])
        
        max_text_width = max(surface.get_width() for surface in text_surfaces)
        total_height = sum(surface.get_height() for surface in text_surfaces)
        
        # Create tooltip surface
        width = min(max_text_width + self.padding * 2, max_width or float('inf'))
        height = total_height + self.padding * 2
        
        # Adjust position to keep tooltip on screen
        x, y = pos
        if x + width > self.screen.get_width():
            x = self.screen.get_width() - width
        if y + height > self.screen.get_height():
            y = self.screen.get_height() - height
            
        # Create surface with alpha for fade effect
        alpha = int(255 * (self.fade_progress / self.fade_duration))
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Draw background with fade
        background_color = (*theme.background_color[:3], 
                          int(theme.background_color[3] * alpha / 255))
        pygame.draw.rect(surface, background_color, surface.get_rect())
        
        # Draw border with fade
        border_color = (*theme.border_color, alpha)
        pygame.draw.rect(surface, border_color, surface.get_rect(), 2)
        
        # Draw text
        y_offset = self.padding
        for i, text_surface in enumerate(text_surfaces):
            text_color = theme.header_color if i == 0 and header else theme.text_color
            text_surface.set_alpha(alpha)
            surface_rect = text_surface.get_rect(topleft=(self.padding, y_offset))
            surface.blit(text_surface, surface_rect)
            y_offset += text_surface.get_height()
            
        # Draw tooltip
        self.screen.blit(surface, (x, y))