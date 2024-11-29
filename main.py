import pygame
import sys
from game.game import TestamentDuelGame

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Testament Duel")
    clock = pygame.time.Clock()
    
    game = TestamentDuelGame(screen, clock)
    game.run()

if __name__ == "__main__":
    main()