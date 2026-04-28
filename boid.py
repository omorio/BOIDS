from random import uniform, randint
import colorsys
import pygame
from helpers import num_to_range, getDistance, SubVectors, makeBound,rotate_points_around_pivot, dotProduct # pylint: disable=W0611

HEIGHT = 1964
WIDTH = 3024

# Behaviour scaling applied uniformly to all three steering forces
BEHAVIOUR_SCALE = 0.8
# Edge avoidance: proportional softening as a boid approaches the margin
EDGE_APPROACH_SCALE = 0.05
# Cohesion only activates beyond this fraction of the vision radius (avoids overcrowding)
MIN_COHESION_DIVISOR = 4
# Extra overlap buffer used by separation to detect near-collisions
SEP_OVERLAP_BUFFER = 2
# Vision radius adaptation
MAX_VISION_RADIUS = 120
MIN_VISION_RADIUS = 60
VISION_ADJUST_STEP = 10
VISION_BUDDY_MIN = 3   # fewer than this → expand vision
VISION_BUDDY_MAX = 6   # more than this → shrink vision
# Hue range mapped from velocity magnitude
HUE_MIN = 100
HUE_MAX = 360
# HSV saturation and value for live boid colour
COLOR_SAT = 115 / 255.0
COLOR_VAL = 1.0

