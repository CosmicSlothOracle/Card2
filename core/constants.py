import os
import pygame

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WOOD_COLOR = (139, 69, 19)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
GLOW_COLOR = (255, 215, 0)

# Asset directories
ASSET_DIR = os.path.join('assets')
CARD_BACK_IMAGE = os.path.join(ASSET_DIR, 'card_back.png')
WOOD_TEXTURE = os.path.join(ASSET_DIR, 'wood_texture.jpg')
PLAYER_AVATAR = os.path.join(ASSET_DIR, 'player_avatar.png')
OPPONENT_AVATAR = os.path.join(ASSET_DIR, 'opponent_avatar.png')

# Fonts
pygame.font.init()
FONT_LARGE = pygame.font.Font(None, 48)
FONT_MEDIUM = pygame.font.Font(None, 36)
FONT_SMALL = pygame.font.Font(None, 24)

# Card dimensions
CARD_WIDTH = 100
CARD_HEIGHT = 150

# Game constants
MAX_HAND_SIZE = 7
STARTING_LIFE = 20 