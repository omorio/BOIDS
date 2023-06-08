import pygame
from math import pi
from helpers import *
from random import uniform, randint
from matrix import *
from UI import *

class Boid: 
    def __init__(self, x, y):
        self.position = Vec(x, y)
        vel_x = uniform(-1,1)
        vel_y = uniform(-1,1)
        self.velocity = Vec(vel_x, vel_y)
        self.acceleration = Vec()
        self.min_speed = 1 #unused
        self.max_speed = 3
        self.max_length = 1
        self.size = 2
        self.angle = 0
        self.lineThicknes = 2
        self.radius = 60
        self.id = randint(1,8)
        self.color = (255,255,255)#(uniform(100,200), 0 ,uniform(100,200))
        self.toggles = {"separation":True, "alignment":True, "cohesion":True}
        self.values = {"separation":1, "alignment":1, "cohesion":1}

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
        
        
    def edges(self, width, height, avoid, margin, turnFactor):
        if avoid:
            if self.position.x < margin:
                self.velocity.addX(turnFactor*((margin-self.position.x)*0.05))
            if self.position.y > height - margin:
                self.velocity.addY(turnFactor*((height - margin - self.position.y)*0.05))
            if self.position.x > width - margin:
                self.velocity.addX(turnFactor*((width - margin - self.position.x)*0.05))
            if self.position.y < margin:
                self.velocity.addY(turnFactor*((margin-self.position.y)*0.05))

                #calulate dot product between vel vector and the vec that is perpendicular to the edge.
                #if dot product positive it is moving towards it.

                #then calculate the angle between velocity vect and boundary and steer by a small fraction of this angle.
                #the dot product help determine if to move in the positive or negative direction.
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
        self.acceleration.reset()

        if self.toggles["alignment"] == True:
            align = self.alignment(flock)
            align = align * self.values["alignment"]
            self.acceleration.add(align)

        if self.toggles["cohesion"]== True:
            coh = self.cohesion(flock)
            coh = coh * self.values["cohesion"]
            self.acceleration.add(coh)

        if self.toggles["separation"] == True:
            avoid = self.separation(chasers, flock)
            avoid = avoid * self.values["separation"]
            self.acceleration.add(avoid)
        

    def cohesion(self, flock):
        total = 0
        steering = Vec()
        for buddy in flock:
            dist = getDistance(self.position, buddy.position)
            if buddy is not self and dist < self.radius and self.id == buddy.id:
                steering.add(buddy.position)

                total += 1
        
        if total > 0:
            steering = steering / total
            steering = steering - self.position
            steering.normalize()
            steering = steering * self.max_speed
            steering = steering - self.velocity
            steering.limit(self.max_length)

        return steering    

    def alignment(self, flock):
        total = 0
        averageHeading = Vec()
        for buddy in flock:
            dist = getDistance(self.position, buddy.position)
            if buddy is not self and dist < self.radius and self.id == buddy.id:
                vel = buddy.velocity.Normalize() 
                averageHeading.add(vel)
        
                total += 1
        
        if total > 0:
            averageHeading = averageHeading / total
            averageHeading.normalize()
            averageHeading = averageHeading * self.max_speed
            averageHeading = averageHeading - self.velocity.Normalize()
            averageHeading.limit(self.max_length)

        return averageHeading
    
    def separation(self, chasers ,flock):
        total = 0
        steering = Vec()
        danger = False
        for buddy in flock:
            dist = getDistance(self.position, buddy.position)
            chaserDist = float
            for chaser in chasers:
                chaserDist = (getDistance(self.position, chaser.position))
                if chaserDist < self.radius: 
                    temp = SubVectors(self.position, chaser.position)
                    temp = temp/(chaserDist ** 2)
                    self.acceleration.add(temp)
            if buddy is not self and dist < self.radius/3:
                temp = SubVectors(self.position, buddy.position)
                temp = temp/(dist ** 2)
                steering.add(temp)
            
        
                total += 1
        if total > 0:
            steering = steering / total
            steering.normalize()
            if danger:
                steering = steering * self.max_speed + 10
                steering = steering - self.velocity
            else:
                steering = steering * self.max_speed
                steering = steering - self.velocity
                steering.limit(self.max_length)
        return steering

    def update(self):
        # update the possitional values of the boid
        self.position += self.velocity
        self.velocity = self.velocity + self.acceleration
        self.velocity.limit(self.max_speed)
        self.angle = self.velocity.heading() + pi/2

    def draw(self, window, distance, scale):
        # initializes array that will later hold the verteces of the boid
        boidEdges = []
        # initialize a 3d matrix
        points = [None for _ in range(3)]

        points[0] = [[0], [-self.size], [0]]
        points[1] = [[self.size//2], [self.size//2], [0]]
        points[2] = [[-self.size//2], [self.size//2], [0]]

        # point the boid in the direction of travell
        for point in points:

            rotated = matrix_multiplication(rotationZ(self.angle) , point)
            z = 1/(distance - rotated[2][0])

            projection_matrix = [[z, 0, 0], [0, z, 0]]
            projected_2d = matrix_multiplication(projection_matrix, rotated)

            x = int(projected_2d[0][0] * scale) + self.position.x
            y = int(projected_2d[1][0] * scale) + self.position.y
            boidEdges.append((x, y))
        pygame.draw.circle(window, self.color, (makeBound(self.position.x, 0, width), makeBound(self.position.y, 0, height)), 4)
        pygame.draw.aaline(window, self.color, (self.position.x, self.position.y), 
                    (self.position.x + self.velocity.x*4, self.position.y + self.velocity.y*4))
        #pygame.draw.polygon(window, self.color, boidEdges) #fills boid
        #pygame.draw.polygon(window, self.color, boidEdges, self.lineThicknes) #draws outline of boid


