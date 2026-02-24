# enemy.py

import pygame
import math
from settings import *

class Enemy:
    def __init__(self, x, y, level, enemy_type="normal"):
        self.type = enemy_type
        self.type = enemy_type
        
        # Load sprite based on type
        if self.type == "normal":
            self.image = pygame.image.load("assets/enemy_normal.png").convert_alpha()
        elif self.type == "tank":
            self.image = pygame.image.load("assets/enemy_tank.png").convert_alpha()
        elif self.type == "fast":
            self.image = pygame.image.load("assets/enemy_fast.png").convert_alpha()

        # Scale AFTER loading
        self.image = pygame.transform.scale(self.image, (48, 48))

        # Create rect AFTER scaling
        self.rect = self.image.get_rect(center=(x, y))
        
        # ---------------- BASE STATS ----------------
        base_hp = ENEMY_BASE_HP + (level * 2)
        base_damage = ENEMY_BASE_DAMAGE + (level * 1.5)
        base_speed = ENEMY_BASE_SPEED + (level * 0.2)

        # ---------------- TYPE MODIFIERS ----------------
        if self.type == "tank":
            self.max_hp = base_hp * 2
            self.damage = base_damage * 1.3
            self.speed = base_speed * 0.6
            self.color = (160, 60, 200)  # purple

        elif self.type == "fast":
            self.max_hp = base_hp * 0.6
            self.damage = base_damage * 0.8
            self.speed = base_speed * 1.6
            self.color = (255, 140, 0)  # orange

        else:  # normal
            self.max_hp = base_hp
            self.damage = base_damage
            self.speed = base_speed
            self.color = (200, 50, 50) # red

        self.hp = self.max_hp

    def move_toward(self, player_rect):
        dx = player_rect.x - self.rect.x
        dy = player_rect.y - self.rect.y

        distance = math.hypot(dx, dy)
        if distance != 0:
            dx /= distance
            dy /= distance

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def take_damage(self, amount):
        self.hp -= amount

    def is_dead(self):
        return self.hp <= 0

    # ---------------- DRAWING ----------------
    def draw(self, screen, offset_x=0, offset_y=0):
        screen.blit(self.image,
        (self.rect.x + offset_x,
         self.rect.y + offset_y)
        )
    

        # HP bar
        hp_ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, (255, 0, 0),
                         (self.rect.x + offset_x, self.rect.y - 6 + offset_y, self.rect.width, 4))
        pygame.draw.rect(screen, (0, 255, 0),
                         (self.rect.x + offset_x, self.rect.y - 6 + offset_y,
                          self.rect.width * hp_ratio, 4))