from .constants import *
import pygame

class LayoutManager:
    def __init__(self, screen):
        self.screen = screen
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Set fullscreen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        
        self.zones = {}
        self.ui_elements = {}
        self._init_zones()
        self._init_ui_elements()
        
        # Load fonts
        self.title_font = pygame.font.Font(None, 36)
        self.main_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 20)

    def _init_zones(self):
        """Initialize zones with proper spacing"""
        # Base measurements
        margin = 40
        zone_spacing = 20
        
        # Calculate zone sizes
        zone_height = (self.screen_height - (margin * 6)) // 6
        deck_width = self.screen_width * 0.15
        mission_width = self.screen_width * 0.6
        vault_width = self.screen_width * 0.15
        
        # Player 2 (Top) row
        top_y = margin
        self.zones.update({
            'P2_DECK': pygame.Rect(
                margin,
                top_y,
                deck_width,
                zone_height
            ),
            'P2_MISSION': pygame.Rect(
                margin * 2 + deck_width,
                top_y,
                mission_width,
                zone_height
            ),
            'P2_VAULT': pygame.Rect(
                self.screen_width - margin - vault_width,
                top_y,
                vault_width,
                zone_height
            )
        })
        
        # Player 2 Sanctuary (upper middle)
        p2_sanctuary_y = top_y + zone_height + zone_spacing
        self.zones['P2_SANCTUARY'] = pygame.Rect(
            margin * 2 + deck_width,
            p2_sanctuary_y,
            mission_width,
            zone_height * 1.5
        )
        
        # Extra Zones (center)
        extra_zone_size = zone_height
        center_y = (self.screen_height - extra_zone_size) // 2
        extra_zone_spacing = zone_spacing * 2
        
        extra_zone1_x = self.screen_width // 2 - extra_zone_size - extra_zone_spacing
        extra_zone2_x = self.screen_width // 2 + extra_zone_spacing
        
        self.zones.update({
            'EXTRA_ZONE_1': pygame.Rect(
                extra_zone1_x,
                center_y,
                extra_zone_size,
                extra_zone_size
            ),
            'EXTRA_ZONE_2': pygame.Rect(
                extra_zone2_x,
                center_y,
                extra_zone_size,
                extra_zone_size
            )
        })
        
        # Player 1 Sanctuary (lower middle)
        p1_sanctuary_y = center_y + extra_zone_size + zone_spacing
        self.zones['P1_SANCTUARY'] = pygame.Rect(
            margin * 2 + deck_width,
            p1_sanctuary_y,
            mission_width,
            zone_height * 1.5
        )
        
        # Player 1 (Bottom) row
        bottom_y = self.screen_height - margin - zone_height
        self.zones.update({
            'P1_DECK': pygame.Rect(
                margin,
                bottom_y,
                deck_width,
                zone_height
            ),
            'P1_MISSION': pygame.Rect(
                margin * 2 + deck_width,
                bottom_y,
                mission_width,
                zone_height
            ),
            'P1_VAULT': pygame.Rect(
                self.screen_width - margin - vault_width,
                bottom_y,
                vault_width,
                zone_height
            )
        })

    def _init_ui_elements(self):
        """Initialize UI elements"""
        # Phase display (top center)
        phase_width = 300
        self.ui_elements['phase'] = {
            'rect': pygame.Rect(
                (self.screen_width - phase_width) // 2,
                10,
                phase_width,
                40
            ),
            'style': {
                'color': GOLD,
                'bg_color': None,
                'border': True
            }
        }
        
        # Turn display (below phase)
        self.ui_elements['turn'] = {
            'rect': pygame.Rect(
                (self.screen_width - phase_width) // 2,
                55,
                phase_width,
                30
            ),
            'style': {
                'color': BLUE_GLOW,
                'bg_color': None,
                'border': True
            }
        }
        
        # Grace/SKP displays (top right)
        stats_width = 200
        self.ui_elements['stats'] = {
            'rect': pygame.Rect(
                self.screen_width - stats_width - 10,
                10,
                stats_width,
                60
            ),
            'style': {
                'color': WHITE,
                'bg_color': None,
                'border': False
            }
        }

    def draw_zones(self):
        """Draw all zones with clean borders"""
        # Fill background
        self.screen.fill(DARK_BLUE)
        
        # Draw each zone
        for zone_name, zone_rect in self.zones.items():
            # Determine zone color
            if 'P1' in zone_name:
                color = GOLD
            elif 'P2' in zone_name:
                color = SILVER
            elif 'EXTRA' in zone_name:
                color = BLUE_GLOW
                
            pygame.draw.rect(self.screen, color, zone_rect, 2)
            
            # Draw zone labels
            label = zone_name.split('_')[-1].title()
            text = self.small_font.render(label, True, color)
            text_rect = text.get_rect(center=(zone_rect.centerx, zone_rect.y - 10))
            self.screen.blit(text, text_rect)

    def get_zone_rect(self, zone_name):
        """Get the rectangle for a specific zone"""
        return self.zones.get(zone_name)

    def get_zone_at_pos(self, pos):
        """Get the zone name at a specific position"""
        for zone_name, zone_rect in self.zones.items():
            if zone_rect.collidepoint(pos):
                return zone_name
        return None

    def draw_ui(self, game_state):
        """Draw all UI elements"""
        # Draw phase
        phase_text = f"Phase: {game_state['current_phase']}"
        self._draw_text_element('phase', phase_text)
        
        # Draw Player 1 stats
        p1_stats = [
            f"Grace: {game_state['p1_grace']}",
            f"SKP: {game_state['p1_skp']}/{game_state['p1_max_skp']}"
        ]
        self._draw_multi_line_text('stats', p1_stats)
        
        # Draw Player 2 stats
        p2_stats = [
            f"Grace: {game_state['p2_grace']}",
            f"SKP: {game_state['p2_skp']}/{game_state['p2_max_skp']}"
        ]
        self._draw_multi_line_text('stats', p2_stats)
        
        # Draw active player indicator
        active_player = "Player 1" if game_state['active_player'] == 0 else "Player 2"
        self._draw_text_element('turn', f"Turn: {active_player}")

    def _draw_text_element(self, element_name, text):
        """Draw a single text UI element"""
        element = self.ui_elements[element_name]
        rect = element['rect']
        style = element['style']
        
        # Draw background if specified
        if style['bg_color']:
            pygame.draw.rect(self.screen, style['bg_color'], rect)
        
        # Draw border if specified
        if style['border']:
            pygame.draw.rect(self.screen, style['color'], rect, 2)
        
        # Draw text
        text_surface = self.main_font.render(text, True, style['color'])
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def _draw_multi_line_text(self, element_name, lines):
        """Draw multiple lines of text in a UI element"""
        element = self.ui_elements[element_name]
        rect = element['rect']
        style = element['style']
        
        for i, line in enumerate(lines):
            text_surface = self.small_font.render(line, True, style['color'])
            text_rect = text_surface.get_rect(
                left=rect.left,
                top=rect.top + (i * 20)
            )
            self.screen.blit(text_surface, text_rect)

    def highlight_zone(self, zone_name, color=GREEN):
        """Highlight a zone (for valid card placement)"""
        if zone_name in self.zones:
            zone_rect = self.zones[zone_name]
            s = pygame.Surface((zone_rect.width, zone_rect.height))
            s.set_alpha(128)
            s.fill(color)
            self.screen.blit(s, zone_rect)