# settings.py

WIDTH = 1000             # in pixels
HEIGHT = 800            # in pixels
FPS = 60                # frames per second (duh)

# Player stats
PLAYER_SPEED = 3        # pixels per frame
PLAYER_MAX_HP = 45     # increases with upgrades
PLAYER_REGEN = 0.02     # HP per frame
PLAYER_ATTACK = 10      # damage dealt to enemies per bullet hit, increases with upgrades

# Enemy base stats
ENEMY_BASE_HP = 20      # increases with level
ENEMY_BASE_DAMAGE = 10  # damage dealt to player on contact, increases with level
ENEMY_BASE_SPEED = 1    # pixels per frame, increases with level

# Shooting
BULLET_SPEED = 8        # pixels per frame
BULLET_COOLDOWN = 55    # frames between shots, decreases with upgrades

# Spawning
ENEMY_SPAWN_DELAY = 90  # frames between spawns, decreases with level