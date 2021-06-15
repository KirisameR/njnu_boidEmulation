from pygame.sprite import *
import globe

"""
DESCRIPTION: responsible for storing global values. not elegant, but necessary for miantaining the enemy's killist     
"""


# The number of boids/enemies groups should be provided by the GUI
NUM_BOIDS = 2
NUM_ENEMIES = 1

# Declaration of basic properties list and boids/enemies group list
boids = []
boids_property = []
enemies = []
enemies_property = []

killist = []
cache = {}
RESOLUTION = [800, 680]

# generate the group lists' skeleton based on two fundamental attributes: NUM_BOIDS and NUM_ENEMIES
for i in range(NUM_BOIDS):
    boids.append([])
for i in range(NUM_ENEMIES):
    enemies.append([])

# The properties of each group must be specified
boid0_property = {
    "RESOLUTION": RESOLUTION,
    "SPRITE": "./asset/Enemy_FishGreen.png",
    "GROUP_SIZE": 20,
    "MAX_SPEED": 6,
    "MAX_ACC": 0.9,
    "NEIGHBOR_DIST": 720 / 3,
    "ENEMY_DIST": 720 / 2,
    "COMPETITOR_DIST": 720 / 3,
    "THIS_GROUP": globe.boids[0],
    "COMP_GROUP": [globe.boids[1]],
    "ENEMY": [globe.enemies[0]],
}
boid1_property = {
    "RESOLUTION": RESOLUTION,
    "SPRITE": "./asset/Enemy_FishPink.png",
    "GROUP_SIZE": 20,
    "MAX_SPEED": 6,
    "MAX_ACC": 0.9,
    "NEIGHBOR_DIST": 720 / 3,
    "ENEMY_DIST": 720 / 2,
    "COMPETITOR_DIST": 720 / 3,
    "THIS_GROUP": globe.boids[1],
    "COMP_GROUP": [globe.boids[0]],
    "ENEMY": [globe.enemies[0]],
}
enemy_property = {
    "RESOLUTION": RESOLUTION,
    "SPRITE": "./asset/Enemy_FishBlue.png",
    "GROUP_SIZE": 1,
    "MAX_SPEED": 6,
    "MAX_ACC": 2.9,
    "DETECT_DIST": 350,
    "PREYS": globe.boids,
}


def init():
    # declare the main properties for ctrling the beaviour of the boids and enemies
    globe.boids_property = [globe.boid0_property, globe.boid1_property]
    globe.enemies_property = [globe.enemy_property]

    # construct cache based on the given properties
    for j in range(NUM_BOIDS):
        globe.cache.update({boids_property[j]["SPRITE"]: {}})
    for j in range(NUM_ENEMIES):
        globe.cache.update({enemies_property[j]["SPRITE"]: {}})
    print(globe.cache)
