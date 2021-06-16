from pygame import *
from pygame.sprite import *
from random import *
import math
import globe


class Boid_0(Sprite):
    """
    DESCRIPTION:
        @author  Yi Lu
        @version 0.2.1
        @desc    The class which maintains code responsible for modeling boids.

        Method 'update': responsible for updating the current state of the boid object.
        Method 'rule_bound': an location-transition helper responsible for keeping the agent inside the screen border.
        Method 'rule_1': an location-transition helper responsible for modeling the behavior that every boid tends to move to the center of the mass of its neighbors.
        Method 'rule_2': an location-transition helper responsible for modeling the behavior that every boid tends to crowed out if the group is too intense.
        Method 'rule_3': an location-transition helper responsible for modeling the behavior that every boid tends to match the velocity of its group.
        Method 'rule_4': not implemented yet
        Method 'rule_5': an location-transition helper responsible for modeling the behavior that the boid tends to run away from the enemy
    """
    def __init__(self, screen, properties, flag):
        super(Boid_0, self).__init__()
        self.screen = screen
        self.property = properties
        self.img = pygame.image.load(self.property["SPRITE"]).convert_alpha()
        self.position = Vector2(uniform(0, self.property["RESOLUTION"][0]), uniform(0, self.property["RESOLUTION"][1]))
        self.rect = self.img.get_rect()
        a = uniform(0, math.pi * 2)
        self.v = Vector2(math.cos(a), math.sin(a))
        self.a = 0
        self.neighbors = []
        self.competitors = []
        self.enemies = []
        self.angle = 0
        self.focus_point = [randrange(0, self.property["RESOLUTION"][0]), randrange(0, self.property["RESOLUTION"][1])]
        self.cache = {}
        self.flag = flag
        self.isKilled = False

    def update(self):
        """
            responsible for updating the current state of the boid object.
        """
        if self.isKilled:
            return
        # scan the neighbors, competitors and enemies in visual range respectively
        self.neighbors = [b for b in globe.boids[self.flag] if b != self and pygame.math.Vector2.length(b.position - self.position) < self.property["NEIGHBOR_DIST"] and not b.isKilled]
        # deprecated: we will not try do model the behaviour between prey groups T^T
        # for comp in self.property["COMP_GROUP"]:
        #    self.competitors = [c for c in comp if pygame.math.Vector2.length(c.position - self.position) < self.property["NEIGHBOR_DIST"] and c not in globe.killist]
        for enemy in self.property["ENEMY"]:
            self.enemies = [e for e in enemy if pygame.math.Vector2.length(e.position - self.position) < self.property["ENEMY_DIST"]]

        # apply several helpers to modify the boid's location in the next state
        if not self.enemies:       # case: no enemies found
            self.rule1(self.neighbors)
            self.rule2(self.neighbors)
            self.rule3(self.neighbors)
            # self.rule4(self.competitors)
        else:         # case: enemy found
            self.rule2(self.neighbors)
            self.rule5(self.enemies)
        self.rule_bound()

        # controlling the speed
        # make sure it will not exceed the maximum speed limit
        if pygame.math.Vector2.length(self.v) > self.property["MAX_SPEED"]:
            self.v /= pygame.math.Vector2.length(self.v) * self.property["MAX_SPEED"]

        # controlling the acceleration
        # make sure it will not exceed the maximum acceleration limit
        delta = self.v  # get the acceleration vector of the last state
        abs_delta = pygame.math.Vector2.length(delta)  # get the vector's absolute
        direction = self.v / abs_delta  # get the unit vector
        if abs(abs_delta - self.a) <= self.property["MAX_ACC"]:  # check whether the acceleration exceeds the limit
            abs_v = abs_delta  # do nothing if it's fine
        else:
            abs_v = self.property["MAX_SPEED"]  # override the acceleration to maximum value (i.e. accelerate to the maximum speed) if it's too large
        self.a = abs_v  # keep the current accelaration value for the next state
        self.position += direction * abs_v

        # detect whether the boid itself has been hunted down
        for e in self.enemies:
            if pygame.math.Vector2.length(self.position - e.position) < 20:
                globe.boids[self.flag].remove(self)        # remove itself from the rendering list
                self.isKilled = True                       # remove itself from the enemie's hunting list

        # rotate the sprite image to its corresponding heading direction
        self.angle = int(- 180 / 3.14 * math.atan2(delta[1], delta[0]) + 180)
        if not globe.cache[self.property["SPRITE"]].__contains__(self.angle):     # cache the image if not found in self.cache to improve performance
            globe.cache[self.property["SPRITE"]].update({self.angle: pygame.transform.rotate(self.img, self.angle)})
        # finally, render the context to the screen
        # the second attribute is responsible for make sure the sprite rotate based on the correct center point. see:
        # https://www.cnblogs.com/yjmyzz/p/pygame-tutorial-9-image-rotate.html
        self.screen.blit(globe.cache[self.property["SPRITE"]][self.angle], globe.cache[self.property["SPRITE"]][self.angle].get_rect(center=self.position))

    def rule_bound(self):
        """
        an location-transition helper responsible for keeping the agent inside the screen border.
        if the agent is going to exceed the border, we force override its location back inside the border so it's still viewable...
        and we modify its acceleration direction to bounce it back.
        """
        # Stay within screen bounds
        v = Vector2()
        if self.position[0] < 0:
            self.position[0] = 0  # override the location
            v[0] = 1  # bounce back
        if self.position[0] >= self.property["RESOLUTION"][0] - 40:
            self.position[0] = self.property["RESOLUTION"][0] - 40  # override the location
            v[0] = -1  # bounce back
        if self.position[1] < 0:
            self.position[1] = 0  # override the location
            v[1] = 1  # bounce back
        if self.position[1] >= self.property["RESOLUTION"][1] - 40:
            self.position[1] = self.property["RESOLUTION"][1] - 40  # override the location
            v[1] = -1  # bounce back
        self.v += v * 0.5

    def rule1(self, myneighbors):
        """
        an location-transition helper responsible for modeling the behavior...
        which every boid tends to move to the center of the mass of its neighbors.
        :param myneighbors:  receive the list of its neighbors to compute the 'center of the mass'.
        """

        # case0: no neighbors in visual range
        if not myneighbors:
            return Vector2()
        # case1: found several neighbors in visual range
        p = Vector2()
        for n in myneighbors:
            p += n.position
        m = p / len(myneighbors)

        # Startaled: deprecated feature
        if False:
            self.v -= (m - self.position) * 0.007
        else:
            self.v += (m - self.position) * 0.001

    def rule2(self, myneighbors):
        """
        rule_2": an location-transition helper responsible for modeling the behavior which every boid tends to crowed out if the group is too intense.
        :param myneighbors: receive the list of its neighbors to check whether it's crowd or not.
        """

        if not myneighbors:     # case0: no neighbors in visual range
            return Vector2()

        c = Vector2()
        for n in myneighbors:   # case1: found several neighbors in visual range
            if abs(pygame.math.Vector2.length(n.position - self.position)) < 40:
                c += (self.position - n.position)
        self.v += c * 0.02      # crowd out if the distance is too small

    def rule3(self, myneighbors):
        """
        Method 'rule_3": an location-transition helper responsible for modeling the behavior which every boid tends to match the velocity of its group.
        :param myneighbors: receive the list of its neighbors to compute the main velocity of the group
        """
        if not myneighbors:     # case0: no neighbors in visual range
            return Vector2()
        v = Vector2()
        for n in myneighbors:   # case1: found several neighbors in visual range
            v += n.v
        m = v / len(myneighbors)
        self.v += m * 0.01      # match the main velocity of the group

    def rule4(self, competitors):
        pass

    def rule5(self, myenemies):
        """
         Method 'rule_5': an location-transition helper responsible for modeling the behavior that the boid tends to run away from the enemy
        :param myenemies: receive the list of its enemies to compute the escaping direction
        """
        v = Vector2()
        if len(myenemies):
            for e in myenemies:
                v += e.position
            m = v / len(myenemies)
            self.v += (0.07*((-m + self.position)/pygame.math.Vector2.length(-m + self.position)))

        # case: close to the dead corners
        if (self.position[0] <= 50 or self.position[0] >= self.property["RESOLUTION"][0] - 50) and (self.position[1] <= 50 or self.position[1] >= self.property["RESOLUTION"][1] - 50):
            if pygame.math.Vector2.length(self.position - self.focus_point) <= 100:
                # pick a new point if so
                self.focus_point = randrange(0, self.property["RESOLUTION"][0]), randrange(0, self.property["RESOLUTION"][1])
            self.v += 0.05 * (Vector2(self.focus_point) - self.position)
