from pygame.sprite import *

"""
DESCRIPTION: responsible for storing global values. not elegant, but necessary for miantaining the enemy's killist     
"""

boid0 = Group()
boid1 = Group()
enemies = Group()
killist = []
cache = {"./Enemy_FishGreen.png": {}, "./Enemy_FishPink.png": {}, "./Enemy_FishBlue.png": {}}
