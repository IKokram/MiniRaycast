import pygame
import tile
from settings import *

class MapLoader:
	def __init__(self, file = None):
		self.width = CELL_WIDTH
		self.height = CELL_HEIGHT
		self.start_pos = pygame.Vector2((WIDTH//2, HEIGHT//2))
		self.size_map = [0, 0]
		if file:
			self.mapL = self.load_file(file)
			self.fullmap_fill()
		else:
			self.mapL = []
		self.full_map = []

	def load_file(self, file):
		return self.load(self.read_file(file))

	def read_file(self, file):
		with open(file, "r") as f:
			return f.read()

	def load(self, locate, pos = pygame.Vector2((WIDTH//2, HEIGHT//2))):
		self.start_pos = pos
		load_map = []
		all_map = locate.split("\n")
		self.size_map[0] = len(all_map[0])
		self.size_map[1] = len(all_map)
		self.full_map = [[0] * self.size_map[0] for _ in range(self.size_map[1])]
		for y, line in enumerate(all_map):
			for x, block in enumerate(line):
				if block != " ":
					load_map.append(tile.Tile(pygame.Vector2(x*self.width, y*self.height), (255, 0, 0)))
					self.full_map[y][x] = block
		return load_map

	def draw(self, surf, min_map_draw):
		for tile in self.mapL:
			if min_map_draw[int(tile.pos.y//CELL_HEIGHT)][int(tile.pos.x//CELL_WIDTH)]:
				tile.draw(surf)

	def get_map(self):
		return self.mapL

	def get_full_map(self):
		return self.full_map

	def fullmap_show(self):
		for line in self.full_map:
			print(*line)
