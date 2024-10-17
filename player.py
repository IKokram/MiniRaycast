import pygame
from math import sin, cos, pi
from function import clamp
from random import randint

class Player:
	def __init__(self, pos):
		self.pos = pygame.Vector2(pos)
		self.angle = randint(0, 100)/50 * pi
		self.speed = 40
		self.angle_speed = pi*.7
		self.radius = 5

	def direct_vect(self):
		return pygame.Vector2(cos(self.angle), sin(self.angle))

	def direct_vect_norm(self):
		return pygame.Vector2(cos(self.angle + pi/2), sin(self.angle + pi/2))

	def move(self, dt):
		keys = pygame.key.get_pressed()
		move = pygame.Vector2(0, 0)
		if keys[pygame.K_w]:
			move += self.direct_vect() * self.speed * dt
		if keys[pygame.K_s]:
			move += -self.direct_vect() * self.speed * dt
		if keys[pygame.K_d]:
			move += self.direct_vect_norm() * self.speed * dt
		if keys[pygame.K_a]:
			move += -self.direct_vect_norm() * self.speed * dt
		if keys[pygame.K_e]:
			self.angle += self.angle_speed * dt
		if keys[pygame.K_q]:
			self.angle += -self.angle_speed * dt
		return move

	def who_collision(self, locate):
		for tile in locate:
			mn_p = pygame.Vector2(self.pos.x-self.radius, self.pos.y-self.radius)
			mx_p = pygame.Vector2(self.pos.x+self.radius, self.pos.y+self.radius)

			if not (((tile.pos.x < mn_p.x < tile.pos.x+tile.width) or (tile.pos.x < mx_p.x < tile.pos.x+tile.width)) and ((tile.pos.y < mn_p.y < tile.pos.y+tile.height) or (tile.pos.y < mx_p.y < tile.pos.y+tile.height))):
				continue

			closes_p = self.pos.copy()
			closes_p.x = clamp(tile.pos.x, tile.pos.x+tile.width, closes_p.x)
			closes_p.y = clamp(tile.pos.y, tile.pos.y+tile.height, closes_p.y)
			if (self.pos-closes_p).length() < self.radius:
				return tile

	def collision(self, locate, move_vec, dt):
		self.pos.x += move_vec.x

		tile = self.who_collision(locate)
		if tile:
			if move_vec.x < 0:
				self.pos.x = tile.pos.x+tile.width+self.radius
			elif move_vec.x > 0:
				self.pos.x = tile.pos.x-self.radius


		self.pos.y += move_vec.y

		tile = self.who_collision(locate)
		if tile:
			if move_vec.y < 0:
				self.pos.y = tile.pos.y+tile.height+self.radius
			elif move_vec.y > 0:
				self.pos.y = tile.pos.y-self.radius

	def update(self, dt, locate):
		self.collision(locate, self.move(dt), dt)

	def draw(self, surf):
		pygame.draw.circle(surf, (0, 0, 255), self.pos, self.radius)
		#pygame.draw.line(surf, (0, 0, 255), self.pos, self.pos+self.direct_vect()*self.radius)