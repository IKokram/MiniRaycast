import pygame
from settings import *
from function import raycast
import player
import math
import map_loader
from GenMap import generate

pygame.init()

file = "brick_wall.png"
file1 = "concrete_wall.png"
img = pygame.image.load(file)
img1 = pygame.image.load(file1)

display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

mapLoader = map_loader.MapLoader()
mas = generate(12, 10, 3, 100)
mapLoader.mapL = mapLoader.load(mas[2], pygame.Vector2(mas[0]*mapLoader.width+mapLoader.width//2, mas[1]*mapLoader.height+mapLoader.height//2))
ply = player.Player(mapLoader.start_pos)

min_map_draw = [[0] * len(mapLoader.get_full_map()[0]) for _ in mapLoader.get_full_map()]

min_map_surf = pygame.Surface((TILE_WIDTH * CELL_WIDTH, TILE_HEIGHT * CELL_HEIGHT))
deltatime = 0
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				mas = generate(w_size=TILE_WIDTH, h_size=TILE_HEIGHT, density=DENSITY, step=STEP)
				mapLoader.mapL = mapLoader.load(mas[2], pygame.Vector2(mas[0]*mapLoader.width+mapLoader.width//2, mas[1]*mapLoader.height+mapLoader.height//2))
				mapLoader.fullmap_show()
				ply = player.Player(mapLoader.start_pos)
				min_map_draw = [[0] * len(mapLoader.get_full_map()[0]) for _ in mapLoader.get_full_map()]

	ply.update(deltatime, mapLoader.mapL)
	display.fill((0, 0, 0))
	min_map_surf.fill((0, 0, 0))
	mapLoader.draw(min_map_surf, min_map_draw)

	pygame.draw.rect(display, (50, 90, 255), (0, 0, WIDTH, HEIGHT//2))
	pygame.draw.rect(display, (12, 52, 14), (0, HEIGHT//2, WIDTH, HEIGHT))
	
	start_angel = ply.angle - HALF_FOV
	end_alpha = ply.angle + HALF_FOV
	for i in range(QUALITY):
		curr_angel = start_angel + ANGLE_PER_RAY*i
		direct = pygame.Vector2(math.cos(curr_angel), math.sin(curr_angel))
		ray_distance, hit = raycast(ply.pos, curr_angel, DISTANCE, mapLoader.get_full_map())
		pygame.draw.line(min_map_surf, (0, 255, 0), ply.pos, ply.pos + direct*ray_distance)
		if hit:
			pos_colision = ply.pos + (ray_distance+0.001)*direct
			map_pos = [int(pos_colision.x//CELL_WIDTH), int(pos_colision.y//CELL_HEIGHT)]
			min_map_draw[map_pos[1]][map_pos[0]] = 1
			ray_distance *= math.cos(ply.angle - curr_angel)
			ray_distance = ray_distance if ray_distance else 1
			high = abs(WALL_HIGH / ray_distance)
			high = min(high, HEIGHT)
			color_cof = abs(40/ray_distance)


			#mapLoader.fullmap_show()
			imgToDraw = img
			match mapLoader.get_full_map()[map_pos[1]][map_pos[0]]:
				case "#":
					imgToDraw = img1
				case "$":
					imgToDraw = img

			offset = 0
			width_img = imgToDraw.get_width()
			center_col = pygame.Vector2(map_pos[0] * CELL_WIDTH + CELL_WIDTH//2, map_pos[1] * CELL_HEIGHT + CELL_HEIGHT//2)
			pos_colision_img = pos_colision - center_col
			pos_colision_img = pygame.Vector2(-abs(pos_colision_img.x), -abs(pos_colision_img.y))
			if pos_colision_img.x > pos_colision_img.y:
				if pos_colision_img.x < 0:
					offset = int(((pos_colision.x - map_pos[0] * CELL_WIDTH)/CELL_WIDTH)*width_img)
				else:
					offset = int((((map_pos[0] + 1)* CELL_WIDTH - pos_colision.x)/CELL_WIDTH)*width_img)
			else:
				if pos_colision_img.y < 0:
					offset = int(((pos_colision.y - map_pos[1] * CELL_HEIGHT)/CELL_HEIGHT) * width_img)
				else:
					offset = int((((map_pos[1] + 1)* CELL_HEIGHT - pos_colision.y)/CELL_HEIGHT) * width_img)

			wall_surf = pygame.Surface((WALL_SIZE_WIDTH, high*2))
			if offset + WALL_SIZE_WIDTH > width_img:
				imgToDraw = imgToDraw.subsurface(offset, 0, width_img-offset, imgToDraw.get_height())
			else:
				imgToDraw = imgToDraw.subsurface(offset, 0, WALL_SIZE_WIDTH, imgToDraw.get_height())
			wall_surf.blit(pygame.transform.scale(imgToDraw, (width_img, high*2)), (0, 0))
			display.blit(wall_surf, (WALL_SIZE_WIDTH*i, HEIGHT//2 - high))


	ply.draw(min_map_surf)
	display.blit(pygame.transform.scale(min_map_surf, (MIN_MAP_WIDTH, MIN_MAP_HEIGHT)), (0, 0))
	pygame.display.flip()

	deltatime = clock.tick(FPS)/1000

