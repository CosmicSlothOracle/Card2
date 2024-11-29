import pygame

class GameMenu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = {
            'resume': pygame.Rect(540, 260, 200, 50),
            'settings': pygame.Rect(540, 320, 200, 50),
            'quit': pygame.Rect(540, 380, 200, 50)
        }
        self.font = pygame.font.Font(None, 36)
        self.visible = False
        
    def toggle(self):
        self.visible = not self.visible
        
    def handle_click(self, pos):
        if not self.visible:
            return None
            
        for action, rect in self.buttons.items():
            if rect.collidepoint(pos):
                return action
        return None
        
    def draw(self):
        if not self.visible:
            return
            
        # Draw semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Draw menu buttons
        for text, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (80, 80, 80), rect)
            pygame.draw.rect(self.screen, (200, 200, 200), rect, 2) 