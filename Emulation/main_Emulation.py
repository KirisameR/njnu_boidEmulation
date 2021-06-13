from pygame import *
from pygame.sprite import *
from Emulation.Boid import Boid_0
from Emulation.Enemy import Enemy
import globe

# rename for convenience
Vector2 = pygame.math.Vector2

# deprecated attributes used to ctrl the behaviour of the boids and enemies
RESOLUTION = [1280, 720]
SWARM_SIZE = 40
ENEMY_SIZE = 1
MAX_SPEED = 6
MAX_SPEED_ENEM = 6
MAX_ACC_BOID = 0.9
MAX_ACC_ENEM = 5


class Emulation:
    """
    DESCRIPTION:
        @author  Yi Lu
        @version 0.2.1
        @desc    The class which maintains code responsible for swarm emulations.

        Method 'initGroup': responsible for initialize the boids and enemies sprite groups
        Method 'run': responsible for firing up the pygame window and loop to refresh the emulation state.
    """
    def __init__(self):
        pygame.display.set_caption("Swarm Emulation")
        self.screen = pygame.display.set_mode(RESOLUTION, pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.scene = []
        self.bgcolor = (230, 230, 230)
        self.group_agents = []

    def initGroup(self):
        """
         responsible for initialize the boids and enemies sprite groups
        """
        # create boid group(s) and the enemy group
        for i in range(globe.boid0_property["GROUP_SIZE"]):
            globe.boid0.add(Boid_0(self.screen, globe.boid0_property))
        for i in range(globe.boid1_property["GROUP_SIZE"]):
            globe.boid1.add(Boid_0(self.screen, globe.boid1_property))
        for i in range(globe.enemy_property["GROUP_SIZE"]):
            globe.enemies.add(Enemy(self.screen, globe.enemy_property))

        self.group_agents = [globe.boid0, globe.boid1, globe.enemies]
        pygame.init()

    def run(self):
        """
         responsible for firing up the pygame window and loop to refresh the emulation state.
        """
        # call the group initialization function
        self.initGroup()

        # loop to refresh the emulation state
        while True:

            self.screen.fill(self.bgcolor)      # refresh the background color
            for agents in self.group_agents:    # for every agents either in the boids group or enemy group, call their 'update' method for refreshing
                for agent in agents:
                    agent.update()
            pygame.display.flip()               # apply the changes and re-render the screen context
            self.clock.tick(60)                      # lock refresh rate to 60fps

    @staticmethod
    def activate():
        emu = Emulation()  # initialize the Emulation object
        emu.run()          # call its 'run' method to fire up the emulation process


Emulation.activate()