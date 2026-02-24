# bullet.py

import pygame
import math
from settings import *

class Bullet:
    def __init__(self, x, y, target_x, target_y, damage, pierce):
        self.rect = pygame.Rect(x, y, 8, 8)
        self.damage = damage
        self.pierce = pierce
        self.original_image = pygame.image.load("assets/bullet.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (16, 16))
        
        dx = target_x - x
        dy = target_y - y
        distance = math.hypot(dx, dy)

        speed = 8  # bullet speed

        if distance != 0:
            self.dx = (dx / distance) * speed
            self.dy = (dy / distance) * speed
        else:
            self.dx = 0
            self.dy = 0

        self.angle = math.degrees(math.atan2(-self.dy, self.dx))
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(x, y))
    
    # ---------------- UPDATE ----------------
    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy


    # ---------------- DRAWING ----------------
    def draw(self, screen, offset_x=0, offset_y=0):
        screen.blit(
            self.image,
            (self.rect.x + offset_x,
             self.rect.y + offset_y)
    )