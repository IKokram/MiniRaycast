import pygame
from settings import *
import math


def lerp(a, b, t):
	return a + (b-a)*t


def clamp(mn, mx, a):
	return max(min(mx, a), mn)


def vec_to_cof(vec1, vec2):
	A = vec1[1]-vec2[1]
	B = vec1[0]-vec2[0]
	C = vec1[0]*vec2[1]-vec2[0]*vec1[1]
	return A, B, C


def colision_line(ABC1, ABC2):
	if ABC1[0]*ABC2[1]-ABC1[1]*ABC2[0] != 0:
		return pygame.Vector2((ABC1[1]*ABC2[2]-ABC1[2]*ABC2[1])/(ABC1[0]*ABC2[1]-ABC1[1]*ABC2[0]), -(ABC1[2]*ABC2[0]-ABC1[0]*ABC2[2])/(ABC1[0]*ABC2[1]-ABC1[1]*ABC2[0]))
	


def raycast(pos, direct, distance, location):
	map_pos = pygame.Vector2(pos.x//CELL_WIDTH, pos.y//CELL_HEIGHT)

	sin_a, cos_a = math.sin(direct), math.cos(direct)
	sin_a = sin_a if sin_a else 0.000001
	cos_a = cos_a if cos_a else 0.000001
	depth_v = 0
	depth_h = 0

	x, dx = (CELL_WIDTH * (map_pos.x+1), 1) if cos_a >= 0 else (CELL_WIDTH * map_pos.x, -1)
	y, dy = ((map_pos.y+1) * CELL_HEIGHT, 1) if sin_a >= 0 else (map_pos.y * CELL_HEIGHT, -1)

	for _ in range(0, WIDTH, CELL_WIDTH):
		depth_v = (x - pos.x) / cos_a
		y1 = pos.y + depth_v * sin_a
		mx, my = int((dx+x)//CELL_WIDTH), int(y1//CELL_HEIGHT)
		if 0 <= mx < len(location[0]) and 0 <= my < len(location):
			if location[my][mx]:
				break
		x += dx * CELL_WIDTH
		if depth_v > distance:
			break

	
	for _ in range(0, HEIGHT, CELL_HEIGHT):
		depth_h = (y - pos.y) / sin_a
		x1 = pos.x + depth_h * cos_a
		mx, my = int(x1//CELL_WIDTH), int((y+dy)//CELL_HEIGHT)
		if 0 <= mx < len(location[0]) and 0 <= my < len(location):
			if location[my][mx]:
				break
		y += dy * CELL_HEIGHT
		if depth_h > distance:
			break

	if min(depth_v, depth_h) > distance:
		return distance, 0
	return min(depth_v, depth_h), 1