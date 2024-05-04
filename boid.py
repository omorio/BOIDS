from random import uniform, randint
import colorsys
import pygame
from helpers import num_to_range, getDistance, SubVectors, makeBound



HEIGHT = 1964
WIDTH = 3024

class Boid:
    def __init__(self, x, y, boidID):
        self.position = pygame.Vector2(x, y)
        vel_x = uniform(-2, 2)
        vel_y = uniform(-2, 2)
        self.velocity = pygame.Vector2(vel_x, vel_y)
        self.acceleration = pygame.Vector2()
        self.min_speed = 1  # 1
        self.max_speed = 6  # 3 was original
        self.size = 2
        self.angle = 0
        self.lineThicknes = 2
        self.radius = 6  # Radius of blob
        self.vRadius = 60  # Vision square WIDTH and HEIGHT.
        self.vRect = pygame.Rect(  # defines the vision area.
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
        self.neighbours = []
        self.boidID = boidID
        self.colorID = randint(5, 5)
        velToHue = num_to_range(self.velocity.magnitude(),0,4,0,360)
        self.color = colorsys.hsv_to_rgb(velToHue / 360.0, 100 / 255.0, 100 / 255.0) #Need to normalize the colors
        self.color = (int (round (self.color[0] * 255)), int (self.color[1] * 255), int (self.color[2] * 255))
        self.values = {"separation": 1, "alignment": 1, "cohesion": 1}

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
        # self.color = (255, 255, 255)

    def edges(
        self, avoid, margin, turnFactor
    ):  # Determines what happens when a boid reaches an edge of the window
        if avoid:
            if self.position.x < margin:
                self.velocity.x += turnFactor * ((margin - self.position.x) * 0.05)
            if self.position.y > HEIGHT - margin:
                self.velocity.y += turnFactor * (
                    (HEIGHT - margin - self.position.y) * 0.05
                )
            if self.position.x > WIDTH - margin:
                self.velocity.x += turnFactor * (
                    (WIDTH - margin - self.position.x) * 0.05
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

    def behaviour(self, quadTree):
        self.acceleration.update(0, 0)
        self.neighbours = quadTree.findInRect(self.vRect)
        if not self.neighbours is None:
            align = self.alignment(self.neighbours) * 0.8
            align = align * self.values["alignment"]
            self.acceleration += align

            coh = self.cohesion(self.neighbours) * 0.8
            coh = coh * self.values["cohesion"]
            self.acceleration += coh

            sep = self.separation(self.neighbours) * 0.8
            sep = sep * self.values["separation"]
            self.acceleration += sep


    def cohesion(self, neighbours):
        total = 0
        steering = pygame.Vector2(0, 0)

        for buddy in neighbours:
            dist = getDistance(self.position, buddy.position)
            if buddy is not self and self.vRadius/4 < dist < self.vRadius and self.colorID == buddy.colorID:
                steering += buddy.position

                total += 1

        if total > 0:
            steering = steering / total
            steering = steering - self.position
            if len(steering) != 0 and (steering.x != 0 and steering.y != 0):
                steering = steering.normalize()
            steering = steering * self.max_speed
            steering = steering - self.velocity
            if len(steering) != 0 and (steering.x != 0 and steering.y != 0):
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
            averageHeading = averageHeading * self.max_speed

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
                if buddy is not self and dist < self.radius+2:
                    temp = SubVectors(self.position, buddy.position)
                    temp = temp / (dist**2)
                    steering += temp

                    total += 1
        if total > 0:
            steering = steering / total
            steering = steering.normalize()
            if danger:
                steering = steering * (self.max_speed + 10)
                steering = steering - self.velocity
            else:
                steering = steering * self.max_speed
                steering = steering - self.velocity
                if len(steering) != 0 and (steering.x != 0 and steering.y != 0):
                    steering = steering.normalize()

        return steering

    def update(self, dragCoeff):
        # increases the boids vision if it cant see any flock members, decrease if it can see more than 3
        if not self.neighbours is None:
            buddyCount = 0
            for boid in self.neighbours: # pop all self.neighbours who are of the same flock and then get.
                if self.colorID == boid.colorID:
                    buddyCount += 1

            if buddyCount <= 3:
                if self.vRadius < 120:
                    self.vRadius += 10
            elif buddyCount > 3 and buddyCount <= 6:
                pass  # if the boid sees between 3 and 6 of his flock members it doesnt change its vision
            else:
                if self.vRadius > 30:
                    self.vRadius -= 10
        else:
            if self.vRadius < 120:
                self.vRadius += 10


        # update the possitional values of the boid
        self.velocity = pygame.Vector2(self.velocity.x * (1-dragCoeff), self.velocity.y * (1-dragCoeff))
        self.position += self.velocity
        self.velocity = self.velocity + self.acceleration
        self.velocity = self.velocity.clamp_magnitude(self.min_speed, self.max_speed)

        # Map velocity to hue of boid
        velToHue = num_to_range(self.velocity.magnitude(), 0, self.max_speed, 100, 360)
        self.color = colorsys.hsv_to_rgb(velToHue / 360.0, 115 / 255.0, 255 / 255.0) #Need to normalize the colors
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
        pygame.draw.circle(
            window,
            self.color,
            (
                makeBound(self.position.x, 0, WIDTH),
                makeBound(self.position.y, 0, HEIGHT),
            ),
            self.radius,
        )

        #p1 = pygame.Vector2(self.position.x + self.radius * 3, self.position.y)
        #p2 = pygame.Vector2(p1.x - self.radius * 3, p1.y - self.radius)
        #p3 = pygame.Vector2(p2.x, p2.y + self.radius)
        #p4 = pygame.Vector2(p3.x, p3.y + self.radius)
        #p5 = p1

        #triangle = [p1, p2, p3, p4, p5]

        # pygame.math.Vector2()

        # rotate_points_around_pivot(triangle, p3, dotProduct(self.position, self.velocity)) 

        # pygame.draw.polygon(window, self.color, triangle)

        pygame.draw.aaline(
            window,
            self.color,
            (self.position.x, self.position.y),
            (
                self.position.x + self.velocity.x * 2.5,
                self.position.y + self.velocity.y * 2.5,
            ),
        )
        # pygame.draw.polygon(window, self.color, boidEdges) #fills boid
        # pygame.draw.polygon(window, self.color, boidEdges, self.lineThicknes) #draws outline of boid
