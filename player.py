# player.py

import pygame
from settings import *

class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, 40, 40)
        self.image = pygame.image.load("assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        # Invincibility frames after taking damage
        self.invincible = False             # whether currently invincible
        self.invincible_timer = 0           # frames since last hit
        self.invincible_duration = 20       # 1 second at 60 FPS

        # Stats
        self.max_hp = PLAYER_MAX_HP         # maximum health
        self.hp = self.max_hp               # current health
        self.regen = PLAYER_REGEN           # HP regen per frame
        self.attack = PLAYER_ATTACK         # damage dealt to enemies
        self.xp_multiplier = 1.0            # increases XP gain by this factor
        self.bullet_cooldown_bonus = 0      # reduces bullet cooldown by this amount
        self.speed = PLAYER_SPEED           # movement speed
        self.damage_reduction = 0           # reduces damage by percentage (0.2 = 20%)

        # Leveling system
        self.level = 1                      # starting level
        self.xp = 0                         # starting XP
        self.xp_needed = 50                 # XP needed for next level, increases with each level
        
        # Weapon stats
        self.bullets_per_shot = 1           # bullets shot per attack
        self.bullet_spread = 10             # degrees of spread for bullets
        self.pierce = 0                     # how many enemies bullets can pierce through

    def move(self, keys):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

        # Keep inside screen
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def update(self):
        # Regeneration every frame
        if self.hp < self.max_hp:
            self.hp += self.regen
            if self.hp > self.max_hp:
                self.hp = self.max_hp
        # Handle invincibility timer
        if self.invincible:
            self.invincible_timer += 1
            if self.invincible_timer >= self.invincible_duration:
                self.invincible = False
                self.invincible_timer = 0
    
    def take_damage(self, amount):
        if not self.invincible:
            reduced = amount * (1 - self.damage_reduction)
            self.hp -= reduced
            self.invincible = True

            if self.hp < 0:
                self.hp = 0

    def is_dead(self):
        return self.hp <= 0
    
    def add_xp(self, amount):
        amount *= self.xp_multiplier
        self.xp += amount

        if self.xp >= self.xp_needed:
            self.level += 1
            self.xp -= self.xp_needed
            self.xp_needed = int(self.xp_needed * 1.3)
            return True  # Tell main that we leveled up
        
        return False
    
    # --------------- DRAWING ----------------
    def draw(self, screen, offset_x=0, offset_y=0):

        color = (50, 150, 255)
        if self.invincible:
            color = (255, 255, 255)

        # Draw player rectangle with screen shake offset
    def draw(self, screen, offset_x=0, offset_y=0):
        screen.blit(
        self.image,
        (self.rect.x + offset_x,
         self.rect.y + offset_y)
    )


        # HP bar (also offset!)
        hp_ratio = self.hp / self.max_hp

        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (self.rect.x + offset_x,
             self.rect.y - 10 + offset_y,
             self.rect.width,
             5)
        )

        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (self.rect.x + offset_x,
             self.rect.y - 10 + offset_y,
             self.rect.width * hp_ratio,
             5)
        )

        # XP bar (no shake for UI)
        bar_width = 300
        bar_height = 20
        bar_x = (WIDTH - bar_width) // 2
        bar_y = HEIGHT - 40

        xp_ratio = self.xp / self.xp_needed

        pygame.draw.rect(screen, (60, 60, 60),
                         (bar_x, bar_y, bar_width, bar_height))

        pygame.draw.rect(screen, (0, 200, 255),
                         (bar_x, bar_y, bar_width * xp_ratio, bar_height))