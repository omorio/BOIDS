from math import sqrt, atan2
import pygame

width = 1080+400 #2048 
height = 720+130 #1080

def getDistance(v1, v2): # recieves two vectors and finds the distance between them.
	return sqrt((v1.x - v2.x)**2 + (v1.y - v2.y)**2)

def SubVectors(v1, v2): #recieve two vectors and substract them.
	return pygame.Vector2(v1.x - v2.x, v1.y - v2.y)

def dotProduct(v1, v2):
	return v1.angle_to(v2)


def makeBound(x, lower, upper):
	if x < lower:
		return lower
	elif x > upper:
		return upper
	else:
		return x

def mouseInBound(rect, pos):
	x, y = pos
	if x > 0 and x < rect.x:
		if y > 0 and y < height:
			return True
		else: 
			return False
	elif x > rect.x:
		if y < rect.y:
			return True
		elif y > rect.y+rect.height:
			return True
		else:
			return False
	else: 
		return False

def rotate_points_around_pivot(points, pivot, angle):
    pp = pygame.math.Vector2(pivot)
    rotated_points = [
        (pygame.math.Vector2(x, y) - pp).rotate(angle) + pp for x, y in points]
    return rotated_points

class Vec:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def __mul__(self, a):
		self.x = self.x * a
		self.y = self.y * a
		return self

	def __add__(self, a):
		self.x = self.x + a.x
		self.y = self.y + a.y
		return self

	def __sub__(self, a):
		self.x = self.x - a.x
		self.y = self.y - a.y
		return self

	def __truediv__(self, a):
		self.x = self.x / a
		self.y = self.y / a
		return self

	def add(self, a):
		self.x = self.x + a.x
		self.y = self.y + a.y

	def addX(self, a):
		self.x = a + self.x
		return self

	def addY(self, a):
		self.y = self.y + a
		return self
		
	def parseToInt(self):
		return (int(self.x), int(self.y))

	def magnitude(self):
		return sqrt(self.x * self.x + self.y * self.y)

	def normalize(self):
		mag = self.magnitude()
		if not (mag == 0 ):
			self = self/mag
	def Normalize(self):
		mag = self.magnitude()
		if mag != 0:
			return Vec(self.x/mag, self.y/mag)
		else:
			return Vec(1, 1)

	def heading(self):
		angle = atan2(self.y, self.x)
		# in radians
		return angle

	def limit(self, max_length):
		squared_mag = self.magnitude() * self.magnitude()
		if squared_mag > (max_length * max_length):
			self.x = self.x/sqrt(squared_mag)
			self.y = self.y/sqrt(squared_mag)
			self.x = self.x * max_length
			self.y = self.y * max_length
	def reset(self, x=0, y=0):
		self.x = x
		self.y = y

	def __repr__(self):
		return f'vector-> x:{self.x}, y:{self.y}'