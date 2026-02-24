# upgrades.py

import pygame
import random

# ---------------------------------------------
# ALL POSSIBLE UPGRADES 
# ---------------------------------------------

UPGRADES = {
    # ----- Common Upgrades -----
    
"power_training": {
    "name": "Power Training",
    "description": "+4 Attack",
    "rarity": "common",
    "effect": lambda p: setattr(p, "attack", p.attack + 4),
    "icon": pygame.image.load("assets/upgrades/power_training.png").convert_alpha()
    },

"quick_step": {
    "name": "Quick Step",
    "description": "+0.5 Speed",
    "rarity": "common",
    "effect": lambda p: setattr(p, "speed", p.speed + 0.5),
    "icon": pygame.image.load("assets/upgrades/quick_step.png").convert_alpha()
    },

"vitality": {
    "name": "Vitality",
    "description": "+15 Max HP",
    "rarity": "common",
    "effect": lambda p: setattr(p, "max_hp", p.max_hp + 15),
    "icon": pygame.image.load("assets/upgrades/vitality.png").convert_alpha()
    },

"recovery": {
    "name": "Recovery",
    "description": "+0.015 Regen",
    "rarity": "common",
    "effect": lambda p: setattr(p, "regen", p.regen + 0.015),
    "icon": pygame.image.load("assets/upgrades/recovery.png").convert_alpha()
    },

"focus": {
    "name": "Focus",
    "description": "-5 Bullet Cooldown",
    "rarity": "common",
    "effect": lambda p: setattr(p, "bullet_cooldown_bonus",
                                p.bullet_cooldown_bonus - 5),
    "icon": pygame.image.load("assets/upgrades/focus.png").convert_alpha()
    },

"combat_reflex": {
    "name": "Combat Reflex",
    "description": "+5 I-Frames",
    "rarity": "common",
    "effect": lambda p: setattr(p, "invincible_duration",
                                p.invincible_duration + 5),
    "icon": pygame.image.load("assets/upgrades/combat_reflex.png").convert_alpha()
    },

    # ----- Rare Upgrades -----
    
"twin_barrel": {
    "name": "Twin Barrel",
    "description": "+1 Bullet Per Shot",
    "rarity": "rare",
    "effect": lambda p: setattr(p, "bullets_per_shot",
                                p.bullets_per_shot + 1),
    "icon": pygame.image.load("assets/upgrades/twin_barrel.png").convert_alpha()
},

"armor_plating": {
    "name": "Armor Plating",
    "description": "-15% Damage Taken",
    "rarity": "rare",
    "effect": lambda p: setattr(p, "damage_reduction",
                                p.damage_reduction + 0.15),
    "icon": pygame.image.load("assets/upgrades/armor_plating.png").convert_alpha()
},

"deep_wounds": {
    "name": "Deep Wounds",
    "description": "+10 Attack",
    "rarity": "rare",
    "effect": lambda p: setattr(p, "attack", p.attack + 10),
    "icon": pygame.image.load("assets/upgrades/deep_wounds.png").convert_alpha()
},

"piercing_rounds": {
    "name": "Piercing Rounds",
    "description": "+1 Pierce",
    "rarity": "rare",
    "effect": lambda p: setattr(p, "pierce", p.pierce + 1),
    "icon": pygame.image.load("assets/upgrades/piercing_rounds.png").convert_alpha()
},

    # ----- Legendary Upgrades -----

"bullet_fury": {
    "name": "Bullet Fury",
    "description": "+2 Bullets & -10 Cooldown",
    "rarity": "legendary",
    "effect": lambda p: (
        setattr(p, "bullets_per_shot", p.bullets_per_shot + 2),
        setattr(p, "bullet_cooldown_bonus",
                p.bullet_cooldown_bonus - 10)
    ),
    "icon": pygame.image.load("assets/upgrades/bullet_fury.png").convert_alpha()
},

"unstoppable": {
    "name": "Unstoppable",
    "description": "+30 HP, +20 I-Frames",
    "rarity": "legendary",
    "effect": lambda p: (
        setattr(p, "max_hp", p.max_hp + 30),
        setattr(p, "invincible_duration",
                p.invincible_duration + 20)
    ),
    "icon": pygame.image.load("assets/upgrades/unstoppable.png").convert_alpha()
},
}

# -----------------------------------------------
# LOAD UPGRADE ICONS   
# -----------------------------------------------

for key, upgrade in UPGRADES.items():
    try:
        image = pygame.image.load(f"assets/upgrades/{key}.png").convert_alpha()
        upgrade["icon"] = pygame.transform.scale(image, (48, 48))
    except:
        upgrade["icon"] = None

# ---------------------------------------------
# GET 3 RANDOM UPGRADES
# ---------------------------------------------

def get_random_upgrades():

    commons = [k for k, v in UPGRADES.items() if v["rarity"] == "common"]
    rares = [k for k, v in UPGRADES.items() if v["rarity"] == "rare"]
    legendaries = [k for k, v in UPGRADES.items() if v["rarity"] == "legendary"]

    choices = []

    while len(choices) < 3:

        roll = random.random()

        if roll < 0.70 and commons:
            pick = random.choice(commons)

        elif roll < 0.95 and rares:
            pick = random.choice(rares)

        elif legendaries:
            pick = random.choice(legendaries)

        else:
            pick = random.choice(list(UPGRADES.keys()))

        if pick not in choices:
            choices.append(pick)

    return choices