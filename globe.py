from pygame.sprite import *
import globe

"""
DESCRIPTION: responsible for storing global values. not elegant, but necessary for miantaining the enemy's killist     
"""

boid0 = Group()
boid1 = Group()
enemies = Group()
killist = []
cache = {"./Enemy_FishGreen.png": {}, "./Enemy_FishPink.png": {}, "./Enemy_FishBlue.png": {}}
RESOLUTION = [1280, 720]

# declare the main properties for ctrling the beaviour of the boids and enemies
boid0_property = {
    "RESOLUTION": RESOLUTION,
    "SPRITE": "./Enemy_FishGreen.png",
    "GROUP_SIZE": 40,
    "MAX_SPEED": 6,
    "MAX_ACC": 0.9,
    "NEIGHBOR_DIST": 720/3,
    "ENEMY_DIST": 720/2,
    "COMPETITOR_DIST": 720/3,
    "THIS_GROUP": globe.boid0,
    "COMP_GROUP": [globe.boid1],
    "ENEMY": [globe.enemies],
}
boid1_property = {
    "RESOLUTION": RESOLUTION,
    "SPRITE": "./Enemy_FishPink.png",
    "GROUP_SIZE": 40,
    "MAX_SPEED": 6,
    "MAX_ACC": 0.9,
    "NEIGHBOR_DIST": 720/3,
    "ENEMY_DIST": 720/2,
    "COMPETITOR_DIST": 720/3,
    "THIS_GROUP": globe.boid1,
    "COMP_GROUP": [globe.boid0],
    "ENEMY": [globe.enemies],
}
enemy_property = {
    "RESOLUTION": RESOLUTION,
    "SPRITE": "./Enemy_FishBlue.png",
    "GROUP_SIZE": 1,
    "MAX_SPEED": 6,
    "MAX_ACC": 2.9,
    "DETECT_DIST": 350,
    "PREYS": [globe.boid0, globe.boid1],
}

