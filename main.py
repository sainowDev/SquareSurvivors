# main.py
import math
import pygame
import random
from settings import *
from player import Player
from enemy import Enemy
from bullet import Bullet

print("Starting game...")

game_time = 0                   # In Game Seconds

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Upgrades need to be imported after display.set_mode
# For the icons to load properly (otherwise they load before pygame can handle images and crash)
# There is a better way to do this probably but for now this works fine
from upgrades import UPGRADES, get_random_upgrades


player = Player()

enemies = []
bullets = []
damage_numbers = [] # fancy number JUICE

# Whole lotta flags and timers for various mechanics
game_over = False               # Game over flag
enemy_spawn_timer = 0           # Timer for enemy spawning
bullet_timer = 0                # Timer for auto-shooting
shake_timer = 0                 # Timer for screen shake effect
shake_intensity = 0             # Shake intensity on hit
level = 1                       # Current level
level_timer = 0                 # Counts frames for level progression
upgrade_choices = []            # Upgrade options for level-up
choosing_upgrade = False        # Upgrade selection toggle
show_stats = False              # Stats overlay toggle
flash_timer = 0                 # Timer for legendary flash effect

class DamageNumber:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = int(value)
        self.timer = 40  # frames visible

    def update(self):
        self.y -= 1              # float upward
        self.timer -= 1

    def draw(self, screen):
        alpha = max(0, int(255 * (self.timer / 40)))

        text = font.render(str(self.value), True, (255, 80, 80))
        text.set_alpha(alpha)

        screen.blit(text, (self.x, self.y))

