import pygame

def create_hero_ship(width=40, height=40):
    """Create a hero ship sprite"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Main body (blue)
    pygame.draw.polygon(surface, (0, 0, 255), [(width//2, height), (0, 0), (width, 0)])
    
    # Engine flames
    pygame.draw.polygon(surface, (0, 255, 255), 
                       [(width//4, 0), (width//4+10, -5), (width//2, 0)])
    pygame.draw.polygon(surface, (0, 255, 255), 
                       [(width//2, 0), (width//4*3, -5), (width//4*3+10, 0)])
    
    # Cockpit
    pygame.draw.ellipse(surface, (200, 200, 255), (width//4, height//3, width//2, height//3))
    
    # Wing details
    pygame.draw.line(surface, (100, 100, 255), (5, 10), (width-5, 10), 2)
    
    return surface