class Boid:
    def __init__(self, x, y, boidID):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(uniform(-2, 2), uniform(-2, 2))
        self.acceleration = pygame.Vector2()
        self.minSpeed = 1
        self.maxSpeed = 6
        self.radius = 6  # Radius of blob
        self.vRadius = 60  # Vision rectangle WIDTH and HEIGHT.
        # defines the vision area.
        self.vRect = pygame.Rect(self.position.x - self.vRadius / 2, self.position.y - self.vRadius / 2, self.vRadius, self.vRadius)
        # Used to be found in the Quad Tree.
        self.rect = pygame.Rect(self.position.x - self.radius / 2, self.position.y - self.radius / 2, self.radius, self.radius)
        self.neighbours = []
        self.boidID = boidID
        self.colorID = randint(1, 8)
        velToHue = num_to_range(self.velocity.magnitude(), 0, self.maxSpeed, 0, HUE_MAX)
        self.color = colorsys.hsv_to_rgb(velToHue / HUE_MAX, COLOR_SAT, COLOR_VAL)
        self.color = (int (round (self.color[0] * 255)), int (self.color[1] * 255), int (self.color[2] * 255))

        if self.colorID == 1:
            self.color = (255, 150, 0)
        if self.colorID == 2:
            self.color = (0, 255, 255)
        if self.colorID == 3:
            self.color = (255, 0, 255)
        if self.colorID == 4:
            self.color = (0, 255, 0)
        if self.colorID == 5:
            self.color = (0, 150, 255)
        if self.colorID == 6:
            self.color = (255, 255, 0)
        if self.colorID == 7:
            self.color = (255, 128, 255)
        if self.colorID == 8:
            self.color = (0, 0, 255)

    def edges(
        self, avoid, margin, turnFactor
    ):  # Determines what happens when a boid reaches an edge of the window
        if avoid:
            if self.position.x < margin:
                self.velocity.x += turnFactor * ((margin - self.position.x) * EDGE_APPROACH_SCALE)
            if self.position.y > HEIGHT - margin:
                self.velocity.y += turnFactor * (
                    (HEIGHT - margin - self.position.y) * EDGE_APPROACH_SCALE
                )
            if self.position.x > WIDTH - margin:
                self.velocity.x += turnFactor * (
                    (WIDTH - margin - self.position.x) * EDGE_APPROACH_SCALE
                )
            if self.position.y < margin:
                self.velocity.y += turnFactor * ((margin - self.position.y) * 0.05)

                # calulate dot product between vel vector and the vec that is perpendicular to the edge.
                # if dot product positive it is moving towards it.

                # then calculate the angle between velocity vect and boundary and steer by a small fraction of this angle.
                # the dot product help determine if to move in the positive or negative direction.
        else:
            if self.position.x > WIDTH:
                self.position.x = 0
            elif self.position.x < 0:
                self.position.x = WIDTH

            if self.position.y > HEIGHT:
                self.position.y = 0
            elif self.position.y < 0:
                self.position.y = HEIGHT

    def behaviour(self, quadTree, values):
        self.acceleration.update(0, 0)
        self.neighbours = quadTree.findInRect(self.vRect)
        align = self.alignment(self.neighbours) * BEHAVIOUR_SCALE
        align = align * values["alignment"]
        self.acceleration += align

        coh = self.cohesion(self.neighbours) * BEHAVIOUR_SCALE
        coh = coh * values["cohesion"]
        self.acceleration += coh

        sep = self.separation(self.neighbours) * BEHAVIOUR_SCALE
        sep = sep * values["separation"]
        self.acceleration += sep

    def cohesion(self, neighbours):
        total = 0
        steering = pygame.Vector2(0, 0)

        for buddy in neighbours:
            dist = getDistance(self.position, buddy.position)
            if buddy is not self and self.vRadius/MIN_COHESION_DIVISOR < dist < self.vRadius and self.colorID == buddy.colorID:
                steering += buddy.position

                total += 1

        if total > 0:
            steering = steering / total
            steering = steering - self.position
            if steering.length_squared() > 0:
                steering = steering.normalize()
            steering = steering * self.maxSpeed
            steering = steering - self.velocity
            if steering.length_squared() > 0:
                steering = steering.normalize()

        return steering

    def alignment(self, neighbours):
        total = 0
        averageHeading = pygame.Vector2(0, 0)

        for buddy in neighbours:
            dist = getDistance(self.position, buddy.position)
            if buddy is not self and dist < self.vRadius and self.colorID == buddy.colorID:
                vel = buddy.velocity.normalize()
                averageHeading += vel

                total += 1

        if total > 0:
            averageHeading = averageHeading / total
            averageHeading = averageHeading.normalize()
            averageHeading = averageHeading * self.maxSpeed

            averageHeading = averageHeading - self.velocity.normalize()
            averageHeading = averageHeading.normalize()

        return averageHeading

    def separation(self, neighbours):
        total = 0
        steering = pygame.Vector2(0, 0)
        danger = False

        for buddy in neighbours:
            dist = getDistance(self.position, buddy.position)
            if dist != 0:
                if buddy is not self and dist < self.radius + SEP_OVERLAP_BUFFER:
                    temp = SubVectors(self.position, buddy.position)
                    temp = temp / (dist**2)
                    steering += temp

                    total += 1
        if total > 0:
            steering = steering / total
            steering = steering.normalize()
            if danger:
                steering = steering * (self.maxSpeed + 10)
                steering = steering - self.velocity
            else:
                steering = steering * self.maxSpeed
                steering = steering - self.velocity
                if steering.length_squared() > 0:
                    steering = steering.normalize()

        return steering

    def update(self, dragCoeff):
        # increases the boids vision if it cant see any flock members, decrease if it can see more than 3
        buddyCount = 0
        for boid in self.neighbours:
            if self.colorID == boid.colorID:
                buddyCount += 1

        if buddyCount <= VISION_BUDDY_MIN:
            if self.vRadius < MAX_VISION_RADIUS:
                self.vRadius += VISION_ADJUST_STEP
        elif buddyCount > VISION_BUDDY_MAX:
            if self.vRadius > MIN_VISION_RADIUS:
                self.vRadius -= VISION_ADJUST_STEP

        # update the possitional values of the boid
        self.velocity = pygame.Vector2(self.velocity.x * (1-dragCoeff), self.velocity.y * (1-dragCoeff))
        self.position += self.velocity
        self.velocity = self.velocity + self.acceleration
        self.velocity = self.velocity.clamp_magnitude(self.minSpeed, self.maxSpeed)

        # Map velocity to hue of boid
        velToHue = num_to_range(self.velocity.magnitude(), 0, self.maxSpeed, HUE_MIN, HUE_MAX)
        self.color = colorsys.hsv_to_rgb(velToHue / HUE_MAX, COLOR_SAT, COLOR_VAL)
        self.color = (int (round (self.color[0] * 255)), int (round (self.color[1] * 255)), int (round (self.color[2] * 255)))

        self.vRect = pygame.Rect(
            self.position.x - self.vRadius / 2,
            self.position.y - self.vRadius / 2,
            self.vRadius,
            self.vRadius,
        )
        self.rect = pygame.Rect(
            self.position.x - self.radius / 2,
            self.position.y - self.radius / 2,
            self.radius,
            self.radius,
        )

    def draw(self, window):
        pygame.draw.circle(window, self.color, (makeBound(self.position.x, 0, WIDTH), makeBound(self.position.y, 0, HEIGHT),),self.radius)
        pygame.draw.aaline(window, self.color, (self.position.x, self.position.y), (self.position.x + self.velocity.x * 3, self.position.y + self.velocity.y * 3))

        # Uncomment the bellow lines to turn the boids into triangles instead

        #p1 = pygame.Vector2(self.position.x + (self.radius * 3), self.position.y)
        #p2 = pygame.Vector2(p1.x - self.radius * 3, p1.y - self.radius)
        #p3 = pygame.Vector2(p2.x, p2.y + self.radius)
        #p4 = pygame.Vector2(p3.x, p3.y + self.radius)
        #p5 = p1

        #triangle = [p1, p2, p3, p4, p5]
        #triangle = rotate_points_around_pivot(triangle, p3, dotProduct(pygame.Vector2(0,0), self.velocity))

        #pygame.draw.polygon(window, self.color, triangle)
