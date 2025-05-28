import pygame

def create_enemy_bullet(width=5, height=15):
    """Create an enemy bullet sprite"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Red bullet with glow effect
    pygame.draw.rect(surface, (255, 0, 0), (0, 0, width, height))
    pygame.draw.rect(surface, (255, 200, 200), (1, 1, width-2, height-2))
    pygame.draw.rect(surface, (255, 255, 200), (2, 2, width-4, height-4))
    
    return surface

def create_hero_bullet(width=5, height=15):
    """Create a hero bullet sprite"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Blue bullet with glow effect
    pygame.draw.rect(surface, (0, 0, 255), (0, 0, width, height))
    pygame.draw.rect(surface, (200, 200, 255), (1, 1, width-2, height-2))
    pygame.draw.rect(surface, (200, 255, 255), (2, 2, width-4, height-4))
    
    return surface
