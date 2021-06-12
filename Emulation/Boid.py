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
    def __init__(self, screen, property):
        super(Boid_0, self).__init__()
        self.screen = screen
        self.property = property
        self.img = pygame.image.load(self.property["SPRITE"]).convert_alpha()
        self.position = Vector2(uniform(0, self.property["RESOLUTION"][0]), uniform(0, self.property["RESOLUTION"][1]))
        self.rect = self.img.get_rect()
        a = uniform(0, math.pi * 2)
        self.v = Vector2(math.cos(a), math.sin(a))
        self.a = 0
        self.neighbors = Group()
        self.competitors = Group()
        self.enemies = Group()
        self.angle = 0

    def update(self):
        """
            responsible for updating the current state of the boid object.
        """

        # scan the neighbors, competitors and enemies in visual range respectively
        self.neighbors = [b for b in self.property["THIS_GROUP"] if b != self and pygame.math.Vector2.length(b.position - self.position) < self.property["NEIGHBOR_DIST"]]
        for comp in self.property["COMP_GROUP"]:
            self.competitors = [c for c in comp if pygame.math.Vector2.length(c.position - self.position) < self.property["NEIGHBOR_DIST"]]
        for enemy in self.property["ENEMY"]:
            self.enemies = [e for e in enemy if pygame.math.Vector2.length(e.position - self.position) < self.property["ENEMY_DIST"]]

        # apply several helpers to modify the boid's location in the next state
        if not len(self.enemies):       # case: no enemies found
            self.rule1(self.neighbors)
            self.rule2(self.neighbors)
            self.rule3(self.neighbors)
            # self.rule4(self.competitors)
        if len(self.enemies):         # case: enemy found
            self.rule5(self.enemies)
        self.rule_bound()

        # controlling the speed
        # make sure it will not exceed the maximum speed limit
        if pygame.math.Vector2.length(self.v) > self.property["MAX_SPEED"]:
            self.v /= pygame.math.Vector2.length(self.v)

        # controlling the acceleration
        # make sure it will not exceed the maximum acceleration limit
        delta = self.v  # get the acceleration vector of the last state
        abs_delta = pygame.math.Vector2.length(delta)  # get the vector's absolute
        direction = self.v / abs_delta  # get the unit vector
        if abs(abs_delta - self.a) <= self.property["MAX_ACC"]:  # check whether the acceleration exceeds the limit
            abs_v = abs_delta  # do nothing if it's fine
        else:
            abs_v = self.property["MAX_ACC"]  # override the acceleration to maximum value (i.e. accelerate to the maximum speed) if it's too large
        self.a = abs_v  # keep the current accelaration value for the next state
        self.position += direction * abs_v

        # detect whether the boid itself has been hunted down
        for e in self.enemies:
            if pygame.math.Vector2.length(self.position - e.position) < 30:
                self.property["THIS_GROUP"].remove(self)        # remove itself from the rendering list
                globe.killist.append(self)                      # remove itself from the enemie's hunting list

        # rotate the sprite image to its corresponding heading direction
        self.angle = - 180 / 3.14 * math.atan2(delta[1], delta[0]) + 180

        # finally, render the context to the screen
        # the second attribute is responsible for make sure the sprite rotate based on the correct center point. see:
        # https://www.cnblogs.com/yjmyzz/p/pygame-tutorial-9-image-rotate.html
        self.screen.blit(pygame.transform.rotate(self.img, self.angle), pygame.transform.rotate(self.img, self.angle).get_rect(center=self.position))

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
            self.v += ((-m + self.position)/pygame.math.Vector2.length(-m + self.position)*randrange(0, self.property["MAX_SPEED"]) + (Vector2(self.property["RESOLUTION"][0]/2, self.property["RESOLUTION"][1]/2)-self.position)*0.001)
