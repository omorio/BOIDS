import pygame
from math import pi, atan2, sqrt
from helpers import getDistance, SubVectors, makeBound
from random import uniform
from matrix import matrix_multiplication, rotationZ

width = 2560
height = 1440


class ChaserBoid:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(uniform(-3, 3), uniform(-3, 3))
        self.acceleration = pygame.Vector2()
        self.max_speed = 3
        self.max_length = 100
        self.size = 2
        self.angle = 0
        self.lineThicknes = 2
        self.radius = 60
        self.color = (255, 0, 0)
        self.toggles = {"separation": True, "alignment": True, "cohesion": True}
        self.values = {"separation": 0.29, "alignment": 1, "cohesion": 0.25}

    def edges(self, width, height, avoid, margin=50, turnFactor=0.5):
        margin *= 8
        turnFactor *= 0.8
        if avoid:
            if self.position.x < margin:
                self.velocity.x += turnFactor
            if self.position.y > height - margin:
                self.velocity.y -= turnFactor
            if self.position.x > width - margin:
                self.velocity.x -= turnFactor
            if self.position.y < margin:
                self.velocity.y += turnFactor
        else:
            if self.position.x > width:
                self.position.x = 0
            elif self.position.x < 0:
                self.position.x = width

            if self.position.y > height:
                self.position.y = 0
            elif self.position.y < 0:
                self.position.y = height

    def behaviour(self, chasers, flock):
        self.acceleration = pygame.Vector2()

        if self.toggles["separation"]:
            avoid = self.separation(chasers)
            avoid = avoid * self.values["separation"]
            self.acceleration += avoid

        if self.toggles["alignment"]:
            align = self.alignment(flock)
            align = align * self.values["alignment"]
            self.acceleration += align

        if self.toggles["cohesion"]:
            coh = self.cohesion(flock)
            coh = coh * self.values["cohesion"]
            self.acceleration += coh

    def separation(self, chasers):
        total = 0
        steering = pygame.Vector2()
        for buddy in chasers:
            dist = getDistance(self.position, buddy.position)
            if buddy is not self and dist < self.radius / 3:
                temp = self.position - buddy.position
                if dist > 0:
                    temp = temp / (dist ** 2)
                steering += temp
                total += 1
        if total > 0:
            steering /= total
            if steering.length_squared() > 0:
                steering.normalize_ip()
            steering *= self.max_speed
            steering -= self.velocity
            if steering.length() > self.max_length:
                steering.scale_to_length(self.max_length)
        return steering

    def alignment(self, flock):
        total = 0
        averageHeading = pygame.Vector2()
        for buddy in flock:
            dist = getDistance(self.position, buddy.position)
            if buddy is not self and dist < self.radius:
                vel = buddy.velocity
                if vel.length_squared() > 0:
                    vel = vel.normalize()
                averageHeading += vel
                total += 1

        if total > 0:
            averageHeading /= total
            if averageHeading.length_squared() > 0:
                averageHeading.normalize_ip()
            averageHeading *= self.max_speed
            vel_norm = self.velocity.normalize() if self.velocity.length_squared() > 0 else pygame.Vector2()
            averageHeading -= vel_norm
            if averageHeading.length() > self.max_length:
                averageHeading.scale_to_length(self.max_length)

        return averageHeading

    def cohesion(self, flock):
        total = 0
        steering = pygame.Vector2()
        for buddy in flock:
            dist = getDistance(self.position, buddy.position)
            if buddy is not self and dist < self.radius:
                steering += buddy.position
                total += 1

        if total > 0:
            steering /= total
            steering -= self.position
            if steering.length_squared() > 0:
                steering.normalize_ip()
            steering *= self.max_speed
            steering -= self.velocity
            if steering.length() > self.max_length:
                steering.scale_to_length(self.max_length)

        return steering

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        self.angle = atan2(self.velocity.y, self.velocity.x) + pi / 2

    def draw(self, window, distance, scale):
        boidEdges = []
        points = [None for _ in range(3)]

        points[0] = [[0], [-self.size], [0]]
        points[1] = [[self.size // 2], [self.size // 2], [0]]
        points[2] = [[-self.size // 2], [self.size // 2], [0]]

        for point in points:
            rotated = matrix_multiplication(rotationZ(self.angle), point)
            z = 1 / (distance - rotated[2][0])

            projection_matrix = [[z, 0, 0], [0, z, 0]]
            projected_2d = matrix_multiplication(projection_matrix, rotated)

            x = int(projected_2d[0][0] * scale) + self.position.x
            y = int(projected_2d[1][0] * scale) + self.position.y
            boidEdges.append((x, y))

        pygame.draw.circle(window, self.color, (makeBound(self.position.x, 0, width), makeBound(self.position.y, 0, height)), 4)
        pygame.draw.aaline(window, self.color, (self.position.x, self.position.y),
                           (self.position.x + self.velocity.x * 4, self.position.y + self.velocity.y * 4))
