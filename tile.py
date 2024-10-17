import pygame
from settings import CELL_HEIGHT, CELL_WIDTH


class Tile:
	def __init__(self, pos, color):
		self.pos = pos
		self.color = color
		self.width = CELL_WIDTH
		self.height = CELL_HEIGHT

	def __repr__(self):
		return f"pos: {self.pos} color: {self.color} width: {self.width} height: {self.height}"

	def draw(self, surf):
		pygame.draw.rect(surf, self.color, (self.pos.x, self.pos.y, self.width, self.height), width=5)