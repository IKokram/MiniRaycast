import pygame
from settings import *


class Sprite:
	def __init__(self, img, pos, scale, shift):
		self.img = img
		self.pos = pos
		self.scale = scale
		self.shift = shift

	def object_loccate(self, player, walls):
		pass

