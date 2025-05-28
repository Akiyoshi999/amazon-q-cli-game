import pygame
import random

def create_explosion_frames(num_frames=8, size=50):
    """Create a series of explosion animation frames"""
    frames = []
    
    for i in range(num_frames):
        # Create a surface for this frame
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Calculate explosion size for this frame (grows then shrinks)
        if i < num_frames // 2:
            radius = int((i + 1) * size / (num_frames // 2) / 2)
        else:
            radius = int((num_frames - i) * size / (num_frames // 2) / 2)
        
        # Colors change from bright yellow/orange to red/black
        if i < num_frames // 2:
            inner_color = (255, 255, 0)  # Bright yellow
            outer_color = (255, 165, 0)  # Orange
        else:
            inner_color = (255, 100, 0)  # Orange-red
            outer_color = (100, 0, 0)    # Dark red
        
        # Draw the explosion
        pygame.draw.circle(surface, outer_color, (size//2, size//2), radius)
        pygame.draw.circle(surface, inner_color, (size//2, size//2), radius//2)
        
        # Add some random particles
        for _ in range(10):
            particle_size = random.randint(1, 3)
            x = random.randint(size//2 - radius, size//2 + radius)
            y = random.randint(size//2 - radius, size//2 + radius)
            pygame.draw.circle(surface, (255, 255, 200), (x, y), particle_size)
        
        frames.append(surface)
    
    return frames
