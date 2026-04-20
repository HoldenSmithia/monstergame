"""Game constants and configuration."""

import pygame

# Window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 32

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Monster type colors
TYPE_COLORS = {
    "fire": (255, 80, 0),
    "water": (0, 120, 255),
    "grass": (34, 139, 34),
    "electric": (255, 215, 0),
    "ice": (135, 206, 235),
    "fighting": (139, 0, 0),
    "poison": (128, 0, 128),
    "ground": (139, 69, 19),
    "flying": (135, 206, 250),
    "psychic": (255, 105, 180),
    "bug": (154, 205, 50),
    "rock": (112, 128, 144),
    "ghost": (75, 0, 130),
    "dragon": (72, 61, 139),
    "dark": (47, 47, 47),
    "steel": (192, 192, 192),
    "fairy": (255, 182, 193),
    "normal": (169, 169, 169),
}

# Type effectiveness chart (multiplier)
# Format: attacking_type: {defending_type: multiplier}
TYPE_CHART = {
    "fire": {"grass": 2.0, "ice": 2.0, "bug": 2.0, "steel": 2.0, "fire": 0.5, "water": 0.5, "rock": 0.5, "dragon": 0.5},
    "water": {"fire": 2.0, "ground": 2.0, "rock": 2.0, "water": 0.5, "grass": 0.5, "dragon": 0.5},
    "grass": {"water": 2.0, "ground": 2.0, "rock": 2.0, "fire": 0.5, "grass": 0.5, "poison": 0.5, "flying": 0.5, "bug": 0.5, "dragon": 0.5, "steel": 0.5},
    "electric": {"water": 2.0, "flying": 2.0, "electric": 0.5, "grass": 0.5, "dragon": 0.5, "ground": 0.0},
    "ice": {"grass": 2.0, "ground": 2.0, "flying": 2.0, "dragon": 2.0, "fire": 0.5, "water": 0.5, "ice": 0.5, "steel": 0.5},
    "fighting": {"normal": 2.0, "ice": 2.0, "rock": 2.0, "dark": 2.0, "steel": 2.0, "poison": 0.5, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "fairy": 0.5, "ghost": 0.0},
    "poison": {"grass": 2.0, "fairy": 2.0, "poison": 0.5, "ground": 0.5, "rock": 0.5, "ghost": 0.5, "steel": 0.0},
    "ground": {"fire": 2.0, "electric": 2.0, "poison": 2.0, "rock": 2.0, "steel": 2.0, "grass": 0.5, "bug": 0.5, "flying": 0.0},
    "flying": {"grass": 2.0, "fighting": 2.0, "bug": 2.0, "electric": 0.5, "rock": 0.5, "steel": 0.5},
    "psychic": {"fighting": 2.0, "poison": 2.0, "psychic": 0.5, "steel": 0.5, "dark": 0.0},
    "bug": {"grass": 2.0, "psychic": 2.0, "dark": 2.0, "fire": 0.5, "fighting": 0.5, "poison": 0.5, "flying": 0.5, "ghost": 0.5, "steel": 0.5, "fairy": 0.5},
    "rock": {"fire": 2.0, "ice": 2.0, "flying": 2.0, "bug": 2.0, "fighting": 0.5, "ground": 0.5, "steel": 0.5},
    "ghost": {"psychic": 2.0, "ghost": 2.0, "dark": 0.5, "normal": 0.0},
    "dragon": {"dragon": 2.0, "steel": 0.5, "fairy": 0.0},
    "dark": {"psychic": 2.0, "ghost": 2.0, "fighting": 0.5, "dark": 0.5, "fairy": 0.5},
    "steel": {"ice": 2.0, "rock": 2.0, "fairy": 2.0, "fire": 0.5, "water": 0.5, "electric": 0.5, "steel": 0.5},
    "fairy": {"fighting": 2.0, "dragon": 2.0, "dark": 2.0, "fire": 0.5, "poison": 0.5, "steel": 0.5},
    "normal": {"rock": 0.5, "steel": 0.5, "ghost": 0.0},
}

def get_type_multiplier(attacking_type, defending_type):
    """Get the damage multiplier for type matchups."""
    if attacking_type in TYPE_CHART and defending_type in TYPE_CHART[attacking_type]:
        return TYPE_CHART[attacking_type][defending_type]
    return 1.0

# Experience formula
def exp_for_level(level):
    """Experience needed to reach a given level."""
    return int(0.8 * level ** 3)

# Game directories
SAVE_DIR = "saves"
ASSETS_DIR = "assets"
