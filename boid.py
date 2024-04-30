import pygame
from math import pi
from helpers import *
from random import uniform, randint
from matrix import *
from UI import *

width = 2560
height = 1440

class Boid:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        vel_x = uniform(-1, 1)
        vel_y = uniform(-1, 1)
        self.velocity = pygame.Vector2(vel_x, vel_y)
        self.acceleration = pygame.Vector2()
        self.min_speed = 2 #1
        self.max_speed = 4 #3 was original
        self.size = 2
        self.angle = 0
        self.lineThicknes = 2
        self.radius = 4  # Radius of blob
        self.vRadius = 60  # Vision square width and height.
        self.vRect = pygame.Rect( #defines the vision area.
            self.position.x - self.vRadius / 2,
            self.position.y - self.vRadius / 2,
            self.vRadius,
            self.vRadius
        )
        self.rect = pygame.Rect(
            self.position.x - self.radius / 2,
            self.position.y - self.radius / 2,
            self.radius,
            self.radius
        )
        self.rect.collidepoint
        self.id = randint(1, 8)
        self.color = (255, 255, 255)  # (uniform(100,200), 0 ,uniform(100,200))
        self.toggles = {"separation": True, "alignment": True, "cohesion": True}
        self.values = {"separation": 1, "alignment": 1, "cohesion": 1}

        if self.id == 1:
            self.color = (255, 150, 0)
        if self.id == 2:
            self.color = (0, 255, 255)
        if self.id == 3:
            self.color = (255, 0, 255)
        if self.id == 4:
            self.color = (0, 255, 0)
        if self.id == 5:
            self.color = (0, 150, 255)
        if self.id == 6:
            self.color = (255, 255, 0)
        if self.id == 7:
            self.color = (255, 128, 255)
        if self.id == 8:
            self.color = (0, 0, 255)
        #self.color = (255, 255, 255) 

    def edges(self, width, height, avoid, margin, turnFactor): #Determines what happens when a boid reaches an edge of the window
        if avoid:
            if self.position.x < margin:
                self.velocity.x += (turnFactor * ((margin - self.position.x) * 0.05))
            if self.position.y > height - margin:
                self.velocity.y += (
                    turnFactor * ((height - margin - self.position.y) * 0.05)
                )
            if self.position.x > width - margin:
                self.velocity.x += (
                    turnFactor * ((width - margin - self.position.x) * 0.05)
                )
            if self.position.y < margin:
                self.velocity.y += (turnFactor * ((margin - self.position.y) * 0.05))

                # calulate dot product between vel vector and the vec that is perpendicular to the edge.
                # if dot product positive it is moving towards it.

                # then calculate the angle between velocity vect and boundary and steer by a small fraction of this angle.
                # the dot product help determine if to move in the positive or negative direction.
        else:
            if self.position.x > width:
                self.position.x = 0
            elif self.position.x < 0:
                self.position.x = width

            if self.position.y > height:
                self.position.y = 0
            elif self.position.y < 0:
                self.position.y = height

    def behaviour(self, quadTree):
        self.acceleration.update(0,0)
        self.neighbours = quadTree.hit(self.vRect) #do once only in the behavior funciton and then pass it into the 3 diff funcs
        if(not self.neighbours is None):
            if self.toggles["alignment"] == True:
                align = self.alignment(quadTree, self.neighbours) * 0.8
                align = align * self.values["alignment"]
                self.acceleration += align

            if self.toggles["cohesion"] == True:
                coh = self.cohesion(quadTree, self.neighbours) * 0.8
                coh = coh * self.values["cohesion"]
                self.acceleration += coh

            if self.toggles["separation"] == True:
                sep = self.separation(quadTree, self.neighbours) * 0.8
                sep = sep * self.values["separation"]
                self.acceleration += sep

    def cohesion(self, quadTree, neighbours):
        total = 0
        steering = pygame.Vector2(0,0)
        
        for buddy in neighbours:
            dist = getDistance(self.position, buddy.position)
            if buddy is not self and dist < self.vRadius and self.id == buddy.id:
                steering += buddy.position

                total += 1

        if total > 0:
            steering = steering / total
            steering = steering - self.position
            steering = steering.normalize()
            steering = steering * self.max_speed
            steering = steering - self.velocity
            if(len(steering) != 0 and (steering.x != 0 and steering.y != 0) ):
                steering = steering.normalize()

        return steering

    def alignment(self, quadTree, neighbours):
        total = 0
        averageHeading = pygame.Vector2(0,0)
        
        for buddy in neighbours:
            dist = getDistance(self.position, buddy.position)
            if buddy is not self and dist < self.vRadius and self.id == buddy.id:
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

    def separation(self, quadTree, neighbours):
        total = 0
        steering = pygame.Vector2(0,0)
        danger = False
        
        for buddy in neighbours:
            dist = getDistance(self.position, buddy.position)
            if buddy is not self and dist < self.vRadius / 6:
                temp = SubVectors(self.position, buddy.position)
                temp = temp / (dist**2)
                steering += temp

                total += 1
        if total > 0:
            steering = steering / total
            steering = steering.normalize()
            if danger:
                steering = steering * self.max_speed + 10
                steering = steering - self.velocity
            else:
                steering = steering * self.max_speed
                steering = steering - self.velocity
                if(len(steering) != 0 and (steering.x != 0 and steering.y != 0) ):
                    steering = steering.normalize()
                
        return steering

    def update(self):
        #increases the boids vision if it cant see any flock members, decrease if it can see more than 3
        if self.neighbours is not None:
            buddyCount = 0
            for boid in self.neighbours:
                if(self.id == boid.id):
                    buddyCount += 1

            if (buddyCount <= 3):
                if(not self.vRadius >= 120):
                    self.vRadius += 10
            elif (buddyCount > 3 and buddyCount <= 5):
                pass #if the boid has between 3 and 5 buddies it doesnt change its vision
            else:
                if(not self.vRadius <= 60):
                    self.vRadius -= 10
        else:
            if(not self.vRadius >= 120):
                self.vRadius += 10
                
        # update the possitional values of the boid
        self.position += self.velocity
        self.velocity = self.velocity + self.acceleration
        self.velocity = self.velocity.clamp_magnitude(self.min_speed, self.max_speed)

        #self.velocity.limit(self.max_speed)
        #self.angle = self.velocity.heading() + pi / 2

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

    def draw(self, window, distance, scale):
        pygame.draw.circle(
            window,
            self.color,
            (
                makeBound(self.position.x, 0, width),
                makeBound(self.position.y, 0, height),
            ),
            self.radius,
        )
        


        p1 = pygame.Vector2(self.position.x + self.radius*3, self.position.y)
        p2 = pygame.Vector2(p1.x - self.radius*3, p1.y - self.radius)
        p3 = pygame.Vector2(p2.x, p2.y + self.radius)
        p4 = pygame.Vector2(p3.x, p3.y + self.radius)
        p5 = p1

        triangle = [p1, p2, p3, p4, p5]

        #pygame.math.Vector2()



        #rotate_points_around_pivot(triangle, p3, dotProduct(self.position, self.velocity)) # TODO: rotate triangle around pivot 

        #pygame.draw.polygon(window, self.color, triangle)

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
