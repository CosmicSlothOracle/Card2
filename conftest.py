import pytest
import pygame
from game.game import TestamentDuelGame

@pytest.fixture
def screen():
    pygame.init()
    return pygame.display.set_mode((1280, 720))

@pytest.fixture
def clock():
    return pygame.time.Clock()

@pytest.fixture
def game(screen, clock):
    return TestamentDuelGame(screen, clock)
