from pygame import *
from pygame.sprite import *
from random import *
import math
import globe


class Enemy(Sprite):
    """
    DESCRIPTION:
        @author  Yi Lu
        @version 0.2.1
        @desc    The class which maintains code responsible for modeling enemies.

        Method 'update': responsible for updating the current state of the enemy object.
        Method 'rule_bound": an location-transition helper responsible for keeping the agent inside the screen border.
        Method 'rule_catch": an location-transition helper responsible for modeling the 'catch-and-hunt' behaviour.
    """
    def __init__(self, screen, properties):
        super(Enemy, self).__init__()
        self.screen = screen
        self.property = properties
        self.img = pygame.image.load(self.property["SPRITE"]).convert_alpha()
        self.rect = self.img.get_rect()
        self.position = Vector2(uniform(0, self.property["RESOLUTION"][0]), uniform(0, self.property["RESOLUTION"][1]))
        a = uniform(0, math.pi * 2)
        self.v = Vector2(math.cos(a), math.sin(a))
        self.a = 0
        self.preys = []
        self.killist = []
        self.angle = 0
        self.focus_point = [randrange(0, self.property["RESOLUTION"][0]), randrange(0, self.property["RESOLUTION"][1])]

    def update(self):
        """
        responsible for updating the current state of the enemy object.
        """
        # scan to find any preys within the enemy's prey-detection distance
        for preys in self.property["PREYS"]:
            tmp_preys = [b for b in preys if pygame.math.Vector2.length(b.position - self.position) < self.property["DETECT_DIST"]]
            self.preys.append(tmp_preys)

        # apply two helpers to modify the enemy's location in the next state
        self.rule_bound()
        self.rule_catch()

        # controlling the speed
        # make sure it will not exceed the maximum speed limit
        if pygame.math.Vector2.length(self.v) > self.property["MAX_SPEED"]:
            self.v /= pygame.math.Vector2.length(self.v) * self.property["MAX_SPEED"]

        # controlling the acceleration
        # make sure it will not exceed the maximum acceleration limit
        delta = self.v                                  # get the acceleration vector of the last state
        abs_delta = pygame.math.Vector2.length(delta)   # get the vector's absolute
        direction = self.v / abs_delta                  # get the unit vector
        if abs(abs_delta - self.a) <= self.property["MAX_ACC"]:     # check whether the acceleration exceeds the limit
            abs_v = abs_delta                           # do nothing if it's fine
        else:
            abs_v = self.property["MAX_SPEED"]            # override the acceleration to maximum value (i.e. accelerate to the maximum speed) if it's too large
        self.a = abs_v                                  # keep the current accelaration value for the next state
        self.position += direction * abs_v

        # rotate the sprite image to its corresponding heading direction
        self.angle = int(- 180 / 3.14 * math.atan2(delta[1], delta[0]) + 180)
        if not globe.cache[self.property["SPRITE"]].__contains__(self.angle):  # cache the image if not found in self.cache to improve performance
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
            self.position[0] = 0    # override the location
            v[0] = 1    # bounce back
        if self.position[0] >= self.property["RESOLUTION"][0] - 40:
            self.position[0] = self.property["RESOLUTION"][0] - 40  # override the location
            v[0] = -1   # bounce back
        if self.position[1] < 0:
            self.position[1] = 0    # override the location
            v[1] = 1    # bounce back
        if self.position[1] >= self.property["RESOLUTION"][1] - 40:
            self.position[1] = self.property["RESOLUTION"][1] - 40  # override the location
            v[1] = -1   # bounce back
        self.v += v * 0.5

    def rule_catch(self):
        """
        an location-transition helper responsible for modeling the 'catch-and-hunt' behaviour.

        Modeling Baseline:
        we do not consider cooperation among the enemies (predators) now.
        case0: The enemy cannot found any preys inside its visual range:
               it will wander around. it pick one random point and move towards it. it will choose another random point when it reached the old one.
        case1: The enemy found several preys.
               it will hunt the closest one.
        """
        min_dist = float("inf")    # initialize the maximum distance for comparision
        nearest_prey = Vector2()   # initialize the nearest prey to catch
        for preys in self.preys:   # group of preys
            for prey in preys:     # prey in each groups
                if prey not in globe.killist:   # only consider the preys which haven't been killed
                    if pygame.math.Vector2.length(prey.position - self.position) <= min_dist:   # select the nearest prey to hunt
                        min_dist = pygame.math.Vector2.length(prey.position - self.position)
                        nearest_prey = prey.position

        if nearest_prey:   # case1: prey found, head to the nearest prey and try to catch it
            self.v += (nearest_prey - self.position)/pygame.math.Vector2.length(nearest_prey - self.position) * 0.04

        else:   # case0: : no preys found, wander around
            # check whether the enemy has moved close to the old point
            if pygame.math.Vector2.length(self.position - self.focus_point) <= 100:
                # pick a new point if so
                self.focus_point = randrange(0, self.property["RESOLUTION"][0]), randrange(0, self.property["RESOLUTION"][1])
            self.v += 0.02 * (Vector2(self.focus_point) - self.position)

    def rule_disperse(self):
        """
        *DEPRECATED*
        an location-transition helper responsible for modeling the 'enemy dispersed by large group of boids' behaviour.

        Modeling Baseline:
        The enemy will be dispersed by a large group of boids.
        """
        count = 0
        for preys in self.preys:   # group of preys
            for prey in preys:     # prey in each groups
                if prey not in globe.killist:   # only consider the preys which haven't been killed
                    count += 1
        return count >= 30