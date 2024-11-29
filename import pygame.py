import pygame

class Card:
    def __init__(self, name, scripture, effect, power, image_path):
        self.name = name
        self.scripture = scripture
        self.effect = effect
        self.power = power
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (CARD_WIDTH, CARD_HEIGHT))
        self.rect = self.image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)