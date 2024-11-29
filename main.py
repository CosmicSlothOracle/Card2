import pygame
import sys
from game.game import TestamentDuelGame

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60
WHITE = (255, 255, 255)
FONT_SIZE = 20
CARD_WIDTH, CARD_HEIGHT = 100, 150

def main():
    # Initialize pygame
    pygame.init()
    
    # Setup display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Testament Duel")
    clock = pygame.time.Clock()
    
    # Create and run game
    game = TestamentDuelGame(screen, clock)
    game.run()

if __name__ == "__main__":
    main()