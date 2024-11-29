import pygame
import sys
import os

# Add the game directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enum import Enum

class CardType(Enum):
    CREATURE = "Creature"

from game.core.card import Card

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Create a test card
    test_card = Card(
        name="Test Card",
        card_type=CardType.CREATURE,
        effect=None
    )
    test_card.rect.x = 300
    test_card.rect.y = 200

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                test_card.is_face_down = not test_card.is_face_down
        
        screen.fill((50, 50, 50))  # Dark gray background
        test_card.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main() 