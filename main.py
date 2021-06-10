
from pygame import *
from pygame.sprite import *
from random import *
import math

Vector2 = pygame.math.Vector2

RESOLUTION = [600, 600]
SWARM_SIZE = 4
ENEMY_SIZE = 0
MAX_SPEED = 4
neighbor_distance = 250
boid0 = Group()
boid1 = Group()
enemies = Group()
clock = pygame.time.Clock()


class Emulation:
    def __init__(self):
        pygame.display.set_caption("Swarm Emulation")
        self.screen = pygame.display.set_mode(RESOLUTION, pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.scene = []
        self.bgcolor = (230, 230, 230)
        self.group_agents = []

    def initGroup(self):
        for i in range(SWARM_SIZE):
            boid0.add(Boid_0(self.screen))
        # for i in range(SWARM_SIZE):
        #     boid1.add(Boid_1(self.screen))
        for i in range(ENEMY_SIZE):
            enemies.add(Enemy(self.screen))
        self.group_agents = [boid0, boid1, enemies]
        pygame.init()

    def run(self):
        """定义刷新函数"""

        self.initGroup()

        while True:
            self.screen.fill(self.bgcolor)
            for agents in self.group_agents:
                for agent in agents:
                    agent.update()
            pygame.display.flip()
            clock.tick(60)


class Boid_0(Sprite):

    def __init__(self, screen):
        super(Boid_0, self).__init__()
        self.screen = screen
        self.img = pygame.image.load("./Enemy_FishGreen.png").convert_alpha()
        self.position = Vector2(uniform(0, RESOLUTION[0]), uniform(0, RESOLUTION[1]))
        self.rect = self.img.get_rect()
        a = uniform(0, math.pi * 2)
        self.v = Vector2(math.cos(a), math.sin(a))
        self.neighbors = Group()
        self.competitors = Group()
        self.enemies = Group()
        self.angle = 0


    def update(self):
        self.neighbors = [b for b in boid0 if b != self and pygame.math.Vector2.length(b.position - self.position) < neighbor_distance]
        self.competitors = [c for c in boid1 if pygame.math.Vector2.length(c.position - self.position) < neighbor_distance]
        self.enemies = [e for e in enemies if pygame.math.Vector2.length(e.position - self.position) < neighbor_distance]


        # self.rule1(self.neighbors)
        # self.rule2(self.neighbors)
        # self.rule3(self.neighbors)
        # self.rule4(self.competitors)
        # self.rule5(self.enemies)
        self.rule_bound()

        # speed ctrl
        if pygame.math.Vector2.length(self.v) > MAX_SPEED:
            self.v /= pygame.math.Vector2.length(self.v)

        # a = uniform(0, math.pi * 2)
        delta = self.v * MAX_SPEED # + 0.002 * Vector2(math.cos(a), math.sin(a))
        self.position += delta
        # self.rule_inner()

        # eating
        for e in enemies:
            if pygame.math.Vector2.length(self.position - e.position) < 30:
                boid0.remove(self)

        self.angle = math.atan((delta[1]) / (delta[0] + 0.000000000000001))
        print(self.angle)
        new_img = pygame.transform.rotate(self.img, self.angle)
        newRect = new_img.get_rect(center=self.position)


        # self.screen.blit(new_img, self.position)
        self.screen.blit(new_img, newRect)

    def rule_bound(self):
        # Stay within screen bounds
        v = Vector2()
        if self.position[0] < 0:
            v[0] = 1
        if self.position[0] >= RESOLUTION[0]-40:
            v[0] = -1
        if self.position[1] < 0:
            v[1] = 1
        if self.position[1] >= RESOLUTION[1]-40:
            v[1] = -1
        self.v += v * 0.5


    def rule1(self, myneighbors):
        # Move to 'center of mass' of neighbors
        if not myneighbors:
            return Vector2(0, 0)
        p = Vector2()
        for n in myneighbors:
            p += n.position
        m = p / len(myneighbors)
        # Startaled
        if False:
            self.v -= (m - self.position) * 0.007
        else:
            self.v += (m - self.position) * 0.001

    def rule2(self, myneighbors):
        # Don't crowd neighbors
        if not myneighbors:
            return Vector2(0, 0)
        c = Vector2()
        for n in myneighbors:
            if pygame.math.Vector2.length(n.position - self.position) < 30:
                c += (self.position - n.position)
        self.v += c * 0.01

    def rule3(self, myneighbors):
        # Match velocity of neighbors
        if not myneighbors:
            return Vector2(0, 0)
        v = Vector2()
        for n in myneighbors:
            v += n.v
        m = v / len(myneighbors)
        self.v += m * 0.01

    def rule4(self, competitors):
        pass

    def rule5(self, myenemies):
        # escape from enemies
        v = Vector2()
        if len(myenemies):
            for e in myenemies:
                v += e.v
            m = v / len(myenemies)
            self.v += -(m - self.position) * 0.0001 - 0.01 * randrange(0, 1) * Vector2(m.y, -m.x) - 0.01 * randrange(0, 1) * Vector2(-m.y, m.x)
        else:
            pass

    def rule_inner(self):
        if self.position.x < 0:
            self.position.x = 0
        elif self.position.x > RESOLUTION[0]-40:
            self.position.x = RESOLUTION[0]-40

        if self.position.y < 0:
            self.position.y = 0
        elif self.position.y > RESOLUTION[1]-40:
            self.position.y = RESOLUTION[1]-40




class Boid_1(Sprite):
    def __init__(self, screen):
        super(Boid_1, self).__init__()
        self.screen = screen
        self.img = pygame.image.load("./Enemy_FishPink.png").convert_alpha()
        self.rect = self.img.get_rect()
        self.position = Vector2(uniform(0, RESOLUTION[0]), uniform(0, RESOLUTION[1]))
        a = uniform(0, math.pi * 2)
        self.v = Vector2(math.cos(a), math.sin(a))

    def update(self):
        self.neighbors = [b for b in boid1 if
                          b != self and pygame.math.Vector2.length(b.position - self.position) < neighbor_distance]
        self.competitors = [c for c in boid0 if
                            pygame.math.Vector2.length(c.position - self.position) < neighbor_distance]
        self.enemies = [e for e in enemies if
                        pygame.math.Vector2.length(e.position - self.position) < neighbor_distance]

        self.rule1(self.neighbors)
        self.rule2(self.neighbors)
        self.rule3(self.neighbors)
        self.rule4(self.competitors)
        self.rule5(self.enemies)
        self.rule_bound()
        if pygame.math.Vector2.length(self.v) > MAX_SPEED:
            self.v /= pygame.math.Vector2.length(self.v)
        self.position += (self.v * MAX_SPEED)
        self.rule_inner()
        # eating
        for e in enemies:
            if pygame.math.Vector2.length(self.position - e.position) < 30:
                boid1.remove(self)

        self.screen.blit(self.img, self.position)

    def rule_bound(self):
        # Stay within screen bounds
        v = Vector2()
        if self.position[0] < 0:
            v[0] = 1
        if self.position[0] >= RESOLUTION[0]-40:
            v[0] = -1
        if self.position[1] < 0:
            v[1] = 1
        if self.position[1] >= RESOLUTION[1]-40:
            v[1] = -1
        self.v += v * 0.5

    def rule1(self, myneighbors):
        # Move to 'center of mass' of neighbors
        if not myneighbors:
            return Vector2(0, 0)
        p = Vector2()
        for n in myneighbors:
            p += n.position
        m = p / len(myneighbors)
        # Startaled
        if False:
            self.v -= (m - self.position) * 0.007
        else:
            self.v += (m - self.position) * 0.001

    def rule2(self, myneighbors):
        # Don't crowd neighbors
        if not myneighbors:
            return Vector2(0, 0)
        c = Vector2()
        for n in myneighbors:
            if pygame.math.Vector2.length(n.position - self.position) < 30:
                c += (self.position - n.position)
        self.v += c * 0.01

    def rule3(self, myneighbors):
        # Match velocity of neighbors
        if not myneighbors:
            return Vector2(0, 0)
        v = Vector2()
        for n in myneighbors:
            v += n.v
        m = v / len(myneighbors)
        self.v += m * 0.01

    def rule4(self, competitors):
        pass

    def rule5(self, myenemies):
        # escape from enemies
        v = Vector2()
        if len(myenemies):
            for e in myenemies:
                v += e.v
            m = v / len(myenemies)
            a = uniform(0, math.pi * 2)
            self.v += -(m - self.position) * 0.0002 - Vector2(math.cos(a), math.sin(a))
        else:
            pass

    def rule_inner(self):
        if self.position.x < 0:
            self.position.x = 0
        elif self.position.x > RESOLUTION[0]-40:
            self.position.x = RESOLUTION[0]-40

        if self.position.y < 0:
            self.position.y = 0
        elif self.position.y > RESOLUTION[1]-40:
            self.position.y = RESOLUTION[1]-40


class Enemy(Sprite):
    def __init__(self, screen):
        super(Enemy, self).__init__()
        self.screen = screen
        self.img = pygame.image.load("./Enemy_FishBlue.png").convert_alpha()
        self.rect = self.img.get_rect()
        self.position = Vector2(uniform(0, RESOLUTION[0]), uniform(0, RESOLUTION[1]))
        a = uniform(0, math.pi * 2)
        self.v = Vector2(math.cos(a), math.sin(a))
        self.preys_0 = Group()
        self.preys_1 = Group()


    def update(self):
        self.preys_0 = [b for b in boid1 if pygame.math.Vector2.length(b.position - self.position) < neighbor_distance]
        self.preys_1 = [c for c in boid0 if pygame.math.Vector2.length(c.position - self.position) < neighbor_distance]

        self.rule_bound()
        self.rule_catch()

        if pygame.math.Vector2.length(self.v) > MAX_SPEED:
            self.v /= pygame.math.Vector2.length(self.v)
        self.position += self.v*MAX_SPEED/2

        self.screen.blit(self.img, self.position)

    def rule_bound(self):
        # Stay within screen bounds
        v = Vector2()
        if self.position[0] < 0:
            v[0] = 1
        if self.position[0] >= RESOLUTION[0]-40:
            v[0] = -1
        if self.position[1] < 0:
            v[1] = 1
        if self.position[1] >= RESOLUTION[1]-40:
            v[1] = -1
        self.v += v * 0.5

    def rule_catch(self):
        v = Vector2()
        v_0 = Vector2()
        v_1 = Vector2()

        if not self.preys_0 and not self.preys_1:
            v.x = randrange(0, 1)
            v.y = randrange(0, 1)
            self.v += v * 0.03
        else:
            min = 114514
            for prey in self.preys_0:
                if pygame.math.Vector2.length(prey.position - self.position) < min:
                    min = pygame.math.Vector2.length(prey.position - self.position)
                    v_0 = prey.position

            min = 114514
            for prey in self.preys_1:
                if pygame.math.Vector2.length(prey.position - self.position) < min:
                    min = pygame.math.Vector2.length(prey.position - self.position)
                    v_1 = prey.position
            v = self.position - (v_0 + v_1)
            self.v += -v * 0.0005

if __name__ == '__main__':
    emu = Emulation()
    emu.run()