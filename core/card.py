import pygame

class Card:
    def __init__(self, name, card_type, effect=None, power=0, image_path=None):
        self.name = name
        self.card_type = card_type
        self.effect = effect
        self.power = power
        self.is_face_down = False
        
        # Create default card surface with text
        self.image = pygame.Surface((100, 150))
        self.image.fill((100, 100, 100))  # Gray background
        
        # Add card name text
        font = pygame.font.Font(None, 24)
        text = font.render(name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(50, 30))
        self.image.blit(text, text_rect)
        
        self.rect = self.image.get_rect()

    def draw(self, surface):
        if self.is_face_down:
            pygame.draw.rect(surface, (50, 50, 150), self.rect)
        else:
            surface.blit(self.image, self.rect)