import pygame

def create_enemy_ship(width=40, height=40):
    """Create an enemy ship sprite"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Main body (red triangle)
    pygame.draw.polygon(surface, (255, 0, 0), [(width//2, 0), (0, height), (width, height)])
    
    # Engine flames
    pygame.draw.polygon(surface, (255, 165, 0), 
                       [(width//4, height), (width//4+10, height+5), (width//2, height)])
    pygame.draw.polygon(surface, (255, 165, 0), 
                       [(width//2, height), (width//4*3, height+5), (width//4*3+10, height)])
    
    # Cockpit
    pygame.draw.ellipse(surface, (100, 100, 100), (width//4, height//3, width//2, height//3))
    
    # Wing details
    pygame.draw.line(surface, (200, 200, 200), (5, height-10), (width-5, height-10), 2)
    
    return surface
