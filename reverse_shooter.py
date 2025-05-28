import pygame
import random
import sys
import math
import os

# Import sprite creation functions
sys.path.append(os.path.join(os.path.dirname(__file__), 'assets'))
from enemy_ship import create_enemy_ship
from hero_ship import create_hero_ship
from bullet import create_enemy_bullet, create_hero_bullet
from explosion import create_explosion_frames

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Reverse Shooter - Control the Enemy!")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game variables
clock = pygame.time.Clock()
FPS = 60
game_over = False
score = 0
font = pygame.font.SysFont(None, 36)

# Load sprites
enemy_ship_img = create_enemy_ship(50, 50)
hero_ship_img = create_hero_ship(50, 50)
enemy_bullet_img = create_enemy_bullet(8, 20)
hero_bullet_img = create_hero_bullet(8, 20)
explosion_frames = create_explosion_frames(8, 60)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Enemy ship (player controlled)
        self.image = enemy_ship_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5
        self.cooldown = 0
        self.health = 100
        
    def update(self):
        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
            
        # Cooldown for shooting
        if self.cooldown > 0:
            self.cooldown -= 1
            
    def shoot(self):
        if self.cooldown == 0:
            bullet = Bullet(self.rect.centerx, self.rect.top, -1)  # -1 means shooting upward
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)
            self.cooldown = 15  # Cooldown time
            
class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Hero ship (AI controlled)
        self.image = hero_ship_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.top = 50
        self.speed_x = 3
        self.speed_y = 1
        self.direction = 1  # 1 for right, -1 for left
        self.cooldown = 0
        self.health = 100
        self.movement_timer = 0
        self.movement_change = 60  # Change direction every 60 frames
        
    def update(self):
        # Move from one end of the screen to the other
        self.rect.x += self.speed_x * self.direction
        
        # Change direction when reaching screen edges
        if self.rect.left <= 0:
            self.direction = 1  # Move right
            self.rect.y += random.randint(-20, 20)  # Random vertical movement
        elif self.rect.right >= SCREEN_WIDTH:
            self.direction = -1  # Move left
            self.rect.y += random.randint(-20, 20)  # Random vertical movement
            
        # Keep within top half of screen
        if self.rect.top < 10:
            self.rect.top = 10
        if self.rect.bottom > SCREEN_HEIGHT // 2:
            self.rect.bottom = SCREEN_HEIGHT // 2
            
        # Cooldown for shooting
        if self.cooldown > 0:
            self.cooldown -= 1
        
        # Random shooting
        if random.random() < 0.02 and self.cooldown == 0:  # 2% chance to shoot each frame
            self.shoot()
            
    def shoot(self):
        if self.cooldown == 0:
            bullet = Bullet(self.rect.centerx, self.rect.bottom, 1)  # 1 means shooting downward
            all_sprites.add(bullet)
            hero_bullets.add(bullet)
            self.cooldown = 30  # Cooldown time

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        if direction == 1:  # Hero's bullet
            self.image = hero_bullet_img
        else:  # Player's bullet
            self.image = enemy_bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = 7 * direction
        
    def update(self):
        self.rect.y += self.speedy
        # Remove if it goes off screen
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()
hero_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()

# Create game objects
player = Player()
hero = Hero()
all_sprites.add(player)
all_sprites.add(hero)

# Health bars
def draw_health_bar(surface, x, y, health, width=100, height=10):
    fill = (health / 100) * width
    outline_rect = pygame.Rect(x, y, width, height)
    fill_rect = pygame.Rect(x, y, fill, height)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

# Game loop
running = True
while running:
    # Keep game running at the right speed
    clock.tick(FPS)
    
    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            if event.key == pygame.K_ESCAPE:
                running = False
    
    if not game_over:
        # Update
        all_sprites.update()
        
        # Check for collisions - hero bullets hitting player
        hits = pygame.sprite.spritecollide(player, hero_bullets, True)
        for hit in hits:
            player.health -= 10
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            all_sprites.add(explosion)
            explosions.add(explosion)
            if player.health <= 0:
                game_over = True
                
        # Check for collisions - player bullets hitting hero
        hits = pygame.sprite.spritecollide(hero, enemy_bullets, True)
        for hit in hits:
            hero.health -= 10
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            all_sprites.add(explosion)
            explosions.add(explosion)
            score += 10
            if hero.health <= 0:
                game_over = True
    
    # Draw / render
    screen.fill(BLACK)
    
    # Draw stars in the background
    for i in range(100):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        size = random.randint(1, 2)
        brightness = random.randint(150, 255)
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)
    
    all_sprites.draw(screen)
    
    # Draw health bars
    draw_health_bar(screen, 10, 10, hero.health)
    draw_health_bar(screen, SCREEN_WIDTH - 110, 10, player.health)
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 30))
    
    # Draw game over message
    if game_over:
        if hero.health <= 0:
            message = "You Win! You defeated the hero!"
        else:
            message = "Game Over! The hero defeated you!"
        
        game_over_text = font.render(message, True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2))
        
        restart_text = font.render("Press R to restart or ESC to quit", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset game
            game_over = False
            score = 0
            all_sprites = pygame.sprite.Group()
            hero_bullets = pygame.sprite.Group()
            enemy_bullets = pygame.sprite.Group()
            explosions = pygame.sprite.Group()
            player = Player()
            hero = Hero()
            all_sprites.add(player)
            all_sprites.add(hero)
    
    # Flip the display
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = explosion_frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame_rate = 2  # Update every 2 game frames
        self.counter = 0
        
    def update(self):
        self.counter += 1
        if self.counter >= self.frame_rate:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.frame_index]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center
