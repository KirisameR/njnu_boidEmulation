from pygame import *
from pygame.sprite import *

import globe
import time
# rename for convenience
from Emulation.Boid import Boid_0
from Emulation.Enemy import Enemy
Vector2 = pygame.math.Vector2


class Emulation:
    """
    DESCRIPTION:
        @author  Yi Lu
        @desc    The class which maintains code responsible for swarm emulations.

        Method 'initGroup': responsible for initialize the boids and enemies sprite groups
        Method 'run': responsible for firing up the pygame window and loop to refresh the emulation state.
    """
    def __init__(self, screen, settings):
        self.screen = screen
        self.scene = []
        self.bgcolor = (230, 230, 230)
        self.group_agents = []
        self.boids = []
        self.enemies = []
        self.clock = pygame.time.Clock()
        self.settings = settings

    def initGroup(self):
        """
         responsible for initialize the boids and enemies sprite groups
        """
        # globe.init()
        # create boid group(s) and the enemy group
        for i in range(globe.NUM_BOIDS):
            for j in range(self.settings["Boids"][i]["GROUP_SIZE"]):
                globe.boids[i].append(Boid_0(self.screen, self.settings["Boids"][i], i))

        for i in range(globe.NUM_ENEMIES):
            for j in range(self.settings["Enemy"]["GROUP_SIZE"]):
                globe.enemies[i].append(Enemy(self.screen, self.settings["Enemy"], i))

        self.boids = globe.boids
        self.enemies = globe.enemies
        self.group_agents = globe.boids + globe.enemies
        pygame.init()

    def run(self):
        """
         responsible for firing up the pygame window and loop to refresh the emulation state.
        """
        # call the group initialization function
        self.initGroup()

        # loop to refresh the emulation state
        while True:
            self.screen.fill(self.bgcolor)  # refresh the background color
            for agents in self.group_agents:    # for every agents either in the boids group or enemy group, call their 'update' method for refreshing
                for agent in agents:
                    agent.update()

            pygame.display.flip()               # apply the changes and re-render the screen context
            self.clock.tick(60)                      # lock refresh rate to 60fps

    def update(self):
        """
        responsible for updating the pygame subwindow responsible for emulation and loop to refresh the emulation state.
        """
        self.screen.fill(self.bgcolor)      # refresh the background color
        for agents in self.group_agents:    # for every agents either in the boids group or enemy group, call their 'update' method for refreshing
            for agent in agents:
                agent.update()
        self.clock.tick(60)                 # lock refresh rate to 60fps