running = True
while running:
    clock.tick(FPS)
    screen.fill((25, 25, 25))
    
    game_time += clock.get_time() / 1000  # convert ms to seconds

    # ---------------- EVENTS ----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                show_stats = not show_stats

        if choosing_upgrade and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            for i, key in enumerate(upgrade_choices):
                rect = pygame.Rect(WIDTH // 2 - 120, 200 + i * 80, 240, 60)

                if rect.collidepoint(mouse_x, mouse_y):
                    UPGRADES[key]["effect"](player)
                    choosing_upgrade = False
                    break
        
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:

                # Reset everything
                player = Player()
                enemies.clear()
                bullets.clear()

                level = 1
                level_timer = 0
                enemy_spawn_timer = 0
                bullet_timer = 0
                game_time = 0

                game_over = False

    keys = pygame.key.get_pressed()

    # ---------------- GAME LOGIC ----------------
    if not choosing_upgrade and not show_stats and not game_over:

        # ---------------- PLAYER ----------------
        player.move(keys)
        player.update()
        player.invincible_duration = min(player.invincible_duration, 120) # cap invincibility duration to 2 seconds

        # ---------------- LEVEL SYSTEM ----------------
        level_timer += 1
        if level_timer > FPS * 15:
            level += 1
            level_timer = 0
            
        # ---------------- SPAWN ENEMIES ----------------
        enemy_spawn_timer += 1
        # Difficulty scaling factor (every 50 seconds gets harder)
        difficulty_scale = 1 + (game_time / 50)

        # Calculate dynamic spawn delay
        current_spawn_delay = max(15, ENEMY_SPAWN_DELAY / difficulty_scale)

        if enemy_spawn_timer > current_spawn_delay:
            side = random.choice(["top", "bottom", "left", "right"])

            if side == "top":
                x, y = random.randint(0, WIDTH), 0
            elif side == "bottom":
                x, y = random.randint(0, WIDTH), HEIGHT
            elif side == "left":
                x, y = 0, random.randint(0, HEIGHT)
            else:
                x, y = WIDTH, random.randint(0, HEIGHT)

            # Enemy type scaling based on time
            if game_time < 40:
                enemy_type = "normal"
            elif game_time < 70:
                enemy_type = random.choice(["normal", "fast"])
            else:
                enemy_type = random.choice(["normal", "fast", "tank"])
                
            enemies.append(Enemy(x, y, level, enemy_type))
            enemy_spawn_timer = 0

        # ---------------- AUTO SHOOT ----------------
        bullet_timer += 1
        current_cooldown = BULLET_COOLDOWN + player.bullet_cooldown_bonus

        if bullet_timer > max(5, current_cooldown) and enemies:
            nearest = min(
                enemies,
                key=lambda e: math.hypot(
                    e.rect.centerx - player.rect.centerx,
                    e.rect.centery - player.rect.centery
                )
            )

            # Calculate base direction to nearest enemy
            dx = nearest.rect.centerx - player.rect.centerx
            dy = nearest.rect.centery - player.rect.centery

            # Get base angle in radians
            base_angle = math.atan2(dy, dx)

            for i in range(player.bullets_per_shot):

                # This centers the spread
                offset = (i - (player.bullets_per_shot - 1) / 2)

                # Convert spread to radians
                angle = base_angle + math.radians(offset * player.bullet_spread)

                # Convert angle back into direction
                target_x = player.rect.centerx + math.cos(angle)
                target_y = player.rect.centery + math.sin(angle)

                bullets.append(
                    Bullet(
                        player.rect.centerx,
                        player.rect.centery,
                        target_x,
                        target_y,
                        player.attack,
                        player.pierce   # pass pierce here
                    )
                )

            bullet_timer = 0

        # ---------------- UPDATE ENEMIES ----------------
        for enemy in enemies[:]:
            enemy.move_toward(player.rect)

            if enemy.rect.colliderect(player.rect):
                old_hp = player.hp
                player.take_damage(enemy.damage * 0.1)

                # Only shake if damage was actually taken
                if player.hp < old_hp:
                    shake_timer = 10        # how many frames it lasts
                    shake_intensity = 8     # how strong it shakes

        # ---------------- UPDATE BULLETS ----------------
        for bullet in bullets[:]:
            bullet.update()

            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.take_damage(bullet.damage)
                    damage_numbers.append(
                        DamageNumber(enemy.rect.centerx, enemy.rect.y, bullet.damage)
                    )
                    bullet.pierce -= 1

                    if bullet.pierce < 0:
                        bullets.remove(bullet)

                    if enemy.is_dead():
                        enemies.remove(enemy)
                        leveled_up = player.add_xp(10)

                        if leveled_up:
                            choosing_upgrade = True
                            upgrade_choices = get_random_upgrades()

                    break

        # ---------------- GAME OVER ----------------
        if player.is_dead():
            game_over = True
            
        if game_over:

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            title = font.render("GAME OVER", True, (255, 50, 50))
            screen.blit(title, (WIDTH // 2 - 100, HEIGHT // 2 - 60))

            subtitle = font.render("Press R to Restart", True, (255, 255, 255))
            screen.blit(subtitle, (WIDTH // 2 - 140, HEIGHT // 2))
            
        # ---------------- UPDATE DAMAGE NUMBERS ----------------
        for number in damage_numbers[:]:
            number.update()
            if number.timer <= 0:
                damage_numbers.remove(number)
                
    # ---------------- END OF GAME LOGIC ----------------
    
    
    # ---------------- SHAKE & TIMER RENDERING ----------------
    offset_x = 0
    offset_y = 0

    if shake_timer > 0:
        shake_timer -= 1
        offset_x = random.randint(-shake_intensity, shake_intensity)
        offset_y = random.randint(-shake_intensity, shake_intensity)
    
    minutes = int(game_time // 60)
    seconds = int(game_time % 60)

    timer_text = font.render(f"{minutes:02}:{seconds:02}", True, (255, 255, 255))
    screen.blit(timer_text, (WIDTH - 100, 10))
    
    # ---------------- DRAW GAME ----------------
    player.draw(screen, offset_x, offset_y)

    for enemy in enemies:
        enemy.draw(screen, offset_x, offset_y)

    for bullet in bullets:
        bullet.draw(screen, offset_x, offset_y)
        
        for number in damage_numbers:
            number.draw(screen)

    level_text = font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(level_text, (10, 10))

    # ---------------- DRAW UPGRADE OVERLAY ----------------
    if choosing_upgrade:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        rarity_colors = {
        "common": (255, 255, 255),      # white
        "rare": (255, 215, 0),          # yellow
        "legendary": (160, 60, 200)     # purple
        }

        for i, key in enumerate(upgrade_choices):
            upgrade = UPGRADES[key]

            color = rarity_colors.get(upgrade.get("rarity", "common"), (255,255,255))

            base_x = WIDTH // 2 - 150
            base_y = 200 + i * 80
            
            box_rect = pygame.Rect(base_x - 10, base_y - 10, 320, 70)
            pygame.draw.rect(screen, (40, 40, 40), box_rect)
            pygame.draw.rect(screen, color, box_rect, 2)
            
            if upgrade.get("icon"):
                screen.blit(upgrade["icon"], (base_x, base_y))
                
            text = font.render(upgrade["name"], True, color)
            screen.blit(text, (base_x + 50, base_y))
            
            desc = font.render(upgrade["description"], True, (200, 200, 200))
            screen.blit(desc, (base_x + 50, base_y +  25))
    
            if choosing_upgrade and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                for i, key in enumerate(upgrade_choices):
                    rect = pygame.Rect(WIDTH // 2 - 120, 200 + i * 80, 240, 60)

                    if rect.collidepoint(mouse_x, mouse_y):
                        UPGRADES[key]["effect"](player)

                        if UPGRADES[key]["rarity"] == "legendary":
                            flash_timer = 15

                        choosing_upgrade = False
                        break
            
    # ---------------- DRAW STATS OVERLAY ----------------        
    if show_stats:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        stats = [
            f"Level: {player.level}",
            f"HP: {int(player.hp)} / {int(player.max_hp)}",
            f"Regen: {player.regen:.3f}",
            f"Attack: {player.attack}",
            f"Move Speed: {player.speed}",
            f"Bullet Cooldown Bonus: {player.bullet_cooldown_bonus}",
            f"Bullets Per Shot: {player.bullets_per_shot}",
            f"Bullet Pierce: {player.pierce}",
            f"XP Multiplier: {player.xp_multiplier:.2f}",
            f"I-Frame Duration: {player.invincible_duration}",
            f"Damage Reduction: {int(player.damage_reduction * 100)}%",
            f"",
            f"Press TAB to Close"
            f"Created by @imSynonym on Twitter"
        ]

        for i, stat in enumerate(stats):
            text = font.render(stat, True, (255, 255, 255))
            screen.blit(text, (WIDTH // 2 - 200, 100 + i * 40))
            
    if flash_timer > 0:
        flash_timer -= 1

        flash_surface = pygame.Surface((WIDTH, HEIGHT))
        flash_surface.set_alpha(120)
        flash_surface.fill((180, 0, 255))  # purple flash

        screen.blit(flash_surface, (0, 0))
        
    pygame.display.flip()

pygame.quit()